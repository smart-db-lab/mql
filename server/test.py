import pandas as pd

# Example dataset
data = {
    "Make": ["Toyota", "Honda", "Toyota", "Ford", "Honda", "Ford"],
    # "Price Range": ["High", "Medium", "Low", "Medium", "Low", "High"],
    "Mileage": [50000, 60000, 30000, 70000, 40000, 80000],
    "Age": [5, 3, 7, 2, 4, 6],
    "Price": [15000, 18000, 12000, 20000, 17000, 22000]
}
df = pd.DataFrame(data)
print(df)
# Define the target variable
target_var = "Price"

# Define the categorical variable to be target encoded
cat_var = "Make"

grouped = df.groupby(cat_var)

# Iterating over the groups and printing them
for name, group in grouped:
    print(name)  # Print the name of the group (unique value of cat_var)
    print(group)  # Print the DataFrame corresponding to the group
    print('---------------')  #


# Calculate mean of target variable for each category
target_means = df.groupby(cat_var)[target_var].mean()
print(target_means)
# Map the mean values back to the original DataFrame
df[f"{cat_var}_encoded"] = df[cat_var].map(target_means)

# Drop the original categorical variable
df.drop(columns=[cat_var], inplace=True)
print (df)
# Display the DataFrame ready for linear regression
print("DataFrame ready for linear regression:")

# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error

# # Splitting the data into features and target variable
# X = df.drop(columns=["Price"])
# df.drop
# y = df["Price"]

# # Splitting the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Initializing and fitting the linear regression model
# model = LinearRegression()
# model.fit(X_train, y_train)

# # Predicting on the test set
# y_pred = model.predict(X_test)

# # Calculating the mean squared error
# mse = mean_squared_error(y_test, y_pred)
# print("Mean Squared Error:", mse)
