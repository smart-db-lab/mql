import json
import os
from openai import OpenAI

generate_query_system_message = \
"""
GENERATE [DISPLAY OF]
PREDICTION v | CLASSIFICATION INTO C | CLUSTERING
[USING MODEL ModelName | ALGORITHM AlgorithmName]
[WITH ACCURACY P]
[LABEL B1, B2, ..., Bm]
FEATURES A1, A2, ..., An
FROM r1, r2, ..., rq
WHERE c
OVER s

Components Explained:

1. GENERATE [DISPLAY OF]
   - GENERATE: Initiates a query for machine learning operations.
   - [DISPLAY OF]: Optional. Specifies that the output should include a visual display or detailed format of the results.

2. PREDICTION v | CLASSIFICATION INTO C | CLUSTERING
   - PREDICTION v: Performs a prediction task for the target variable v.
   - CLASSIFICATION C: C is a column in the dataset.
   - For classification one feature column will we add in MQL
   - for CLUSTERING Example: 
      - GENERATE DISPLAY OF CLUSTERING ALGORITHM KMeans FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ;
      - GENERATE DISPLAY OF CLUSTERING WITH CLUSTER OF 3 ALGORITHM KMeans FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ;
      - Means where will be only CLUSTERING or CLUSTERING with CLUSTER OF *number of cluster* 

3. [USING MODEL ModelName(only use when model name is given) | ALGORITHM AlgorithmName (KMeans|KNN|LR)]
   - One of the two option will be exist
   - [USING MODEL ModelName]: Optional. Specifies a pre-defined model by name to be used for the ML operation.
   - only use when model name is given
   - [ALGORITHM AlgorithmName]: Optional. Directs the query to use a specific algorithm for creating the model.
   - AlgorithmName choice are: KMeans|KNN|LR

4. [WITH ACCURACY P]
   - [WITH ACCURACY P]: Optional. Sets a threshold for accuracy (or other performance metrics).
   - This filed is optional

6. FEATURES A1,A2,...,An
   - FEATURES: Lists the features or input variables used by the model.
   - This will the column list from the dataset
   - if there is space in column/feature name keep it as it is
   - between two column name there will be no space A 1,A 2
   - If FEATURES is mention and given, don't change the column names from user query

7. FROM r1, r2, ..., rq
   - FROM: Specifies the dataset(s) or table(s) from which the data for the ML task is sourced.
   - This will be primary dataset name which will be used for training

8. WHERE c
   - WHERE: Provides conditions or filters that refine the selection of data.
   - Let's not add this in any MQL
9. OVER s
   - OVER: Defines an additional dataset on which the ML model is applied.
   - This is the secondary dataset which is used for test

"""

constract_query_system_message = \
"""
CONSTRUCT ModelName AS [SUPERVISED | UNSUPERVISED]
FOR PREDICTION | CLASSIFICATION | CLUSTERING
[USING AlgorithmName]
[WITH ACCURACY P]
TRAIN ON N TEST ON M
FEATURES A1, A2, ..., An
FROM r1, r2, ..., rn
WHERE c

Components Explained:

1. CONSTRUCT ModelName
   - CONSTRUCT: Initiates the creation of a new machine learning model.
   - ModelName: Specifies the name for the newly created model.

2. AS [SUPERVISED | UNSUPERVISED]
   - AS: Defines the type of learning.
   - [SUPERVISED | UNSUPERVISED]: Chooses between supervised learning, where the model learns from labeled data, or unsupervised learning, which does not require labeled data.

3. FOR PREDICTION | CLASSIFICATION | CLUSTERING
   - FOR: Specifies the intended use of the model.
   - PREDICTION: Indicates the model is designed to predict continuous outcomes.
   - CLASSIFICATION: Indicates the model is designed to classify input data into predefined categories.
   - CLUSTERING: Indicates the model is designed to group a set of objects in such a way that objects in the same group are more similar to each other than to those in other groups.

4. [USING AlgorithmName]
   - [USING AlgorithmName]: Optional. Specifies the algorithm to be used in model construction, such as 'Random Forest', 'SVM', etc.

5. [WITH ACCURACY P]
   - [WITH ACCURACY P]: Optional. Sets a performance threshold for the model, such as a minimum accuracy or other metrics, that the training process aims to achieve.

6. TRAIN ON N TEST ON M
   - TRAIN ON N: Specifies the number of data instances or percentage of the dataset to use for training the model.
   - TEST ON M: Specifies the number of data instances or percentage of the dataset to use for testing the model.

7. FEATURES A1, A2, ..., An
   - FEATURES: Lists the features or variables used to train the model. Each feature corresponds to a column in the dataset that provides data relevant to the learning task.

8. FROM r1, r2, ..., rn
   - FROM: Specifies the dataset(s) or table(s) from which the data for constructing the model is sourced.

9. WHERE c
   - WHERE: Provides conditions or filters that refine the selection of data used for model training and testing.
"""

