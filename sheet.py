import gspread
# import pandas as pd
# from gspread_dataframe import get_as_dataframe
from oauth2client.service_account import ServiceAccountCredentials


def get_sheet(filename, name_sheet):
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        filename=filename, scopes=scopes
    )
    client = gspread.authorize(credentials)
    sheet = client.open(title=name_sheet).sheet1

    return sheet


# data = get_as_dataframe(sheet, evaluate_formulas=True, header=0)

# print(data)
