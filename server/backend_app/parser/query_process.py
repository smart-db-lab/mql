import os
import re
from sqlalchemy import create_engine
from .operation.query_manipulate import Query_manipulate
from .Function.Show_db import show_db
from .operation.Simple_Generate import simple_generate
from .operation.Generate import generate
from .operation.Inspect import inspect
from .operation.Construct import construct
from .operation import *
from .Function.Imputer import impute
from .operation.Temp_Generate import temp_generate
def query_process(data):
    response = {}
    data_upper = data.upper()
    print(data,"**************")
    if data_upper.startswith("SHOW"):
        yield show_db(data)
    elif data_upper.startswith("CONSTRUCT"):
        '''CONSTRUCT PREDICTION MonthlySales ALGORITHM GB WITH  LABEL ProductID FEATURES Age Price StockLevel FROM retail OVER retailTestData ;
           CONSTRUCT CLASSIFICATION Species ALGORITHM KNN WITH  LABEL ProductID FEATURES SepalLengthCm SepalWidthCm FROM Iris ;
        '''
        yield construct(data)

    elif data_upper.startswith("GENERATE"):
        '''GENERATE DISPLAY OF PREDICTION MonthlySales ALGORITHM GB WITH ACCURACY 100 LABEL ProductID FEATURES Age Price StockLevel FROM retail OVER retailTestData ;
           GENERATE DISPLAY OF CLASSIFICATION Species ALGORITHM KNN WITH ACCURACY 100 LABEL ProductID FEATURES SepalLengthCm SepalWidthCm FROM Iris ;
        '''
        if " BEST ALGORITHM " in data_upper:
            print("in generate")
            yield generate(data)
        else:
            print("in simple generate")
            yield temp_generate(data)

    elif data_upper.startswith("INSPECT"):
        '''
            INSPECT CHECKNULL FEATURES medv FROM Boston
            INSPECT ENCODING USING ONE-HOT ENCODING feature medv from boston
        '''
        yield inspect(data)

    elif data_upper.startswith("IMPUTE"):
        '''
            IMPUTE medv FROM Boston;
            IMPUTE * FROM Boston;
        '''
        yield impute(data)

    else:
        query = f'{data};'
        yield Query_manipulate(query)
    