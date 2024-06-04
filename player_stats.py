import json
import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the JSON file
with open('scores.json', 'r') as f:
    data = json.load(f)

# Initialize an empty DataFrame
df = pd.DataFrame()

# Iterate over each player in the data
for player_name, player_data in data.items():
    # Convert the player's data to a DataFrame
    player_df = pd.DataFrame(player_data)
    # Add a column for the player's name
    player_df['player_name'] = player_name
    # Append the player's DataFrame to the main DataFrame
    df = df._append(player_df, ignore_index=True)
