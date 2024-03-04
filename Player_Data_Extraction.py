import pandas as pd
import requests
from bs4 import BeautifulSoup


def extract_player_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    tables = soup.find_all("table", class_="wf-table-inset mod-overview")

    player_data = []
    for table in tables:
        headers = [th.text for th in table.find_all("th")]
        data_rows = table.find_all("tr")[1:]

        for row in data_rows:
            row_data = []
            for td in row.find_all("td"):
                if td.get("class") == ["mod-stat", "mod-vlr-deaths"]:
                    deaths_span = td.find("span", class_="mod-both")
                    row_data.append(deaths_span.text.strip() if deaths_span else "")
                else:
                    text = td.text.strip()
                    if text:
                        first_value = text.split()[0]
                        row_data.append(first_value)
                    else:
                        row_data.append("")
            player_data.append(row_data)

    return pd.DataFrame(player_data, columns=headers)

    # Read URLs from the text file
with open("player_urls.txt", "r") as file:
    urls = [line.strip() for line in file.readlines()]

    # Combine data from all URLs into a single DataFrame
    combined_df = pd.concat([extract_player_data(url) for url in urls], ignore_index=True)

    # Define the file path
    file_path = "Player_Stats_Per_Map.xlsx"

    # Save the combined DataFrame to an Excel file
    combined_df.to_excel(file_path, index=False)

    # Read the Excel file again
    combined_df = pd.read_excel(file_path)

    # Rename the first column to "Name" and drop the second column
    combined_df.rename(columns={combined_df.columns[0]: "Name"}, inplace=True)
    combined_df.drop(combined_df.columns[1], axis=1, inplace=True)

    # Save the modified DataFrame back to the Excel file
    combined_df.to_excel(file_path, index=False)

    print(f'Data saved to {file_path}')