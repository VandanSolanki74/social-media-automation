from google.oauth2.service_account import Credentials
import gspread
import json
import os

creds_dict = json.loads(os.environ["SERVICE_ACCOUNT_JSON"])
creds = Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(creds)

# List all visible spreadsheet titles
for file in client.list_spreadsheet_files():
    print(file['name'])
