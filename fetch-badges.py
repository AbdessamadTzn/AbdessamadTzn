import requests
from bs4 import BeautifulSoup

USERNAME = "abdessamad-touzani"  # replace with your public Credly username
URL = f"https://www.credly.com/users/{USERNAME}/badges"

resp = requests.get(URL)
soup = BeautifulSoup(resp.text, "html.parser")

badges = []

for badge in soup.select("div.cr-badge"):
    img = badge.find("img")
    link = badge.find("a", href=True)

    if img and link:
        badge_md = f"[![{img['alt']}]({img['src']})](https://www.credly.com{link['href']})"
        badges.append(badge_md)

# Read README
with open("README.md", "r") as f:
    readme = f.read()

start = "<!-- CREDLY-BADGES:START -->"
end = "<!-- CREDLY-BADGES:END -->"
badge_section = "\n".join(badges)

new_readme = readme.split(start)[0] + start + "\n" + badge_section + "\n" + end + readme.split(end)[1]

with open("README.md", "w") as f:
    f.write(new_readme)
