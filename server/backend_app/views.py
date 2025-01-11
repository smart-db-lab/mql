import json
import os
import re
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.response import Response

from .parser.query_process import query_process
from .parser.Function.csvToDB import csvToDB
from .parser.Function.rearrange_query import rearrange_query


@csrf_exempt
@api_view(['GET', 'POST'])
def test_view(req):
    if req.method == 'POST':
        current_directory = os.path.dirname(__file__)
        if 'file' in req.FILES:
            file = req.FILES['file']
            print(file)
            file_name = file.name
            file_path = os.path.join(current_directory, f'./data/files/{file_name}')
            if file_name.endswith('.csv'):
                csvToDB(file)
            else:
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
        if 'test' in req.FILES:
            file = req.FILES['test']
            file_name = file.name
            file_path = os.path.join(current_directory, f'./data/files/{file_name}')
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        
        data = req.POST.get('input')  # json.loads(req.body)
        data = data.strip()
        data= rearrange_query(data)
        # data = data.split(';')
        # if "WHERE" in  data[0].upper():
        #     data=data[0].split("WHERE")
        #     if "BASED ON" in data[1]:
        #         s=data[1].split("BASED ON")
            
        #     data[0],data[1]=data[1].strip(),data[0].strip()
        #     print(data)
        print(data, type(data))
        if type(data) == str:
            data = [data]
        print(data, type(data))
        
        responses = {}  
        for index, cmd in enumerate(data):
            if cmd != " " and cmd !="" and cmd != ";":
                responses[f'response_{index}'] = {}
                for response_dict in query_process(cmd):
                    # print("response", response_dict)
                    responses[f'response_{index}'].update(response_dict)  

        # print(responses)
        response_json = json.dumps(responses)
        # print("response is", response_json)
        return JsonResponse(response_json, safe=False)



DATASET_FOLDER = settings.DATASET_FOLDER
DEFAULT_DATASET = None

import rest_framework.status as status
@api_view(['GET'])
def list_datasets(request):
    try:
        datasets = [f for f in os.listdir(DATASET_FOLDER) if os.path.isfile(os.path.join(DATASET_FOLDER, f))]
        return Response({"datasets": datasets}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Constants
DATASET_FOLDER = settings.DATASET_FOLDER

@api_view(['POST'])
def set_datasets(request):
    file_name = request.data.get('file_name', None)

    if not file_name:
        return Response({"error": "No file name provided"}, status=status.HTTP_400_BAD_REQUEST)

    file_path = os.path.join(DATASET_FOLDER, file_name)
    
    if not os.path.exists(file_path):
        return Response({"error": f"File '{file_name}' does not exist in the dataset folder."}, status=status.HTTP_404_NOT_FOUND)

    try:
        csvToDB(file_path)  

        return Response({"message": f"File '{file_name}' processed successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)