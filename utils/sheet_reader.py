import os
import json
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_service_account_credentials():
    service_account_json = os.environ.get("SERVICE_ACCOUNT_JSON")
    if not service_account_json:
        raise Exception("SERVICE_ACCOUNT_JSON is not set")
    return json.loads(service_account_json)

def connect_to_sheet(sheet_name: str):
    creds_dict = get_service_account_credentials()
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name)

def get_pending_posts(sheet_name: str, client_tab: str):
    spreadsheet = connect_to_sheet(sheet_name)
    worksheet = spreadsheet.worksheet(client_tab)

    data = worksheet.get_all_records()
    now = datetime.datetime.now()
    today = now.strftime("%d-%m-%Y")
    current_hour = now.strftime("%H")

    filtered = []
    for idx, row in enumerate(data, start=2):  # start=2 for 1-based index + header row
        row_date = str(row.get("Date")).strip()
        row_hour = str(row.get("Time")).zfill(2)
        status = row.get("Status", "").strip().lower()

        if row_date == today and row_hour == current_hour and status == "pending":
            row["_row_number"] = idx
            filtered.append(row)

    return filtered

def update_post_status(sheet_name: str, client_tab: str, row_number: int, new_status: str = "done"):
    spreadsheet = connect_to_sheet(sheet_name)
    worksheet = spreadsheet.worksheet(client_tab)
    status_col_index = get_column_index_by_name(worksheet, "Status")

    if status_col_index is None:
        raise Exception("Status column not found.")

    worksheet.update_cell(row_number, status_col_index, new_status)
    print(f"✅ Updated row {row_number} to '{new_status}'")

def get_column_index_by_name(worksheet, column_name: str):
    headers = worksheet.row_values(1)
    for i, name in enumerate(headers, start=1):
        if name.strip().lower() == column_name.strip().lower():
            return i
    return None
