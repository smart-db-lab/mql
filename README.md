# Machine Learning Query Language (MQL) 
Implemention of a Declarative Query Language for High Level Machine Learning Application Design 

## Technology used
- Python 3.11 (required)
- JAVA runtime
- ReactJS
- Django rest framework
- PostgreSQL
- OS : Linux (to perform autosklearn)

## To run the application
firstly clone this repositoroy by 
```
git clone "https://github.com/smart-db-lab/mql.git"
```

**for database setup:** 
- install postgresql and login
- create a postgres database 
<!-- using command prompt <**psql**>  -->
<!-- - required information
```
Server [localhost]: localhost
Database [postgres]: postgres
Port [5432]: 5432
Username [postgres]: postgres
Password for user postgres:  <your_assigned_password>

``` -->
- install mysql and login
- create a mysql database 
<!-- -Create a database as your desired name [e.g. mydatabase]


```
create database mydatabase;
``` -->
<!-- for example
```
        create database demo1;
``` -->


### Setup environment variable
- Create a file with name **.env** in the server folder where **.env.example file appear**
- paste all variable from **.env.example** to the created **.env** file and replace your credentials with the variable name.
<!-- ```
POSTGRES_URL = postgresql://myuser:mypassword@localhost:5432/mydatabase
DATABASE_URL = postgresql://myuser:mypassword@localhost:5432/
   
```
 for example
```
POSTGRES_URL = postgresql://postgres:1234@localhost:5432/demo1
DATABASE_URL = postgresql://postgres:1234@localhost:5432/

``` -->
<!-- - Keep running database connection -->
To migrate database schema:
```
    python manage.py migrate
```
To run Frontend:
```
    cd client
    npm install
    npm  run dev
```
To run Backend: 
```
    cd server
    pip install -r requirements.txt
    python manage.py runserver
```
Also install Java ( openjdk ) runtime environment. [It is required to run h2o automl package]

