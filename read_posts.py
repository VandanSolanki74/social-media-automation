from utils.sheet_reader import get_pending_posts

# Set these as per your sheet
SHEET_NAME = "social-media-automation"
CLIENT_TAB = "Vivianna"  # Example

posts = get_pending_posts(SHEET_NAME, CLIENT_TAB)

if not posts:
    print("No posts to publish at this time.")
else:
    print(f"Found {len(posts)} post(s) to publish:\n")
    for post in posts:
        print(post)
