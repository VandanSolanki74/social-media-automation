from utils.sheet_reader import get_pending_posts, update_post_status

SHEET_NAME = "social-media-automation"
CLIENT_TAB = "Vivianna Group"

posts = get_pending_posts(SHEET_NAME, CLIENT_TAB)

if not posts:
    print("No posts to publish at this time.")
else:
    print(f"Found {len(posts)} post(s):\n")

    for post in posts:
        print(post)
        
        # Simulate successful posting
        update_post_status(SHEET_NAME, CLIENT_TAB, post["_row_number"])
