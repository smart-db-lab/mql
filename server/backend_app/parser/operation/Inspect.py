import pandas as pd
import os
import sqlite3

from ..Function.categorize import categorize

from ..Function.deduplicate import deduplicate
from ..Function.encoding import encoding
from ..Function.checknull import checknull
from ..Function.Imputer import impute

from ..Function.utility import response_schema
from .utils import get_arg, get_dataset_name


def inspect(command):
    '''
    INSPECT CHECKNULL FEATURES medv FROM Boston
    INSPECT ENCODING USING ONE-HOT ENCODING feature medv from boston
    INSPECT medv CHECKNULL FROM Boston;
    INSPECT medv DEDUPLICATE FROM Boston;
    INSPECT age CATEGORIZE INTO L1,L2,L3,L4 FROM Boston;
    
    New: Multiple operations in one query:
    INSPECT medv CHECKNULL, xyz DEDUPLICATE, age CATEGORIZE INTO l1, l2 FROM Boston;
    '''
    command_parts = [part for part in command.split(" ") if part.strip()]
    print(command_parts)
    
    try:
        # Check if this is a multi-operation query (contains commas)
        if ',' in command:
            return handle_multi_operations(command, command_parts)
        else:
            return handle_single_operation(command, command_parts)
    except Exception as e:
        print(f"Error in inspect: {e}")
        response = response_schema()
        response['query'] = command
        response['text'] = [f"Error processing command: {str(e)}"]
        return response

def handle_multi_operations(command, command_parts):
    """Handle multiple operations in a single INSPECT query"""
    try:
        # Extract dataset name using get_arg function
        dataset_name = get_dataset_name(command_parts)
        print(f"Dataset name: {dataset_name}")
        inspect_idx = [p.upper() for p in command_parts].index("INSPECT")
        from_idx = [p.upper() for p in command_parts].index("FROM")
        
        operations_part = ' '.join(command_parts[inspect_idx + 1:from_idx])
        
        operation_strings = [op.strip() for op in operations_part.split('|')]
        
        combined_response = response_schema()

        for i, op_string in enumerate(operation_strings):
            print(f"Processing operation {i+1}: {op_string}")
            
            # Create individual command for this operation
            individual_command = f"INSPECT {op_string} FROM {dataset_name};"
            
            # Process the individual operation
            result = handle_single_operation(individual_command, individual_command.split())
            print("hi ", result)
            # Combine results
            if result:
                # combined_response['operations'].append({
                #     'operation': op_string,
                #     'result': result
                # })
                if result.get('text'):
                    combined_response['text'].extend([f"Operation '{op_string}': {text}" for text in result['text']])
        print(combined_response)
        return combined_response
        
    except Exception as e:
        print(f"Error in handle_multi_operations: {e}")
        response = response_schema()
        response['query'] = command
        response['text'] = [f"Error processing multi-operations: {str(e)}"]
        return response

def handle_single_operation(command, command_parts):
    """Handle single operation INSPECT queries"""
    try:
        operation_types = ["CHECKNULL", "ENCODING", "DEDUPLICATE", "CATEGORIZE", "IMPUTE"]
        operation_type = next((word for word in operation_types if word.upper() in command.upper()), "") 
        dataset_name = get_arg(command_parts, "FROM", "").split(';')[0]
        features = get_arg(command_parts, "INSPECT", "")
          
    except Exception as e:
        print(f"Error parsing single operation: {e}")
        pass
    
    response = response_schema()
    response['query'] = command
    
    if operation_type.upper() == "CHECKNULL":
        response = checknull(dataset_name)
        return response
    elif operation_type.upper() == "ENCODING":
        res = encoding(dataset_name, command_parts)
        if res: 
            return res
        else:
            response['text'].append("Something wrong. try again")
            return response
    elif operation_type.upper() == "DEDUPLICATE":
        res = deduplicate(command_parts)
        if res:
            return res
        else:
            response['text'].append("Something wrong. try again")
            return response
    elif operation_type.upper() == "CATEGORIZE":
        res = categorize(dataset_name, command_parts)
        if res:
            return res
        else:
            response['text'].append("Something wrong. try again")
            return response
    elif operation_type.upper() == "IMPUTE":
        res = impute(dataset_name, command_parts)
        if res:
            return res
        else:
            response['text'].append("Something wrong. try again")
            return response
    
    return response
