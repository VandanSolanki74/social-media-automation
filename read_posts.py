from sheet_reader import get_pending_posts

SHEET_NAME = "social-media-automation1"  # Same sheet
# Instead of a single tab, get all worksheets
import gspread
from sheet_reader import connect_to_sheet

spreadsheet = connect_to_sheet(SHEET_NAME)
worksheet_list = spreadsheet.worksheets()

all_pending_posts = []

for worksheet in worksheet_list:
    client_tab = worksheet.title
    try:
        pending_posts = get_pending_posts(SHEET_NAME, client_tab)
        for post in pending_posts:
            post["client_tab"] = client_tab  # Store which client this post belongs to
            all_pending_posts.append(post)
    except Exception as e:
        print(f"⚠️ Error processing tab '{client_tab}': {e}")

if not all_pending_posts:
    print("No posts to publish at this time.")
else:
    for post in all_pending_posts:
        print(f"📢 Scheduled post for client '{post['client_tab']}': {post['Title']} at row {post['_row_number']}")
        
        # Simulate successful posting
        update_post_status(SHEET_NAME, CLIENT_TAB, post["_row_number"])
