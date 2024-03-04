import pandas as pd
from urllib.parse import urlparse
import os

# Read URLs from the text file
with open("../player_urls.txt", "r") as file:
    player_urls = file.readlines()

# Create a folder named "Player_Data" if it doesn't exist
folder_name = "Player_Data"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Process each URL
for url in player_urls:
    url = url.strip()  # Remove leading/trailing whitespaces

    # Read HTML tables from the URL
    dfs = pd.read_html(url)

    # Assuming the table of interest is the first one on the page
    df = dfs[0]

    # Remove any rows that contain all NaN values
    df = df.dropna(how="all")
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Remove parentheses and percentage from the "Use" column
    df['Use'] = df['Use'].str.replace(r'\([^()]*\)|%', '', regex=True)

    # Convert KAST from percentage to decimal
    df['KAST'] = df['KAST'].str.rstrip('%').astype(float) / 100

    # Extract player name from the URL
    parsed_url = urlparse(url)
    player_name = parsed_url.path.split('/')[3]  # Extracts 't3xture' from the URL

    # Construct Excel file path
    excel_file_path = os.path.join(folder_name, f"{player_name.capitalize()}_Player_Data.xlsx")

    # Write DataFrame to Excel
    df.to_excel(excel_file_path, index=False)