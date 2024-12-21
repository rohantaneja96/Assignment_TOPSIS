# -*- coding: utf-8 -*-
"""102203515.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mInZddYIareutpezW0L64-xpP9qtxREy
"""

!pip install pandas numpy openpyxl

import pandas as pd
data = pd.read_excel('data.xlsx')
print(data.head())

import numpy as np


def topsis(data, weights, impacts):

    for i in range(1, len(data.columns)):
        column = data.iloc[:, i]
        norm = np.sqrt(sum(column**2))
        data.iloc[:, i] = column / norm


    for i in range(1, len(data.columns)):
        data.iloc[:, i] = data.iloc[:, i] * weights[i - 1]


    ideal_best = []
    ideal_worst = []
    for i in range(1, len(data.columns)):
        if impacts[i - 1] == "+":
            ideal_best.append(max(data.iloc[:, i]))
            ideal_worst.append(min(data.iloc[:, i]))
        else:
            ideal_best.append(min(data.iloc[:, i]))
            ideal_worst.append(max(data.iloc[:, i]))


    distances_best = []
    distances_worst = []
    for i in range(len(data)):
        distances_best.append(np.sqrt(sum((data.iloc[i, 1:] - ideal_best) ** 2)))
        distances_worst.append(np.sqrt(sum((data.iloc[i, 1:] - ideal_worst) ** 2)))


    scores = []
    for i in range(len(distances_best)):
        scores.append(distances_worst[i] / (distances_best[i] + distances_worst[i]))
    return scores

print("Data Preview:")
print(data.head())
print("\nColumn Information:")
print(data.info())

weights = [1, 1, 1, 2]  # Adjust as per your requirement
impacts = ["+", "+", "-", "+"]  # Adjust as per your requirement

num_columns = len(data.columns) - 1  # Exclude the first column
if len(weights) != num_columns or len(impacts) != num_columns:
    print(f"Mismatch detected! The number of numeric columns is {num_columns}.")
    print("Updating weights and impacts to match the columns...")
    weights = [1] * num_columns  # Default weights
    impacts = ["+"] * num_columns  # Default impacts (positive for all)
    print(f"Updated Weights: {weights}")
    print(f"Updated Impacts: {impacts}")

data.iloc[:, 1:] = data.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")
if data.iloc[:, 1:].isnull().values.any():
    raise ValueError("Input data contains non-numeric values in numeric columns.")
# Call the TOPSIS function
scores = topsis(data.copy(), weights, impacts)

# Add scores and ranks to the DataFrame
data["Topsis Score"] = scores
data["Rank"] = data["Topsis Score"].rank(ascending=False).astype(int)

print("\nFinal Data with Scores and Ranks:")
print(data)
data.to_csv("result.csv", index=False)
print("\nResults saved to 'result.csv'")

from google.colab import files
files.download("result.csv")