inspect_query_system_message = \
"""
INSPECT A1, A2, ..., Am
[CATEGORIZE INTO L1, L2, ..., Lx |
IMPUTE | NUMERIZE AS E | DEDUPLICATE]
[, B1, B2, ..., Bk [CATEGORIZE INTO L1, L2, ..., Lx |
IMPUTE | NUMERIZE AS E | DEDUPLICATE] ...]
FROM r1, r2, ..., rn
WHERE c

Components Explained:

1. INSPECT A1, A2, ..., Am
   - INSPECT: Initiates an operation to examine or modify data within the dataset.
   - A1, A2, ..., Am: Specifies the columns in the dataset to be inspected and potentially modified.

2. [CATEGORIZE INTO L1, L2, ..., Lx | IMPUTE | NUMERIZE AS E | DEDUPLICATE]
   - [CATEGORIZE INTO L1, L2, ..., Lx]: Optional. Assigns data into predefined categories L1, L2, ..., Lx.
   - [IMPUTE]: Optional. Fills in missing values within the specified columns using statistical methods.
   - [NUMERIZE AS E]: Optional. Converts categorical data into numerical format, potentially with encoding specified by E.
   - [DEDUPLICATE]: Optional. Removes duplicate entries from the data in specified columns.

3. [, B1, B2, ..., Bk [CATEGORIZE INTO L1, L2, ..., Lx | IMPUTE | NUMERIZE AS E | DEDUPLICATE] ...]
   - B1, B2, ..., Bk: Additional columns that may undergo similar data manipulation processes as A1, A2, ..., Am.
   - The operations listed can be applied in the same manner to these additional columns.

4. FROM r1, r2, ..., rn
   - FROM: Specifies the dataset(s) or table(s) from which the data is sourced for inspection.

5. WHERE c
   - WHERE: Provides conditions or filters that refine the selection of data to be inspected or modified. This clause allows the INSPECT operation to focus on specific subsets of the data based on the conditions provided.

This detailed guide helps in understanding how to use the INSPECT statement in MQL for data preprocessing tasks such as categorization, imputation, numerization, and deduplication directly within the database environment. This capability is crucial for preparing data for further analysis or machine learning tasks.
"""

