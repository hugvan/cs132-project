"""Scrape the eFOI portal through a real Chrome window.

foi.gov.ph sits behind Cloudflare, which blocks plain HTTP clients (requests/curl get
HTTP 403 "Just a moment..."). A normal Chrome window loads the pages fine, so this
script starts Google Chrome with a remote-debugging port and reads pages through it.
If Cloudflare ever shows a checkbox, tick it in the Chrome window; the script waits.

Commands (all resumable; re-run the same command to continue after a stop):
  python scripts/scrape_efoi.py range --year 2025          # find listing pages that hold 2025
  python scripts/scrape_efoi.py listing --start A --end B  # listing pages A..B -> data/raw/listing.csv
  python scripts/scrape_efoi.py details --sample data/interim/sample.csv  # -> data/raw/details.csv
"""
import argparse
import csv
import random
import subprocess
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))
from efoi_parse import BASE, listing_last_page, parse_detail, parse_listing  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROFILE = ROOT / ".chrome-profile"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9222
LISTING_FIELDS = ["page", "tracking_number", "title", "agency_name", "agency_code", "filed_at",
                  "purpose", "status", "detail_url", "scraped_at"]
DETAIL_FIELDS = ["tracking_number", "title", "agency_name", "agency_code", "filed_at", "purpose",
                 "status", "processing_at", "final_status_at", "first_agency_reply_at",
                 "last_agency_reply_at", "n_agency_messages", "n_requester_messages",
                 "detail_url", "scraped_at"]


def ensure_chrome():
    try:
        urllib.request.urlopen(f"http://localhost:{PORT}/json/version", timeout=2)
        return
    except OSError:
        pass
    subprocess.Popen([CHROME, f"--remote-debugging-port={PORT}", f"--user-data-dir={PROFILE}",
                      "--no-first-run", "--no-default-browser-check", BASE + "/requests/"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(30):
        time.sleep(1)
        try:
            urllib.request.urlopen(f"http://localhost:{PORT}/json/version", timeout=2)
            return
        except OSError:
            pass
    sys.exit("Could not start Chrome with remote debugging.")


class Browser:
    def __init__(self, pw, delay):
        ensure_chrome()
        ctx = pw.chromium.connect_over_cdp(f"http://localhost:{PORT}").contexts[0]
        self.page = ctx.pages[0] if ctx.pages else ctx.new_page()
        self.delay = delay

    def get(self, url, attempts=3):
        """Load url and return (status, html). Waits out Cloudflare checks; retries with backoff."""
        for attempt in range(attempts):
            time.sleep(random.uniform(*self.delay))
            try:
                resp = self.page.goto(url, wait_until="domcontentloaded", timeout=60_000)
                for waited in range(180):  # up to 3 min for a human to tick a challenge box
                    if "just a moment" not in self.page.title().lower():
                        break
                    if waited == 5:
                        print("  Cloudflare check showing - tick the box in the Chrome window if asked.", flush=True)
                    time.sleep(1)
                html = self.page.content()
                status = resp.status if resp else 0
                if status == 200 or status == 404:
                    return status, html
                print(f"  HTTP {status} on {url}", flush=True)
                if status == 429:  # rate limited: honour Retry-After, else pause a minute
                    retry = (resp.headers.get("retry-after") or "") if resp else ""
                    time.sleep(int(retry) if retry.isdigit() else 60)
                    continue
            except Exception as err:  # timeouts, navigation errors
                print(f"  error on {url}: {err}", flush=True)
            time.sleep(10 * (attempt + 1))
        return None, None


def append_rows(path, fields, rows):
    new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        if new:
            w.writeheader()
        w.writerows(rows)


def read_column(path, col):
    if not path.exists():
        return set()
    with path.open(encoding="utf-8") as f:
        return {r[col] for r in csv.DictReader(f)}


def now():
    return datetime.now().isoformat(sep=" ", timespec="seconds")


def page_dates(browser, n):
    _, html = browser.get(f"{BASE}/requests/page/{n}/")
    dates = [r["filed_at"] for r in parse_listing(html or "") if r["filed_at"]]
    return (min(dates), max(dates)) if dates else (None, None)


def cmd_range(browser, args):
    """Binary-search the newest-first listing for the first and last page of a year."""
    _, html = browser.get(BASE + "/requests/")
    last = listing_last_page(html)
    print(f"Listing has {last} pages.")

    def first_page_older_than(stamp):
        lo, hi = 1, last
        while lo < hi:
            mid = (lo + hi) // 2
            oldest, newest = page_dates(browser, mid)
            print(f"  page {mid}: {oldest} .. {newest}", flush=True)
            if oldest is not None and oldest < stamp:
                hi = mid
            else:
                lo = mid + 1
        return lo

    start = first_page_older_than(f"{args.year + 1}-01-01")
    end = first_page_older_than(f"{args.year}-01-01")
    print(f"\n{args.year} filings are on listing pages {start}..{end} (inclusive).")
    print(f"Next: python scripts/scrape_efoi.py listing --start {start} --end {end}")


def cmd_listing(browser, args):
    out = RAW / "listing.csv"
    done = {int(p) for p in read_column(out, "page")}
    todo = [p for p in range(args.start, args.end + 1) if p not in done]
    print(f"{len(todo)} listing pages to fetch ({len(done)} already done) -> {out}")
    for i, n in enumerate(todo, 1):
        status, html = browser.get(f"{BASE}/requests/page/{n}/")
        rows = parse_listing(html or "")
        if not rows:
            append_rows(RAW / "errors.csv", ["url", "status", "at"],
                        [{"url": f"{BASE}/requests/page/{n}/", "status": status, "at": now()}])
            continue
        stamp = now()
        append_rows(out, LISTING_FIELDS, [{**r, "page": n, "scraped_at": stamp} for r in rows])
        if i % 25 == 0 or i == len(todo):
            print(f"  {i}/{len(todo)} pages (page {n}: {rows[-1]['filed_at']})", flush=True)


def cmd_details(browser, args):
    out = RAW / "details.csv"
    done = read_column(out, "tracking_number")
    with open(args.sample, encoding="utf-8") as f:
        sample = [r for r in csv.DictReader(f) if r["tracking_number"] not in done]
    print(f"{len(sample)} detail pages to fetch ({len(done)} already done) -> {out}")
    for i, r in enumerate(sample, 1):
        status, html = browser.get(r["detail_url"])
        row = parse_detail(html or "")
        if not row:
            append_rows(RAW / "errors.csv", ["url", "status", "at"],
                        [{"url": r["detail_url"], "status": status, "at": now()}])
            continue
        append_rows(out, DETAIL_FIELDS, [{**row, "scraped_at": now()}])
        if i % 25 == 0 or i == len(sample):
            print(f"  {i}/{len(sample)} details", flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--delay", type=float, nargs=2, default=(1.0, 2.0), metavar=("MIN", "MAX"),
                    help="random wait between page loads, seconds (default 1 2)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("range").add_argument("--year", type=int, default=2025)
    p = sub.add_parser("listing")
    p.add_argument("--start", type=int, required=True)
    p.add_argument("--end", type=int, required=True)
    sub.add_parser("details").add_argument("--sample", required=True)
    args = ap.parse_args()
    RAW.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = Browser(pw, tuple(args.delay))
        {"range": cmd_range, "listing": cmd_listing, "details": cmd_details}[args.cmd](browser, args)


if __name__ == "__main__":
    main()
