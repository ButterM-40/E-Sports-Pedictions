import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load data from Excel files for each player and their teammates
folder_name = "Player_Data"
all_dfs = []
for file in os.listdir(folder_name):
    if file.endswith(".xlsx"):
        df = pd.read_excel(os.path.join(folder_name, file))
        all_dfs.append(df)
combined_df = pd.concat(all_dfs)

# Split features and target variable
X = combined_df.drop(columns=["K"])
y = combined_df["K"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Make predictions for a specific player's next game
next_game_features = {
    "Use": 80,       # Percentage of utility usage
    "RND": 150,      # Round number
    "Rating": 1.05,  # Player's rating
    "ACS": 220,      # Average Combat Score
    "K:D": 1.2,      # Kill-to-Death ratio
    "ADR": 140,      # Average Damage per Round
    "KAST": 0.75,    # Percentage of rounds with a Kill, Assist, Survive, or Trade
    "KPR": 0.8,      # Kills per Round
    "APR": 0.9,      # Assists per Round
    "FKPR": 0.1,     # First Kill per Round percentage
    "FDPR": 0.05,    # First Death per Round percentage
    "D": 20,         # Total Deaths
    "A": 10,         # Total Assists
    "FK": 5,         # Total First Kills
    "FD": 8          # Total First Deaths
}
predicted_probability = model.predict_proba(next_game_features)[0][1]
print("Predicted probability of hitting kills (K):", predicted_probability)
