import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
import joblib

np.random.seed(42)
n_samples = 5000

incomes = np.random.randint(20000,200000, n_samples)
existing_emis = incomes * np.random.uniform(0,0.4, n_samples)
credit_scores = np.random.randint(300, 900, n_samples)
dependents = np.random.randint(0,6, n_samples)
employment_years  = np.random.randint(0,20, n_samples)

true_safe_emis = []
for i in range(n_samples):
    base_capacity = (incomes[i] *0.5) - existing_emis[i]

    if credit_scores[i] <600:
        base_capacity*=0.4

    elif credit_scores[i]>= 700:
        base_capacity *= 1.2

    if dependents[i] > 2:
        base_capacity -=(dependents[i] * 2000)

    if employment_years[i] > 5:
        base_capacity +=3000

    true_safe_emis.append(max(0, base_capacity))

X = pd.DataFrame({'monthly_income': incomes,
    'existing_emi': existing_emis,
    'credit_score': credit_scores,
    'dependents': dependents,
    'employment_years': employment_years})

y = np.array(true_safe_emis)

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2, random_state = 42)

print('Training the MLPRegressor(Neural Network)...')
pipeline = Pipeline([('scaler', StandardScaler()), ('mlp', MLPRegressor(hidden_layer_sizes= (64, 32), activation = 'relu', max_iter = 1000, random_state = 42))])

pipeline.fit(X_train, y_train)

accuracy = pipeline.score(X_test, y_test)
print(f"Model R2 Score (Accuracy): {accuracy * 100:.2f}%")

os.makedirs('models', exist_ok = True)
joblib.dump(pipeline, 'models/loan_model.joblib')
print('Model saved successfully to models/loan_model.joblib')