### All done?
- Now keep running frontend, backend and databases. go to the application. [e.g. https://localhost:5173]
- create account and login then switch to operation tab to perform query.

### Traditional machine learning using python 

```python
        import pandas as pd
        from sklearn.model_selection import train_test_split 
        from sklearn.linear_model import LogisticRegression 
        from sklearn.metrics import accuracy_score 
        # 1. Load data (downloaded from Kaggle and saved as 'train.csv') 
        df = pd.read_csv('./train.csv') 
        # 2. Basic preprocessing: select a few features and fill missing ages 
        features = ['Pclass', 'Sex', 'Age', 'Fare']

        df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
        df['Age'].fillna(df['Age'].median(), inplace=True) 
        X = df[features] 
        y = df['Survived'] 
        # 3. Split into train/test sets 
        X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=42 ) 
        # 4. Train a logistic regression model 

        model = LogisticRegression(max_iter=200) 
        model.fit(X_train, y_train) 
        # 5. Evaluate 
        y_pred = model.predict(X_test) 
        acc = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {acc:.2f}')

```
Output 

```
        Accuracy: 0.80
```
### MQL Query 
#### INSPECT statement 
```
        INSPECT Sex ENCODING METHOD Ordinal FROM train;
        INSPECT Age IMPUTE USING STRATEGY median FROM train;


```

#### GENERATE Statement
```
        GENERATE  DISPLAY OF CLASSIFICATION Survived ALGORITHM LOG LABEL RecordID FEATURES Pclass,Sex,Age,Fare FROM train;

```
## Output of MQL Query: 

![MQL Report](./mql_report.png)

If the image does not display, [download it here](./mql_report.png).

## Examples of MQL query

<!-- ## Construct 

```
        CONSTRUCT KMeans_Boston AS UNSUPERVISED FOR CLUSTERING  FEATURES age,rad ALGORITHM KMeans WITH CLASS 5 FROM Boston;

        CONSTRUCT LR_Boston AS SUPERVISED FOR PREDICTION on TARGET medv FEATURES age,rad ALGORITHM LR  TEST ON .3 FROM Boston; 

        CONSTRUCT KNN_Combined AS SUPERVISED FOR CLASSIFICATION on TARGET Class FEATURES CAtomCount,TotalAtomCount,HAtomCount ALGORITHM KNN  TEST ON .3 FROM combined;

        CONSTRUCT LR_Combined AS SUPERVISED FOR PREDICTION on TARGET Epsilon FEATURES CAtomCount,TotalAtomCount,HAtomCount ALGORITHM LR  TEST ON .3 FROM combined;

        CONSTRUCT LR_retail AS SUPERVISED FOR PREDICTION on TARGET MonthlySales FEATURES Age,Price,StockLevel ALGORITHM LR  TEST ON .3 FROM retail;
``` -->
## Generate

### Cluster

        GENERATE DISPLAY OF CLUSTERING ALGORITHM KMeans FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ;

![MQL Report](./all_report/output-1-report.pdf)

If the image does not display, [download it here](./all_report/output-1-report.pdf).

        GENERATE DISPLAY OF CLUSTERING ALGORITHM KMeans FEATURES  Pclass,Sex,Age,Fare FROM train;


        GENERATE DISPLAY OF CLUSTERING ALGORITHM KMeans FEATURES  age,rad FROM Boston;
```
        GENERATE DISPLAY OF CLUSTERING ALGORITHM KMeans FEATURES  PetalLengthCm,PetalWidthCm FROM Iris;
```        
![MQL Report](./all_report/output-2-report.pdf)

If the image does not display, [download it here](./all_report/output-2-report.pdf).

<!-- GENERATE DISPLAY OF CLUSTERING WITH CLUSTER OF 3 ALGORITHM KMeans FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ; -->

<!-- GENERATE DISPLAY OF CLUSTERING WITH CLUSTER OF 3 USING MODEL KMeans_Boston FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ; -->


### Classification

        GENERATE  CLASSIFICATION Class ALGORITHM KNN  LABEL ProductID FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ;

![MQL Report](./all_report/output-3-report.pdf)
If the image does not display, [download it here](./all_report/output-3-report.pdf).

        GENERATE  DISPLAY OF CLASSIFICATION Survived ALGORITHM LOG LABEL RecordID FEATURES Pclass,Sex,Age,Fare FROM train;

![MQL Report](./all_report/output-4-report.pdf)
If the image does not display, [download it here](./all_report/output-4-report.pdf).


        GENERATE  CLASSIFICATION Species ALGORITHM KNN WITH ACCURACY 0 LABEL ProductID FEATURES SepalLengthCm,PetalLengthCm,PetalWidthCm FROM Iris ;

![MQL Report](./all_report/output-5-report.pdf)
If the image does not display, [download it here](./all_report/output-5-report.pdf).

<!-- GENERATE  DISPLAY OF CLASSIFICATION Class ALGORITHM KNN WITH ACCURACY 0 LABEL ProductID FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ;

        GENERATE  CLASSIFICATION Class USING MODEL KNN_Combined WITH ACCURACY 0 LABEL ProductID FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ; -->
        


### Prediction

 
        GENERATE DISPLAY OF PREDICTION Epsilon ALGORITHM LR LABEL serialNo FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ;

![MQL Report](./all_report/output-6-report.pdf)
If the image does not display, [download it here](./all_report/output-6-report.pdf).

<!-- GENERATE DISPLAY OF PREDICTION Epsilon USING MODEL LR_Combined  WITH R-SQUARED 0 LABEL serialNo FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ; -->

<!-- GENERATE DISPLAY OF PREDICTION MonthlySales ALGORITHM LR WITH R-SQUARED 0 LABEL serialNo FEATURES Age,Price,StockLevel FROM retail OVER retailTestData ;
        GENERATE DISPLAY OF PREDICTION MonthlySales USING MODEL  LR_retail WITH R-SQUARED  -10 LABEL serialNo FEATURES Age,Price,StockLevel FROM retail OVER retailTestData ;  -->

        GENERATE DISPLAY OF PREDICTION medv ALGORITHM LR WITH ACCURACY 0 LABEL serialNo FEATURES age,rad FROM  Boston WHERE age>50 ;
![MQL Report](./all_report/output-8-report.pdf)
If the image does not display, [download it here](./all_report/output-8-report.pdf).


<!--        GENERATE DISPLAY OF PREDICTION medv USING MODEL LR_Boston LABEL serialNo FEATURES age,rad FROM  Boston ; -->

        GENERATE  CLASSIFICATION Species ALGORITHM KNN LABEL ProductID FEATURES SepalLengthCm,PetalLengthCm,PetalWidthCm FROM Iris ;
![MQL Report](./all_report/output-7-report.pdf)
If the image does not display, [download it here](./all_report/output-7-report.pdf).
<!-- 
        GENERATE DISPLAY OF PREDICTION medv USING MODEL LR_Boston WITH R-SQUARED 0 LABEL serialNo FEATURES age,rad FROM  Boston ;
         -->

<!-- ## Auto ML

        GENERATE DISPLAY OF PREDICTION medv  LABEL serialNo FEATURES age,rad FROM  Boston ;

        CONSTRUCT LR_retail AS SUPERVISED FOR PREDICTION on TARGET MonthlySales FEATURES Age,Price,StockLevel TEST ON .3 FROM retail;

        GENERATE  CLASSIFICATION Class  WITH ACCURACY 0 LABEL ProductID FEATURES CAtomCount,TotalAtomCount,HAtomCount FROM combined ; -->


## Inspect 

#### CHECKNULL
   
        INSPECT medv CHECKNULL  FROM Boston;
        INSPECT Survived CHECKNULL  FROM train;
        INSPECT species CHECKNULL  FROM Iris;


#### ENCODING
   

        INSPECT Species ENCODING METHOD Ordinal FROM Iris;
        INSPECT Survived ENCODING METHOD One-Hot FROM train;
        
<!-- INSPECT Species ENCODING METHOD One-Hot FROM Iris;
        INSPECT Species ENCODING METHOD Label FROM Iris; -->
<!-- INSPECT Species  ENCODING METHOD TARGET TARGET-FEATURE SepalLengthCm FROM Iris; -->
    
#### DEDUPLICATE

        INSPECT * DEDUPLICATE FROM Boston;
        INSPECT medv DEDUPLICATE FROM Boston;
      

#### CATEGORIZE

        INSPECT age CATEGORIZE INTO L1,L2,L3,L4 FROM Boston;
        INSPECT age CATEGORIZE INTO L1,L2,L3,L4 FROM train;
        INSPECT PetalLengthCm CATEGORIZE INTO L1,L2,L3,L4 FROM Iris;
### Combined INSPECT operation
        INSPECT medv checknull | medv deduplicate | age categorize INTO l1,l2 FROM  Boston;
#### Show datset 
        SHOW Customers;
#### Drop datset table
        DROP DATASET Customers;
## IMPUTE
        INSPECT indus IMPUTE USING STRATEGY mean FROM Boston;
        INSPECT * IMPUTE  FROM Boston;
       
## Composite 
```
        GENERATE DISPLAY OF PREDICTION medv ALGORITHM LR WITH ACCURACY 0 LABEL serialNo FEATURES age,rad FROM  Boston  WHERE INSPECT age CATEGORIZE INTO L1,L2,L3,L4 FROM Boston;
![MQL Report](./all_report/output-9-report.pdf)
If the image does not display, [download it here](./all_report/output-9-report.pdf).



        GENERATE  DISPLAY OF CLASSIFICATION Survived ALGORITHM LOG WITH ACCURACY 0 LABEL RecordID FEATURES Pclass,Sex,Age,Fare FROM train WHERE INSPECT * IMPUTE USING STRATEGY mean FROM train;
![MQL Report](./all_report/output-10-report.pdf)
If the image does not display, [download it here](./all_report/output-10-report.pdf).

```        

<!--
        GENERATE DISPLAY OF PREDICTION Extinction_Coefficient USING MODEL XYZ  WITH R-SQUARED 0 LABEL serialNo FEATURES * FROM dyeDesign OVER dyeDesignTest 
        WHERE 
        CONSTRUCT XYZ AS SUPERVISED FOR PREDICTION on TARGET Extinction_Coefficient FEATURES CAtomCount,TotalAtomCount,HAtomCount ALGORITHM LR  TEST ON .3 FROM dyeDesign 
        BASED ON 
        INSPECT Class ENCODING METHOD Ordinal FROM dyeDesign;
```
        GENERATE DISPLAY OF PREDICTION Epsilon USING MODEL predictExtinction  WITH ACCURACY 0 LABEL moleculeNo FEATURES * FROM dyeDesign OVER predicted_epsilon WHERE
        CONSTRUCT predictExtinction AS SUPERVISED FOR PREDICTION on TARGET Epsilon FEATURES * ALGORITHM RF  TEST ON .3 FROM dyeDesign 
        BASED ON 
        INSPECT Class ENCODING METHOD Ordinal FROM dyeDesign;
```  -->
## SQL query 

        SELECT * FROM "Iris";


## Available ML Algorithms

| Algorithm Type | Algorithm query; Code | Full Name |
|---|---|---|
| **Prediction** | LR | Linear Regression |
| | RF | Random Forest Regressor |
| | KNN | K-Neighbors Regressor |
| | SVR | Support Vector Regressor |
| | GBR | Gradient Boosting Regressor |
| **Classification** | LOG | Logistic Regression |
| | RFC | Random Forest Classifier |
| | KNN | K-Neighbors Classifier |
| | SVC | Support Vector Classifier |
| | GBC | Gradient Boosting Classifier |
| **Clustering** | KMEANS | K-Means Clustering |
| | AGGLOMERATIVE | Agglomerative Clustering |
| | DBSCAN | DBSCAN Clustering |

<!--    AgglomerativeClustering
            DBSCAN -->
<!-- &
        Best algorthm selection using AutoML
-->



## Important Notes and Cautions

⚠️ **Feature Naming Guidelines:**
- Features in FEATURES clause must be comma-separated with **no spaces** between feature names
- If a feature name contains spaces, enclose it in **double quotes** (`"`)
- Example: `FEATURES age,income,"annual salary","job title"`
- Incorrect: `FEATURES age, income, annual salary` (spaces after commas and unquoted space-containing names)
- Correct: `FEATURES age,income,"annual salary"`

⚠️ **General Syntax Cautions:**
- Database and table names are case-sensitive
- Algorithm codes must be in uppercase (e.g., `LR`, `KNN`, `LOG`)
- Column names must match exactly as they appear in your database

- Ensure your database connection is active before running queries