example_of_mql = \
"""
##construct 
CONSTRUCT KMeans_Boston AS UNSUPERVISED FOR CLUSTERING  FEATURES age,rad ALGORITHM KMeans WITH CLASS 5 FROM Boston;

CONSTRUCT LR_Boston AS SUPERVISED FOR PREDICTION on TARGET medv FEATURES age,rad ALGORITHM LR  TEST ON .3 FROM Boston; 

CONSTRUCT KNN_Combined AS SUPERVISED FOR CLASSIFICATION on TARGET Class FEATURES CAtomCount,TotalAtomCount,HAtomCount ALGORITHM KNN  TEST ON .3 FROM combined;

CONSTRUCT LR_Combined AS SUPERVISED FOR PREDICTION on TARGET Epsilon FEATURES CAtomCount,TotalAtomCount,HAtomCount ALGORITHM LR  TEST ON .3 FROM combined;

CONSTRUCT LR_retail AS SUPERVISED FOR PREDICTION on TARGET MonthlySales FEATURES Age,Price,StockLevel ALGORITHM LR  TEST ON .3 FROM retail;

##generate

#cluster
GENERATE DISPLAY OF CLUSTERING ALGORITHM KMeans FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ;
GENERATE DISPLAY OF CLUSTERING WITH CLUSTER OF 3 ALGORITHM KMeans FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ;

GENERATE DISPLAY OF CLUSTERING WITH CLUSTER OF 3 USING MODEL KMeans_Boston FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ;

#classificaarion
GENERATE  CLASSIFICATION Class ALGORITHM KNN WITH ACCURACY 0 LABEL ProductID FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ;
GENERATE  DISPLAY OF CLASSIFICATION Class ALGORITHM KNN WITH ACCURACY 0 LABEL ProductID FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ;

GENERATE  CLASSIFICATION Class USING MODEL KNN_Combined WITH ACCURACY 0 LABEL ProductID FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ;



#prediction
GENERATE DISPLAY OF PREDICTION Epsilon ALGORITHM LR WITH R-SQUARED 0 LABEL serialNo FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ;
GENERATE DISPLAY OF PREDICTION Epsilon USING MODEL LR_Combined  WITH R-SQUARED 0 LABEL serialNo FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ;

GENERATE DISPLAY OF PREDICTION MonthlySales ALGORITHM LR WITH R-SQUARED 0 LABEL serialNo FEATURES Age,Price,StockLevel FROM retail OVER retailTestData ;
GENERATE DISPLAY OF PREDICTION MonthlySales USING MODEL LR_retail WITH R-SQUARED 0 LABEL serialNo FEATURES Age,Price,StockLevel FROM retail OVER retailTestData ;

GENERATE DISPLAY OF PREDICTION medv ALGORITHM LR WITH ACCURACY 0 LABEL serialNo FEATURES age,rad FROM  Boston ;
GENERATE DISPLAY OF PREDICTION medv USING MODEL LR_Boston WITH R-SQUARED 0 LABEL serialNo FEATURES age,rad FROM  Boston ;


#auto ml
GENERATE DISPLAY OF PREDICTION medv  LABEL serialNo FEATURES age,rad FROM  Boston ;

 CONSTRUCT LR_retail AS SUPERVISED FOR PREDICTION on TARGET MonthlySales FEATURES Age,Price,StockLevel TEST ON .3 FROM retail;

GENERATE  CLASSIFICATION Class  WITH ACCURACY 0 LABEL ProductID FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ;


## Inspect 

#CHECKNULL

INSPECT CHECKNULL FEATURES medv FROM Boston;
#ENCODING

INSPECT ENCODING USING Ordinal ENCODING FEATURE Species FROM Iris;
INSPECT ENCODING USING One-Hot ENCODING FEATURE Species FROM Iris;
INSPECT ENCODING USING Label ENCODING FEATURE Species FROM Iris;
INSPECT ENCODING USING TARGET ENCODING FEATURE Species  TARGET-FEATURE SepalLengthCm FROM Iris;

#DEDUPLICATE
INSPECT * DEDUPLICATE FROM Boston;
INSPECT medv DEDUPLICATE FROM Boston;

#IMPUTE
IMPUTE *  FROM BostonMiss;
IMPUTE indus FROM BostonMiss;
"""


def get_system_message(dataset_name, column_list):
   original_system_message = f"""Here you will work as a Machine Learning Query Language (MQL) 
   generator. The examples and details are provided {generate_query_system_message} 
   {constract_query_system_message} {inspect_query_system_message}. 
   You will read user input and understand what they need. 
   You will try to extract information from the user query and 
   construct an MQL with it. You will only return one MQL.
   You consider this dataset name {dataset_name} for this query
   Please consider these columns: {column_list}
   ** You will return only MQL noting else string **
   ** Add a field if it met from the MQL criteria from the user question **
   ** Don't add any field which is not given in the user question **
   ** algorithm or model name is required filed **
   ** If FEATURES is mention and given, don't change the column names from user query**
   Model or algorithm will be mentioned in the query. If no them try to choose from algorithm KMeans|KNN|LR
   Example MQL:
   1. r
   Query: generate a predication for Epsilon feature with linear regression algorithm from combined dataset. Use label as serialNo
   MQL: GENERATE DISPLAY OF PREDICTION Epsilon ALGORITHM LR WITH R-SQUARED 0 LABEL serialNo FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined;
   short description: here we understand the this is a PREDICTION for Epsilon column with LR(linear regression) algorithm. label mean a column to uniquely identify each record

   **More Example are given here**

    """

   return original_system_message


mql_conversation_tools = [{
    "type": "function",
    "function": {
        "name": "get_mql_query",
        "description": "Get the mql query based on the user input",
        "parameters": {
            "type": "object",
            "properties": {
                "mql_query": {
                    "type": "string",
                    "description": "Just the MQL query, Nothing else"
                }
            },
            "required": [
                "mql_query"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}]


def extract_mql_query(completion):
    tool_call = completion.choices[0].message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    mql_query = args['mql_query']

    return mql_query


def convert_nl_to_mql(question, file_name, data_frame):
    # file_name,_= os.path.splitext(csv_file.name)
    column_list = data_frame.columns.tolist()
    system_message = get_system_message(file_name, column_list)
    client = OpenAI(api_key=os.getenv('OPENAI_KEY'))

    completion = client.chat.completions.create(
        model="gpt-4o-2024-11-20",
        temperature=0,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": question}
        ],
        tools=mql_conversation_tools,
        tool_choice='required'
    )

    mql_query = extract_mql_query(completion)

    return mql_query