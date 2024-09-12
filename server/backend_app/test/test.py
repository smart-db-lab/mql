import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score,r2_score
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Input
from keras.optimizers import Adam

# # Load the data
# data = pd.read_csv('Iris.csv')

# # Check for missing values
# print(data.isnull().sum())

# # Dynamically identify categorical and numerical variables
# categorical_vars = data.select_dtypes(include=['object', 'category']).columns.tolist()
# numerical_vars = data.select_dtypes(include=['int64', 'float64']).columns.tolist()

# # Remove the target variable from the lists
# # numerical_vars.remove('Species')
# if 'Species' in categorical_vars:
#     categorical_vars.remove('Species')

# # Impute missing values
# # imputer_num = SimpleImputer(strategy='mean')
# # data[numerical_vars] = imputer_num.fit_transform(data[numerical_vars])

# # imputer_cat = SimpleImputer(strategy='most_frequent')
# # data[categorical_vars] = imputer_cat.fit_transform(data[categorical_vars])

# # Encode categorical variables
# encoder = OneHotEncoder(drop='first')
# encoded_features = encoder.fit_transform(data[categorical_vars]).toarray()
# encoded_features_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out())
# data = pd.concat([data.drop(categorical_vars, axis=1), encoded_features_df], axis=1)
# print(data)
# # Encode the target variable
# label_encoder = LabelEncoder()
# data['Species'] = label_encoder.fit_transform(data['Species'])

# # Scale numerical variables
# scaler = StandardScaler()
# data[numerical_vars] = scaler.fit_transform(data[numerical_vars])

# # Define features and target
# X = data.drop('Species', axis=1)
# y = data['Species']

# # Split data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Define and evaluate scikit-learn models
# models = {
#     'Logistic Regression': LogisticRegression(max_iter=200),
#     'Random Forest': RandomForestClassifier(random_state=42),
#     'Gradient Boosting': GradientBoostingClassifier(random_state=42)
# }

# results = {}
# for name, model in models.items():
#     model.fit(X_train, y_train)
#     y_pred = model.predict(X_test)
#     accuracy = accuracy_score(y_test, y_pred)
#     results[name] = accuracy
#     print(f'{name} Accuracy: {accuracy:.4f}')

# # PyTorch model
# class SimpleNN(nn.Module):
#     def __init__(self, input_dim):
#         super(SimpleNN, self).__init__()
#         self.fc1 = nn.Linear(input_dim, 128)
#         self.fc2 = nn.Linear(128, 64)
#         self.fc3 = nn.Linear(64, 3)  # 3 classes for Iris dataset

#     def forward(self, x):
#         x = torch.relu(self.fc1(x))
#         x = torch.relu(self.fc2(x))
#         x = self.fc3(x)
#         return x

# # Convert data to PyTorch tensors
# X_train_tensor = torch.tensor(X_train.to_numpy(), dtype=torch.float32)
# y_train_tensor = torch.tensor(y_train.to_numpy(), dtype=torch.long)  # Change to long for classification
# X_test_tensor = torch.tensor(X_test.to_numpy(), dtype=torch.float32)
# y_test_tensor = torch.tensor(y_test.to_numpy(), dtype=torch.long)

# # Create DataLoader
# train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
# test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
# train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
# test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# # Initialize the model, loss function, and optimizer
# input_dim = X_train.shape[1]
# model = SimpleNN(input_dim)
# criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(model.parameters(), lr=0.001)

# # Train the model
# n_epochs = 10
# for epoch in range(n_epochs):
#     model.train()
#     for X_batch, y_batch in train_loader:
#         optimizer.zero_grad()
#         outputs = model(X_batch)
#         loss = criterion(outputs, y_batch)
#         loss.backward()
#         optimizer.step()

# # Evaluate the model
# model.eval()
# correct = 0
# total = 0
# with torch.no_grad():
#     for X_batch, y_batch in test_loader:
#         outputs = model(X_batch)
#         _, predicted = torch.max(outputs.data, 1)
#         total += y_batch.size(0)
#         correct += (predicted == y_batch).sum().item()

# pytorch_accuracy = correct / total
# results['PyTorch NN'] = pytorch_accuracy
# print(f'PyTorch NN Accuracy: {pytorch_accuracy:.4f}')

# # TensorFlow model
# tf_model = Sequential([
#     Input(shape=(X_train.shape[1],)),
#     Dense(128, activation='relu'),
#     Dense(64, activation='relu'),
#     Dense(3, activation='softmax')  # 3 classes for Iris dataset
# ])

# # Compile the model
# tf_model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# print(X_train.shape,y_train.shape)
# # Train the model
# tf_model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# # Evaluate the model
# loss, accuracy = tf_model.evaluate(X_test, y_test)
# results['TensorFlow NN'] = accuracy
# print(f'TensorFlow NN Accuracy: {accuracy:.4f}')

