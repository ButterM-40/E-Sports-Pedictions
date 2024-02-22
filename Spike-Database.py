import pandas as pd
import requests
from bs4 import BeautifulSoup

# Read URLs from the text file
with open("player_urls.txt", "r") as file:
    urls = file.readlines()

# Create an empty DataFrame to store all the data
combined_df = pd.DataFrame()

# Loop over each URL
for url in urls:
    url = url.strip()  # Remove leading/trailing whitespaces

    # Send a GET request to the URL
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    # Find all tables with the specified class
    tables = soup.find_all("table", class_="wf-table-inset mod-overview")

    # Extract data from the first table
    table0 = tables[0]
    headers0 = table0.find_all("th")
    titles0 = [i.text for i in headers0]
    df0 = pd.DataFrame(columns=titles0)

    rows0 = table0.find_all("tr")
    for i, row in enumerate(rows0[1:], start=1):
        data0 = row.find_all("td")
        row0 = []
        for td in data0:
            if td.get("class") == ["mod-stat", "mod-vlr-deaths"]:
                deaths_span = td.find("span", class_="mod-both")
                row0.append(deaths_span.text.strip() if deaths_span else "")
            else:
                text = td.text.strip()
                if text:
                    first_value = text.split()[0]
                    row0.append(first_value)
                else:
                    row0.append("")
        df0.loc[i] = row0

    # Extract data from the second table and append to the first DataFrame
    for table_index in [1, 4, 5]:
        current_table = tables[table_index]
        current_rows = current_table.find_all("tr")
        for i, row in enumerate(current_rows[1:], start=len(df0)):
            data = row.find_all("td")
            current_row = []
            for td in data:
                if td.get("class") == ["mod-stat", "mod-vlr-deaths"]:
                    deaths_span = td.find("span", class_="mod-both")
                    current_row.append(deaths_span.text.strip() if deaths_span else "")
                else:
                    text = td.text.strip()
                    if text:
                        first_value = text.split()[0]
                        current_row.append(first_value)
                    else:
                        current_row.append("")
            df0.loc[i] = current_row

    # Add a new column with the URL as a reference
    df0["URL"] = url

    # Concatenate the current DataFrame with the combined DataFrame
    combined_df = pd.concat([combined_df, df0])

# Define the file path
file_path = "Player_Stats_Per_Map.xlsx"

# Save the combined DataFrame to an Excel file
combined_df.to_excel(file_path, index=False)

print(f'Data saved to {file_path}')
