import pandas as pd
import os


async def get_head(path, page: int):
    files = sorted(os.listdir("./csv_files/"))
    file = pd.read_csv("./csv_files/" + files[path])
    pages = None
    if file.shape[0] % 200 == 0:
        pages = file.shape[0] // 200
    else:
        pages = file.shape[0] // 200 + 1
    if page == 1:
        return file.iloc[0:201].to_json(), pages
    elif page > 1:
        return file.iloc[(page-1)*200:page*200].to_json(), pages

