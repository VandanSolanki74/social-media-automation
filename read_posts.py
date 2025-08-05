import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Step 1: Load JSON credentials from GitHub secret (or local env)
json_creds = os.getenv("SERVICE_ACCOUNT_JSON")
if not json_creds:
    raise Exception("SERVICE_ACCOUNT_JSON not found in environment variables!")

creds_dict = json.loads(json_creds)

# Step 2: Authenticate using gspread
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Step 3: Open the spreadsheet and select the worksheet (tab)
spreadsheet = client.open("social-media-automation")  # ✅ correct name
worksheet = spreadsheet.worksheet("Nilkanth")  # change to another client tab if needed

# Step 4: Fetch all rows
rows = worksheet.get_all_records()

# Step 5: Filter rows where Status == "pending"
pending_posts = [row for row in rows if row.get("Status", "").strip().lower() == "pending"]

# Step 6: Print the results
for post in pending_posts:
    print(f"Scheduled post on {post['Date']} at {post['Time']} for {post['Platform']}")
    print(f"Title: {post['Title']} | Subtitle: {post['Subtitle']}")
    print(f"Caption: {post['Caption']}")
    print(f"MediaURLs: {post['MediaURLs']}")
    print("-" * 50)