# # Compare and determine the best model
# best_model_name = max(results, key=results.get)
# best_model_accuracy = results[best_model_name]
# print(f'Best Model: {best_model_name} with Accuracy: {best_model_accuracy:.4f}')

# # Example new data for prediction
# new_data = pd.DataFrame({
#     'sepal_length': [5.1],
#     'sepal_width': [3.5],
#     'petal_length': [1.4],
#     'petal_width': [0.2]
# })

# # Scale the new data
# new_data[numerical_vars] = scaler.transform(new_data[numerical_vars])

# # Make predictions
# if best_model_name in ['Logistic Regression', 'Random Forest', 'Gradient Boosting']:
#     prediction = models[best_model_name].predict(new_data)
#     predicted_class = label_encoder.inverse_transform(prediction)
# elif best_model_name == 'PyTorch NN':
#     new_data_tensor = torch.tensor(new_data.to_numpy(), dtype=torch.float32)
#     with torch.no_grad():
#         outputs = model(new_data_tensor)
#         _, predicted = torch.max(outputs.data, 1)
#         predicted_class = label_encoder.inverse_transform(predicted.numpy())
# elif best_model_name == 'TensorFlow NN':
#     prediction = tf_model.predict(new_data)
#     predicted_class = label_encoder.inverse_transform([np.argmax(prediction)])

# print(f'Predicted Species: {predicted_class[0]}')


class SimpleNN(nn.Module):
    def __init__(self, input_dim, output_dim, classification=False):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_dim)
        self.classification = classification

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        if self.classification:
            x = torch.softmax(x, dim=1)  # Use softmax for classification
        return x

def train_and_evaluate_torch(model, X_train, X_test, y_train, y_test, epochs=10, learning_rate=0.001, classification=False):
    # Select appropriate criterion
    criterion = nn.CrossEntropyLoss() if classification else nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Convert data to tensors
    X_train_tensor = torch.tensor(X_train.values, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train.values, dtype=torch.long if classification else torch.float32)
    X_test_tensor = torch.tensor(X_test.values, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test.values, dtype=torch.long if classification else torch.float32)
    
    # Debugging prints
    print(f"Shapes: X_train_tensor: {X_train_tensor.shape}, y_train_tensor: {y_train_tensor.shape}")
    print(f"Shapes: X_test_tensor: {X_test_tensor.shape}, y_test_tensor: {y_test_tensor.shape}")

    # Create DataLoader
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    # Training loop
    for epoch in range(epochs):
        model.train()
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            outputs = model(X_batch)
            # Debugging prints
            print(f"Epoch {epoch+1}, Batch shapes - X_batch: {X_batch.shape}, y_batch: {y_batch.shape}, outputs: {outputs.shape}")

            if classification:
                loss = criterion(outputs, y_batch)
            else:
                loss = criterion(outputs.squeeze(), y_batch)
            loss.backward()
            optimizer.step()

    # Evaluate the model
    model.eval()
    with torch.no_grad():
        y_pred_tensor = model(X_test_tensor)
        # Debugging prints
        print(f"Evaluation shapes - X_test_tensor: {X_test_tensor.shape}, y_test_tensor: {y_test_tensor.shape}, y_pred_tensor: {y_pred_tensor.shape}")

        if classification:
            y_pred = torch.argmax(y_pred_tensor, dim=1).numpy()
        else:
            y_pred = y_pred_tensor.numpy().flatten()

        # Compute R² score or accuracy
        if classification:
            accuracy = accuracy_score(y_test, y_pred)
            print(f"Accuracy: {accuracy}")
            return y_pred, accuracy
        else:
            r2 = r2_score(y_test, y_pred)
            print(f"R² Score: {r2}")
            return y_pred, r2

# Example Usage
# from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset and preprocess
feature_names=["age","rad"]
data = pd.read_csv("Boston.csv")
X = data[feature_names]
y = data["medv"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert to DataFrame for compatibility with the function
X_train = pd.DataFrame(X_train)
X_test = pd.DataFrame(X_test)
X_train_tensor = torch.tensor(X_train.values, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.long )
X_test_tensor = torch.tensor(X_test.values, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.long )


# Instantiate the model
input_dim = X_train.shape[1]
output_dim = 1  # Regression task
print(y_train.shape)
print("in input output dm",X_train.shape[1], len(np.unique(y_train)))

model = SimpleNN(input_dim, output_dim, classification=False)

# Train and evaluate
train_and_evaluate_torch(model, X_train, X_test, y_train, y_test, epochs=10, learning_rate=0.001, classification=False)
