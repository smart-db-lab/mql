import json
import os
import re
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import rest_framework.status as status

from .models import UploadedFile, MLModel, QueryResponse
from .parser.query_process import query_process
from .parser.Function.csvToDB import csv_to_db
from .parser.Function.rearrange_query import rearrange_query
from django.core.files.base import ContentFile

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    """
    Handle CSV/SQL file upload, store in media, and create DB table if CSV.
    """
    user = request.user
    file = request.FILES.get('file')
    if not file:
        return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

    file_type = 'csv' if file.name.endswith('.csv') else 'sql'
    uploaded = UploadedFile.objects.create(user=user, file=file, file_type=file_type)

    if file_type == 'csv':
        try:
            table_name = csv_to_db(uploaded.file, user_id=user.id,csv_name= file.name)
            uploaded.table_name = table_name
            uploaded.save()
        except Exception as e:
            uploaded.delete()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"message": "File uploaded successfully.", "file_id": uploaded.id}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_datasets(request):
    """
    List all datasets (tables) uploaded by the user.
    """
    user = request.user
    datasets = UploadedFile.objects.filter(user=user, file_type='csv').values('id', 'file', 'table_name', 'uploaded_at')
    return Response({"datasets": list(datasets)}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_query(request):
    """
    Accepts a user query (ML or SQL), processes it, stores response and graph.
    """
    user = request.user
    data = request.data.get('input', '').strip()
    if not data:
        return Response({"error": "No query provided."}, status=status.HTTP_400_BAD_REQUEST)

    data = rearrange_query(data)
    if isinstance(data, str):
        data = [data]

    responses = {}
    for idx, cmd in enumerate(data):
        print(cmd, "cmd")

        if cmd.strip():
            for resp in query_process(cmd, user=user):  
                # Save response and graph if present
                graph_file = None
                if isinstance(resp,dict) and  resp.get('graph_path',None):
                    print(resp['graph_path'], "graph_path")
                    graph_path = resp['graph_path']
                    if os.path.exists(graph_path):
                        # Save to media folder
                        from django.core.files import File
                        with open(graph_path, 'rb') as f:
                            graph_file = File(f)
                            graph_name = os.path.basename(graph_path)
                            print("graph condition before ")
                            qr = QueryResponse.objects.create(
                                user=user,
                                query=cmd,
                                response_text=json.dumps(resp.get('text', '')),
                                response_table=resp.get('table', None),
                                graph_file=graph_file
                            )
                            print("graph condition afte")
                            responses[f'response_{idx}'] = {
                                "text": resp.get('text', ''),
                                "table": resp.get('table', ''),
                                "graph": resp.get('graph', ''),
                                "graph_url": qr.graph_file.url if qr.graph_file else None,
                                "graph_path": graph_path,
                                "graph_link": resp.get('graph_link', None),
                                "performance_table": resp.get("performance_table", None)
                            }
                            continue
                qr = QueryResponse.objects.create(
                    user=user,
                    query=cmd,
                    response_text=json.dumps(resp.get('text', ''))
                )
                
                table_data = resp.get('table', None)
                if table_data and isinstance(table_data, list):
                    import pandas as pd
                    df = pd.DataFrame(table_data)
                    print("df ok", df)
                    df = df.replace([float('inf'), float('-inf'), float('nan')], None)
                    csv_content = df.to_csv(index=False, header=True) 
                    resp['table'] = df.to_dict(orient='records')
                    print("csv_content")
                    filename = f"user_{user.id}_response_{qr.id}_table.csv"
                    qr.response_table.save(filename, ContentFile(csv_content))
                    print("csv_content saved")
                    qr.save()
                    
                graphdata = resp.get('graph', '')
                graph_path = resp.get('graph_path', None)
                if graph_path and os.path.exists(graph_path):
                    with open(graph_path, 'rb') as f:
                        qr.graph_file.save(os.path.basename(graph_path), File(f))
                        qr.save()
                

                responses[f'response_{idx}'] = {
                    "text": resp.get('text', ''),
                    "table": resp.get('table', ''),
                    "graph_url": qr.graph_file.url if qr.graph_file else None,
                    "graph": resp.get('graph', ''),
                    "graph_path": qr.graph_file.path if qr.graph_file else None,
                    "graph_link": resp.get('graph_link', None),
                    "performance_table": resp.get("performance_table", None)
                }

    return Response(responses, status=status.HTTP_200_OK)

DATASET_FOLDER = settings.DATASET_FOLDER
DEFAULT_DATASET = None

@api_view(['POST'])
def set_datasets(request):
    file_name = request.data.get('file_name', None)

    if not file_name:
        return Response({"error": "No file name provided"}, status=status.HTTP_400_BAD_REQUEST)

    file_path = os.path.join(DATASET_FOLDER, file_name)
    
    if not os.path.exists(file_path):
        return Response({"error": f"File '{file_name}' does not exist in the dataset folder."}, status=status.HTTP_404_NOT_FOUND)

    try:
        csv_to_db(file_path)  

        return Response({"message": f"File '{file_name}' processed successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)