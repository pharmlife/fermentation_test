"""
Logic for downloading data from Notion

"""

import requests
import pandas as pd

NOTION_ACCESS_TOKEN = 'secret_SBzckpdOOtWsu7R6BSt3rEMPP2XIrakgLogPOg9ItnW'
NOTION_DATABASE_ID = '558261863d3b40d2a2d403748079e37f'

NOTION_API_URL = 'https://api.notion.com/v1'
DATABASE_URL = f'{NOTION_API_URL}/databases/{NOTION_DATABASE_ID}/query'


def download_notion_data() -> pd.DataFrame:
    raw_data = _download_raw_data()

    return _format_raw_data(raw_data)


def _download_raw_data():
    headers = {
        'Authorization': f'Bearer {NOTION_ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'Notion-Version': '2021-05-13',
    }

    database_response = requests.post(DATABASE_URL, headers=headers)
    database_response.raise_for_status()

    raw_data = database_response.json()["results"]

    return raw_data


def _format_raw_data(raw_data):
    df = pd.DataFrame(
        columns=["Dye House", "Location", "Fermentor Name", "Fermentor Model", "Type", "Timestamp", "URL"]
    )

    for i, r in enumerate(raw_data):
        r = r["properties"]
        df.loc[i] = [
            r["Client"]["select"]["name"],
            r["Client location"]["select"]["name"],
            r["Fermentor used"]["select"]["name"],
            r["Fermentor model"]["select"]["name"],
            r["Sample type"]["select"]["name"],
            r["Date"]["date"]["start"],
            r["Download URL"]["url"]
        ]

    return df

