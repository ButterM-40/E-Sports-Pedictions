import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import mean_squared_error

# Load data from the Excel files into a single DataFrame
folder_name = "Player_Data"
all_dfs = []
for file in os.listdir(folder_name):
    if file.endswith(".xlsx"):
        df = pd.read_excel(os.path.join(folder_name, file))
        all_dfs.append(df)
combined_df = pd.concat(all_dfs)

# Assuming 'Kills' is the target variable
X = combined_df.drop(columns=['K'])
y = combined_df['K']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define the neural network model
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    Dropout(0.2),
    Dense(64, activation='relu'),
    Dropout(0.2),
    Dense(1)
])

# Compile the model
model.compile(optimizer=Adam(), loss='mean_squared_error')

# Train the model
history = model.fit(X_train_scaled, y_train, epochs=100, batch_size=32, validation_split=0.2)

# Evaluate the model
y_pred = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Make predictions for t3xture's next game
next_game_features = pd.DataFrame({
    'Use': [75],  # Example value for 'Use'
    'RND': [193],  # Example value for 'RND'
    'Rating': [0.99],  # Example value for 'Rating'
    'ACS': [175.6],  # Example value for 'ACS'
    'K:D': [0.91],  # Example value for 'K:D'
    'ADR': [116.7],  # Example value for 'ADR'
    'KAST': [72],  # Example value for 'KAST' (converted from percentage to decimal)
    'KPR': [0.44],  # Example value for 'KPR'
    'APR': [0.11],  # Example value for 'APR'
    'FKPR': [0.11],  # Example value for 'FKPR'
    'FDPR': [0.14],  # Example value for 'FDPR'
    'D': [138],  # Example value for 'D'
    'A': [76],  # Example value for 'A'
    'FK': [14],  # Example value for 'FK'
    'FD': [14]  # Example value for 'FD'
})

# Standardize the next game features
next_game_features_scaled = scaler.transform(next_game_features)

# Make predictions for t3xture's next game
predicted_kills = model.predict(next_game_features_scaled)
print(f"Predicted kills for t3xture's next game: {predicted_kills}")
