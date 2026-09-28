"""Check static portfolio IDs, local links and required research sections."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / "docs"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.h1_count = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                raise ValueError(f"Duplicate HTML id: {attrs['id']}")
            self.ids.add(attrs["id"])
        if tag == "h1":
            self.h1_count += 1
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.links.append(attrs[attr])


def main():
    page = Page()
    page.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    if page.h1_count != 1:
        raise ValueError("Portfolio must have exactly one h1")
    for section in ("background", "research", "data", "methods", "team"):
        if section not in page.ids:
            raise ValueError(f"Missing required section: {section}")
    for link in page.links:
        parsed = urlsplit(link)
        if parsed.scheme or parsed.netloc:
            continue
        if parsed.path:
            target = (ROOT / unquote(parsed.path)).resolve()
            if not target.is_relative_to(ROOT) or not target.is_file():
                raise ValueError(f"Broken or out-of-site local link: {link}")
        elif parsed.fragment and unquote(parsed.fragment) not in page.ids:
            raise ValueError(f"Broken section link: {link}")
    print("Portfolio checks passed: research sections, heading, IDs and local links.")


if __name__ == "__main__":
    main()
