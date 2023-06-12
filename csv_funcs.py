import pandas as pd


async def get_head(path):
    file = pd.read_csv("./csv_files/" + path)
    return file.head(1000).to_csv(index=False)

