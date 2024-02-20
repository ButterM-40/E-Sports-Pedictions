import pandas as pd

url = "https://www.vlr.gg/player/9/tenz/?timespan=all"
dfs = pd.read_html(url)

# Assuming the table of interest is the first one on the page
df = dfs[0]

# Remove any rows that contain all NaN values
df = df.dropna(how="all")

# Write DataFrame to Excel
df.to_excel("Val_Player_Data.xlsx", index=False)
