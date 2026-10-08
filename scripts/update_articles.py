"""Refresh the "Latest articles" block of README.md from the portfolio's blogs.json."""

import json
import re
import urllib.request
from pathlib import Path

SITE = "https://abdessamadtouzani.com"
FEED = f"{SITE}/assets/js/blogs.json"
README = Path(__file__).resolve().parent.parent / "README.md"
START, END = "<!-- ARTICLES:START -->", "<!-- ARTICLES:END -->"
LIMIT = 3

MONTHS = {
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6,
    "juillet": 7, "août": 8, "aout": 8, "septembre": 9, "octobre": 10, "novembre": 11,
    "décembre": 12, "decembre": 12,
}


def sort_key(article):
    # Dates look like "20 Juillet 2026"; unparseable ones sink to the bottom.
    m = re.match(r"(\d{1,2})\s+(\S+)\s+(\d{4})", article.get("date", ""))
    if not m:
        return (0, 0, 0)
    day, month, year = m.groups()
    return (int(year), MONTHS.get(month.lower(), 0), int(day))


def main():
    with urllib.request.urlopen(FEED, timeout=30) as resp:
        articles = json.load(resp)
    articles = sorted(articles, key=sort_key, reverse=True)[:LIMIT]

    lines = []
    for a in articles:
        url = SITE + "/" + a["url"].removeprefix("./").lstrip("/")
        lines.append(f"- **[{a['title']}]({url})**  \n  <sub>{a['category']} · {a['date']} · {a['readTime']}</sub>")

    readme = README.read_text(encoding="utf-8")
    before, rest = readme.split(START, 1)
    _, after = rest.split(END, 1)
    README.write_text(f"{before}{START}\n" + "\n".join(lines) + f"\n{END}{after}", encoding="utf-8")


if __name__ == "__main__":
    main()
