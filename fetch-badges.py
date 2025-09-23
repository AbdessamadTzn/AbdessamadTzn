import requests
import os

USERNAME = "abdessamad-touzani"  
API_URL = f"https://credly.com/api/v1/users/{abdessamad-touzani}/badges"

# Fetch badges (requires API key if not public)
headers = {"Authorization": f"Bearer {os.environ['CREDLY_TOKEN']}"}
resp = requests.get(API_URL, headers=headers)

if resp.status_code == 200:
    badges = resp.json().get("data", [])
    with open("README.md", "r") as f:
        readme = f.read()

    # Insert badges at placeholder
    start = "<!-- CREDLY-BADGES:START -->"
    end = "<!-- CREDLY-BADGES:END -->"
    badge_md = "\n".join(
        f"[![{b['badge_template']['name']}]({b['badge_template']['image_url']})]({b['issued_to']['url']})"
        for b in badges
    )
    new_readme = readme.split(start)[0] + start + "\n" + badge_md + "\n" + end + readme.split(end)[1]

    with open("README.md", "w") as f:
        f.write(new_readme)
