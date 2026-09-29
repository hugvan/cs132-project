"""Parse eFOI listing and detail pages (server-rendered HTML) into plain dicts.

Only structural fields are kept: no requester names, message text or attachments.
"""
import re
from datetime import datetime

from bs4 import BeautifulSoup

BASE = "https://www.foi.gov.ph"
MONTHS = "Jan|Feb|Mar|Apr|May|June?|July?|Aug|Sept?|Oct|Nov|Dec"
DATE_RE = re.compile(rf"(?:{MONTHS})[a-z]*\.? \d{{1,2}}, \d{{4}}(?:, [\w:. ]+)?")


def parse_date(text):
    """Parse the portal's date formats into a naive Manila-time datetime.

    Handles 'Sept. 27, 2026, 11:03 p.m.', 'Nov. 10, 2025, noon', 'May 5, 2025, 9 a.m.',
    and the timeline's ISO form '2025-12-02 17:31:52.337983'. Returns None if unparseable.
    """
    if not text:
        return None
    t = " ".join(text.split())
    m = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", t)
    if m:
        return datetime.strptime(m.group(0), "%Y-%m-%d %H:%M:%S")
    t = t.replace("Sept.", "Sep.").replace("a.m.", "AM").replace("p.m.", "PM")
    t = t.replace("noon", "12:00 PM").replace("midnight", "12:00 AM").replace(".", "")
    for fmt in ("%b %d, %Y, %I:%M %p", "%b %d, %Y, %I %p", "%B %d, %Y, %I:%M %p",
                "%B %d, %Y, %I %p", "%b %d, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(t, fmt)
        except ValueError:
            pass
    return None


def _iso(dt):
    return dt.isoformat(sep=" ") if dt else ""


def _panel_fields(panel):
    """Fields shared by listing cards and the detail header card."""
    link = panel.select_one("h4.title a")
    desc = panel.select_one("p.description")
    text = " ".join(desc.get_text(" ", strip=True).split())
    spans = [s.get_text(strip=True) for s in desc.find_all("span")]
    agency_link = desc.select_one('a[href^="/agencies/"]')
    tracking = re.search(r"Tracking no:\s*#?(\S+)", text)
    purpose = re.search(r"Purpose:\s*(.*?)\s*(?:Tracking no:|$)", text)
    status = panel.select_one(".component-status")
    return {
        "tracking_number": tracking.group(1) if tracking else "",
        "title": link.get_text(strip=True) if link else "",
        "agency_name": spans[0] if spans else "",
        "agency_code": agency_link["href"].strip("/").split("/")[-1] if agency_link else "",
        "filed_at": _iso(parse_date(desc.get("title"))),
        "purpose": purpose.group(1) if purpose else "",
        "status": status.get_text(strip=True).upper() if status else "",
        "detail_url": BASE + link["href"] if link else "",
    }


def parse_listing(html):
    soup = BeautifulSoup(html, "html.parser")
    return [_panel_fields(p) for p in soup.select(".component-panel") if p.select_one("p.description")]


def listing_last_page(html):
    soup = BeautifulSoup(html, "html.parser")
    nums = [int(a.get_text(strip=True).replace(",", ""))
            for a in soup.select(".pagination a") if a.get_text(strip=True).replace(",", "").isdigit()]
    return max(nums) if nums else None


def parse_detail(html):
    """Return one dict of request-level fields from a detail page, or None if not a request page."""
    soup = BeautifulSoup(html, "html.parser")
    panel = soup.select_one(".component-panel")
    if not panel or not panel.select_one("p.description"):
        return None
    row = _panel_fields(panel)

    # Status timeline: SUBMITTED / PROCESSING / final status, each optionally dated.
    stages = {}
    for item in soup.select(".timeline-item"):
        title = " ".join(item.select_one(".timeline-title").get_text(" ", strip=True).split()) \
            if item.select_one(".timeline-title") else ""
        date = item.select_one(".timeline-body small")
        stages[title] = parse_date(date.get_text()) if date else None
    final = [k for k in stages if k.startswith("REQUEST ") and k != "REQUEST SUBMITTED"]
    row["processing_at"] = _iso(stages.get("PROCESSING REQUEST"))
    row["final_status_at"] = _iso(stages[final[0]]) if final else ""

    # Conversation: -client = requester, -agency = agency. Keep only timestamps and counts.
    agency_times, requester_times = [], []
    for msg in soup.select(".component-message"):
        info = msg.select_one(".information")
        m = DATE_RE.search(info.get_text(" ", strip=True)) if info else None
        when = parse_date(m.group(0)) if m else None
        (agency_times if "-agency" in msg.get("class", []) else requester_times).append(when)
    agency_times = sorted(t for t in agency_times if t)
    row["first_agency_reply_at"] = _iso(agency_times[0]) if agency_times else ""
    row["last_agency_reply_at"] = _iso(agency_times[-1]) if agency_times else ""
    row["n_agency_messages"] = len(agency_times)
    row["n_requester_messages"] = len(requester_times)
    return row
