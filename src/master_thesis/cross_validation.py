# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.metrics import f1_score

# # Load the dataset
# file_path = 'data/final_cm_ic1_ss1.csv'  # Replace with your file path
# data = pd.read_csv(file_path)

# # Preparing the data
# X = data.drop(columns=['curr_service', 'hadm_id', 'Unnamed: 0'])  # Features (distance matrix)
# y = data['curr_service']  # Target variable

# # Splitting the data into training and validation sets
# X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# # Range of k values to test
# k_values = range(1, 11)  # Testing k values from 1 to 10

# # Dictionary to store the weighted F-scores for each k value
# f_scores = {}

# # Training and evaluating the model for each k value
# for k in k_values:
#     # Create and train the k-NN classifier
#     knn = KNeighborsClassifier(n_neighbors=k)
#     knn.fit(X_train, y_train)

#     # Predicting on the validation set
#     y_pred = knn.predict(X_val)

#     # Calculating weighted F-score
#     f_score = f1_score(y_val, y_pred, average='weighted')
#     f_scores[k] = f_score

# # Extracting the top 5 k values and their corresponding scores
# top_5_k_values = sorted(f_scores, key=f_scores.get, reverse=True)[:5]
# top_5_scores = {k: f_scores[k] for k in top_5_k_values}

# # Displaying the top 5 k values and their scores
# print("Top 5 k values and their Weighted F-scores:")
# for k in top_5_scores:
#     print(f"k = {k}: Score = {top_5_scores[k]}")

# ================

from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import make_scorer, f1_score
import numpy as np
import pandas as pd

# Load the provided data file
file_path = 'data/final_cm_ic1_ss1.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the data for an overview
# data.head()

# Preparing the dataset
X = data.drop(['Unnamed: 0', 'hadm_id', 'curr_service'], axis=1)
y = data['curr_service']

# Define a range of k values to test
k_values = range(1, 21)

# We will use Stratified K-Fold to maintain the proportion of each class in each fold
cv = StratifiedKFold(n_splits=5)

# Dictionary to store the average weighted F1 scores for each k value
f1_scores = {}

for k in k_values:
    # Create KNN model
    model = KNeighborsClassifier(n_neighbors=k)

    # Calculate cross-validated weighted F1 score for each k
    scores = cross_val_score(model, X, y, cv=cv, scoring=make_scorer(f1_score, average='weighted'))
    
    # Store the average F1 score
    f1_scores[k] = np.mean(scores)

# Sort the results by best performance
sorted_f1_scores = sorted(f1_scores.items(), key=lambda x: x[1], reverse=True)

# Displaying the best k values based on F1 score
sorted_f1_scores[:5]  # Display top 5 k values and their scores

