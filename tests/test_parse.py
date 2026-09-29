"""Parser tests on synthetic HTML that mirrors the eFOI page structure."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from efoi_parse import listing_last_page, parse_date, parse_detail, parse_listing  # noqa: E402

PANEL = """
<div class="component-panel successful mb10">
  <h4 class="title"><a href="/agencies/abc/sample-request/">Sample request</a></h4>
  <p class="description" title="Nov. 10, 2025, 3:16 p.m.">
    Published by <span>Agency of Examples(ABC)</span> on Nov. 10, 2025.<br>
    Requested from <a href="/agencies/abc/"><span>ABC</span></a> at 03:16 PM on Nov. 10, 2025.<br>
    Purpose: <span>Undergraduate thesis</span> <br>
    Tracking no: <span>#ABC-123456789012</span> <br>
  </p>
  <label class="component-status -successful"><i></i> SUCCESSFUL</label>
</div>"""

DETAIL = f"""<html><body>
<div class="timeline-item"><div class="timeline-title">REQUEST <br> SUBMITTED</div>
  <div class="timeline-body"><p><small>Date: Nov. 10, 2025, 3:16 p.m.</small></p></div></div>
<div class="timeline-item"><div class="timeline-title">PROCESSING REQUEST</div>
  <div class="timeline-body"><p><small>Date: 2025-11-12 09:00:05.1234</small></p></div></div>
<div class="timeline-item"><div class="timeline-title">REQUEST <br> SUCCESSFUL</div>
  <div class="timeline-body"><p><small>Date: 2025-12-02 17:31:52.337983</small></p></div></div>
{PANEL}
<div class="PUBLIC component-message -client"><p class="information"><span>Requester</span> Nov. 10, 2025, 3:16 p.m.</p>
  <div class="speechbubble">secret request text</div></div>
<div class="RO component-message -agency"><p class="information"><span>ABC</span> Nov. 12, 2025, 9 a.m.</p></div>
<div class="DM component-message -agency"><p class="information"><span>ABC</span> Dec. 2, 2025, noon</p></div>
</body></html>"""


class ParseTests(unittest.TestCase):
    def test_dates(self):
        self.assertEqual(str(parse_date("Sept. 27, 2026, 11:03 p.m.")), "2026-09-27 23:03:00")
        self.assertEqual(str(parse_date("May 5, 2025, 9 a.m.")), "2025-05-05 09:00:00")
        self.assertEqual(str(parse_date("Dec. 2, 2025, noon")), "2025-12-02 12:00:00")
        self.assertEqual(str(parse_date("Date: 2025-12-02 17:31:52.3")), "2025-12-02 17:31:52")
        self.assertIsNone(parse_date("not a date"))

    def test_listing(self):
        html = f"{PANEL}<ul class='pagination'><a>1</a><a>17,696</a><a>»</a></ul>"
        [row] = parse_listing(html)
        self.assertEqual(row["tracking_number"], "ABC-123456789012")
        self.assertEqual(row["agency_code"], "abc")
        self.assertEqual(row["purpose"], "Undergraduate thesis")
        self.assertEqual(row["status"], "SUCCESSFUL")
        self.assertEqual(row["filed_at"], "2025-11-10 15:16:00")
        self.assertEqual(listing_last_page(html), 17696)

    def test_detail(self):
        row = parse_detail(DETAIL)
        self.assertEqual(row["first_agency_reply_at"], "2025-11-12 09:00:00")
        self.assertEqual(row["last_agency_reply_at"], "2025-12-02 12:00:00")
        self.assertEqual(row["n_agency_messages"], 2)
        self.assertEqual(row["n_requester_messages"], 1)
        self.assertEqual(row["processing_at"], "2025-11-12 09:00:05")
        self.assertEqual(row["final_status_at"], "2025-12-02 17:31:52")
        self.assertNotIn("secret request text", str(row))

    def test_detail_without_replies(self):
        row = parse_detail(PANEL)
        self.assertEqual(row["first_agency_reply_at"], "")
        self.assertEqual(row["n_agency_messages"], 0)

    def test_non_request_page(self):
        self.assertIsNone(parse_detail("<html><title>Just a moment...</title></html>"))


if __name__ == "__main__":
    unittest.main()
