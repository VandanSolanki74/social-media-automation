import os
from sheet_reader import get_pending_posts, update_post_status

# 🔁 List all client tab names (must match tabs in your Google Sheet)
CLIENT_TABS = ["Nilkanth", "Vivianna", "Royce", "MetWeld"]  # Add more tabs/clients here
SHEET_NAME = "social-media-automation1"  # Replace with your actual Google Sheet name

def get_platform_token(client_key, platform):
    """
    Fetch token from environment variables based on client and platform.
    E.g., VIVIANNA_LINKEDIN_TOKEN or ROYCE_INSTAGRAM_TOKEN
    """
    token_key = f"{client_key.upper()}_{platform.upper()}_TOKEN"
    token = os.environ.get(token_key)
    if not token:
        print(f"⚠️ Token not found: {token_key}")
    return token

def post_to_platform(platform, post_data, token):
    """
    Placeholder for actual posting logic. Currently just prints.
    Replace with API call to post on the selected platform.
    """
    print(f"📢 Posting to {platform} with token {token[:4]}...: {post_data['Title']}")
    # TODO: Add actual API integration here (LinkedIn, Instagram, etc.)
    return True  # Simulate successful post

def main():
    for client_tab in CLIENT_TABS:
        print(f"\n🔍 Checking posts for client: {client_tab}")
        posts = get_pending_posts(SHEET_NAME, client_tab)

        if not posts:
            print("✅ No pending posts to publish at this time.")
            continue

        for post in posts:
            platform = post.get("Platform", "").strip().lower()
            if not platform:
                print(f"⚠️ Platform missing in row {post['_row_number']}, skipping.")
                continue

            token = get_platform_token(client_tab, platform)
            if not token:
                print(f"❌ No token found for {client_tab} - {platform}. Skipping post.")
                continue

            success = post_to_platform(platform, post, token)
            if success:
                update_post_status(SHEET_NAME, client_tab, post["_row_number"], "done")
            else:
                update_post_status(SHEET_NAME, client_tab, post["_row_number"], "failed")

if __name__ == "__main__":
    main()
