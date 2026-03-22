import gspread
from google.oauth2.service_account import Credentials
import datetime
import pandas as pd
import streamlit as st

def get_worksheet(spreadsheet_name, worksheet_name=None):
    """
    spreadsheet_name：google sheets名稱
    worksheet_name：sheet名稱
    """
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    )
    client = gspread.authorize(creds)
    spreadsheet = client.open(spreadsheet_name)

    if worksheet_name:
        worksheet = spreadsheet.worksheet(worksheet_name)
    else:
        worksheet = spreadsheet.sheet1

    return worksheet


def append_dict(worksheet, data, columns=None):
    if columns:
        row = [data.get(col, "") for col in columns]
    else:
        row = list(data.values())
    worksheet.append_row(row)


def overwrite_dataframe(worksheet, df: pd.DataFrame):
    worksheet.clear()
    worksheet.update([df.columns.tolist()] + df.fillna("").values.tolist())


def read_dataframe(worksheet):
    data = worksheet.get_all_records()
    return pd.DataFrame(data)