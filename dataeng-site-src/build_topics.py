"""Build data/topics.js for the Data Engineering study site.

Usage:  python3 build_topics.py  <output_dir>
Writes  <output_dir>/data/topics.js

Each topic follows one recipe:
  picture -> predict -> explain (ASD-STE100 style) -> worked example -> Q&A
  -> best verified video -> build from a blank page -> teach it back -> self-check
Every code example and every number below was run before it was written here
(see verify_examples.py).
"""
import html
import json
import sys
from datetime import date

W = 520  # diagram canvas width


# ---------------------------------------------------------------- svg helpers
def esc(s):
    return html.escape(str(s), quote=True)


def box(x, y, w, h, cls="bx", rx=8, dash=False):
    d = ' stroke-dasharray="5 4"' if dash else ""
    return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"{d}/>'


def text(x, y, s, cls="tx", anchor="start", size=None):
    st = f' font-size="{size}"' if size else ""
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}"{st}>{esc(s)}</text>'


def line(x1, y1, x2, y2, cls="ln", dash=False):
    d = ' stroke-dasharray="5 4"' if dash else ""
    return f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{d}/>'


def arrow(x1, y1, x2, y2, mid, cls="ar"):
    return f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-end="url(#{mid})"/>'


def svg(h, body, label, mid):
    defs = (
        f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
        f'orient="auto-start-reverse"><path class="mk" d="M0 0 L10 5 L0 10 z"/></marker></defs>'
    )
    return f'<svg viewBox="0 0 {W} {h}" role="img" aria-label="{esc(label)}" xmlns="http://www.w3.org/2000/svg">{defs}{body}</svg>'


# ------------------------------------------------------------------- diagrams
def d_dict_count():
    b = []
    panels = [
        (0, "Order 1: shipped", "Not in tally: set to 1", [("shipped: 1", True)]),
        (180, "Order 2: pending", "Not in tally: set to 1", [("shipped: 1", False), ("pending: 1", True)]),
        (360, "Order 3: shipped", "In tally: add 1", [("shipped: 2", True), ("pending: 1", False)]),
    ]
    for x, head, note, rows in panels:
        b.append(box(x, 8, 160, 34, "bx"))
        b.append(text(x + 80, 30, head, "tx tb", "middle"))
        b.append(arrow(x + 80, 42, x + 80, 70, "m1"))
        b.append(text(x + 80, 64, "", "tx"))
        b.append(box(x, 74, 160, 92, "bx"))
        b.append(text(x + 10, 92, "tally", "tx tm", "start", 11))
        for i, (s, hl) in enumerate(rows):
            yy = 112 + i * 26
            b.append(box(x + 10, yy - 16, 140, 22, "bxa" if hl else "bx", 5))
            b.append(text(x + 80, yy, s, "tx", "middle"))
        b.append(text(x + 80, 186, note, "tx tm", "middle", 12))
    return svg(200, "".join(b), "Three panels showing a tally dictionary after each of three orders.", "m1")


def d_mutable():
    b = []
    # left: bug
    b.append(text(0, 14, "Bug: cart=[]", "tx tw tb"))
    b.append(box(0, 24, 245, 34, "bxw"))
    b.append(text(122, 46, "def add_item(item, cart=[])", "tx", "middle", 12))
    b.append(arrow(122, 58, 122, 92, "m2"))
    b.append(box(52, 96, 140, 46, "bxw"))
    b.append(text(122, 116, "ONE list", "tx tb", "middle"))
    b.append(text(122, 133, "made when def runs", "tx tm", "middle", 11))
    b.append(box(0, 190, 112, 40, "bx"))
    b.append(text(56, 207, "Call 1", "tx tb", "middle", 12))
    b.append(text(56, 222, "adds 'Laptop'", "tx tm", "middle", 11))
    b.append(box(133, 190, 112, 40, "bx"))
    b.append(text(189, 207, "Call 2", "tx tb", "middle", 12))
    b.append(text(189, 222, "adds 'Mouse'", "tx tm", "middle", 11))
    b.append(arrow(56, 190, 90, 144, "m2"))
    b.append(arrow(189, 190, 156, 144, "m2"))
    b.append(text(122, 184, "['Laptop', 'Mouse']", "tx tw", "middle", 11))
    # right: fix
    ox = 275
    b.append(text(ox, 14, "Fix: cart=None", "tx tg tb"))
    b.append(box(ox, 24, 245, 34, "bxg"))
    b.append(text(ox + 122, 46, "def add_item(item, cart=None)", "tx", "middle", 12))
    b.append(box(ox, 100, 112, 54, "bx"))
    b.append(text(ox + 56, 120, "Call 1", "tx tb", "middle", 12))
    b.append(text(ox + 56, 138, "new list", "tx tm", "middle", 11))
    b.append(box(ox + 133, 100, 112, 54, "bx"))
    b.append(text(ox + 189, 120, "Call 2", "tx tb", "middle", 12))
    b.append(text(ox + 189, 138, "new list", "tx tm", "middle", 11))
    b.append(arrow(ox + 56, 58, ox + 56, 98, "m2"))
    b.append(arrow(ox + 189, 58, ox + 189, 98, "m2"))
    b.append(box(ox, 190, 112, 34, "bxg"))
    b.append(text(ox + 56, 212, "['Laptop']", "tx", "middle", 12))
    b.append(box(ox + 133, 190, 112, 34, "bxg"))
    b.append(text(ox + 189, 212, "['Mouse']", "tx", "middle", 12))
    b.append(arrow(ox + 56, 154, ox + 56, 188, "m2"))
    b.append(arrow(ox + 189, 154, ox + 189, 188, "m2"))
    return svg(244, "".join(b), "Left: two calls share one list. Right: each call makes a new list.", "m2")


def d_generators():
    b = []
    b.append(text(0, 14, "List  [ ]  stores the values", "tx tb"))
    vals = ["9.0", "22.5", "7.2", "36.0"]
    for i, v in enumerate(vals):
        b.append(box(i * 70, 24, 62, 34, "bxg"))
        b.append(text(i * 70 + 31, 46, v, "tx", "middle"))
    b.append(text(300, 46, "read it as often as you like", "tx tm", "start", 12))
    b.append(line(0, 78, W, 78, "ln"))
    b.append(text(0, 100, "Generator  ( )  gives one value at a time", "tx tb"))
    b.append(box(0, 112, 150, 40, "bxa"))
    b.append(text(75, 137, "p * 0.9 for p in prices", "tx", "middle", 11))
    b.append(arrow(150, 132, 188, 132, "m3"))
    b.append(box(190, 112, 110, 40, "bx"))
    b.append(text(245, 137, "list(gen)  #1", "tx", "middle", 12))
    b.append(arrow(300, 132, 338, 132, "m3"))
    b.append(box(340, 112, 180, 40, "bxg"))
    b.append(text(430, 137, "[9.0, 22.5, 7.2, 36.0]", "tx", "middle", 11))
    b.append(box(0, 176, 150, 40, "bxw", 8, True))
    b.append(text(75, 201, "used up: nothing left", "tx tw", "middle", 11))
    b.append(arrow(150, 196, 188, 196, "m3"))
    b.append(box(190, 176, 110, 40, "bx"))
    b.append(text(245, 201, "list(gen)  #2", "tx", "middle", 12))
    b.append(arrow(300, 196, 338, 196, "m3"))
    b.append(box(340, 176, 180, 40, "bxw"))
    b.append(text(430, 201, "[]   (no error)", "tx", "middle", 12))
    return svg(232, "".join(b), "A list keeps its values. A generator is used up after one pass.", "m3")


def d_except():
    b = []
    b.append(box(0, 10, 170, 36, "bx"))
    b.append(text(85, 33, "Exception", "tx tb", "middle"))
    b.append(box(0, 96, 170, 36, "bx"))
    b.append(text(85, 119, "InsufficientFundsError", "tx", "middle", 12))
    b.append(arrow(85, 96, 85, 48, "m4"))
    b.append(text(95, 76, "is a kind of", "tx tm", "start", 11))
    b.append(box(220, 6, 220, 34, "bxw"))
    b.append(text(330, 28, "raise InsufficientFundsError", "tx", "middle", 12))
    b.append(arrow(330, 40, 330, 66, "m4"))
    b.append(box(220, 68, 220, 38, "bxa"))
    b.append(text(330, 92, "except Exception:", "tx tb", "middle", 13))
    b.append(text(450, 92, "MATCH", "tx ta tb", "start", 12))
    b.append(text(330, 124, "Python stops here. It prints: general", "tx ta", "middle", 12))
    b.append(box(220, 146, 220, 38, "bx", 8, True))
    b.append(text(330, 170, "except InsufficientFundsError:", "tx tm", "middle", 12))
    b.append(text(330, 200, "Never reached. No warning appears.", "tx tw", "middle", 12))
    return svg(214, "".join(b), "An error falls through except blocks from the top. The first match runs.", "m4")


def d_class():
    b = []
    b.append(box(0, 8, 210, 118, "bx"))
    b.append(text(105, 28, "Order object", "tx tb", "middle"))
    b.append(box(14, 38, 182, 26, "bx", 5))
    b.append(text(105, 56, "qty = 3", "tx", "middle"))
    b.append(box(14, 70, 182, 26, "bx", 5))
    b.append(text(105, 88, "unit_price = 10", "tx", "middle"))
    b.append(box(14, 102, 182, 18, "bxa", 5, True))
    b.append(text(105, 115, "total  (property: qty * unit_price)", "tx", "middle", 10))
    rows = [
        (8, "bxg", "order.total", "30   (no brackets)"),
        (62, "bxw", "order.total()", "TypeError: 30 is not callable"),
        (116, "bxg", "repr(order)", "Order('Acme', total=30)"),
        (170, "bxw", "__repr__ with no return", "TypeError: non-string"),
    ]
    for y, cls, a, c in rows:
        b.append(box(240, y, 280, 44, cls))
        b.append(text(252, y + 19, a, "tx tb", "start", 12))
        b.append(text(252, y + 36, c, "tx tm", "start", 11))
    b.append(arrow(210, 70, 238, 30, "m5"))
    b.append(arrow(210, 76, 238, 84, "m5"))
    b.append(arrow(210, 82, 238, 138, "m5"))
    return svg(226, "".join(b), "Reading a property without brackets gives its value. Brackets cause an error.", "m5")


def d_logical_order():
    b = []
    names = ["FROM", "WHERE", "GROUP BY", "HAVING", "SELECT", "ORDER BY"]
    notes = [["tables"], ["single", "rows"], ["makes", "groups"], ["whole", "groups"], ["aliases", "start here"], ["can use", "aliases"]]
    hl = {1, 3}
    for i, n in enumerate(names):
        x = i * 88
        b.append(box(x, 10, 78, 40, "bxa" if i in hl else "bx"))
        b.append(text(x + 39, 35, n, "tx tb", "middle", 12))
        for j, t in enumerate(notes[i]):
            b.append(text(x + 39, 72 + j * 14, t, "tx tm", "middle", 11))
        if i < 5:
            b.append(arrow(x + 78, 30, x + 88, 30, "m6"))
    b.append(text(0, 128, "Runs in this order. You type SELECT first, but it runs fifth.", "tx tm", "start", 12))
    b.append(box(0, 142, 250, 44, "bxa"))
    b.append(text(125, 161, "WHERE sees rows", "tx tb", "middle", 12))
    b.append(text(125, 178, "It cannot use AVG(): no groups yet.", "tx", "middle", 11))
    b.append(box(270, 142, 250, 44, "bxa"))
    b.append(text(395, 161, "HAVING sees groups", "tx tb", "middle", 12))
    b.append(text(395, 178, "It can use AVG(). Repeat the expression.", "tx", "middle", 11))
    return svg(200, "".join(b), "The logical order of SQL clauses: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY.", "m6")


def d_frames():
    b = []
    waits = [10, 50, 30, 70]
    for i, v in enumerate(waits):
        x = 10 + i * 124
        b.append(text(x + 55, 14, f"VisitID {i + 1}", "tx tm", "middle", 11))
        b.append(box(x, 20, 110, 36, "bx"))
        b.append(text(x + 55, 44, str(v), "tx tb", "middle", 15))
    # moving frame for row 3
    b.append(box(10, 66, 358, 10, "bxa", 4))
    b.append(text(10, 96, "Row 3 with  ROWS BETWEEN 2 PRECEDING AND CURRENT ROW", "tx ta tb", "start", 12))
    b.append(text(10, 113, "sees 10, 50, 30   average = 30", "tx", "start", 12))
    # default last_value frame for row 2
    b.append(box(10, 132, 234, 10, "bxw", 4))
    b.append(text(10, 162, "Row 2 with the default frame (ends at the current row)", "tx tw tb", "start", 12))
    b.append(text(10, 179, "LAST_VALUE sees 10, 50   it returns 50, not 70", "tx", "start", 12))
    # full frame
    b.append(box(10, 198, 482, 10, "bxg", 4))
    b.append(text(10, 228, "Fix: ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING", "tx tg tb", "start", 11))
    b.append(text(10, 245, "LAST_VALUE sees 10, 50, 30, 70   it returns 70 on every row", "tx", "start", 12))
    return svg(258, "".join(b), "Window frames over four rows: a moving frame, the default frame, and the full frame.", "m7")


def d_percentile():
    b = []
    xs = {10: 60, 20: 180, 30: 300, 40: 420}
    b.append(text(0, 16, "Values 10, 20, 30, 40", "tx tb"))
    b.append(line(30, 60, 490, 60, "ln"))
    for v, x in xs.items():
        b.append(f'<circle class="dot" cx="{x}" cy="60" r="7"/>')
        b.append(text(x, 40, str(v), "tx", "middle"))
    # 0.5
    b.append(text(0, 122, "Percentile 0.5", "tx tb", "start", 12))
    b.append(f'<circle class="dotg" cx="180" cy="60" r="12"/>')
    b.append(arrow(180, 150, 180, 76, "m8"))
    b.append(text(180, 168, "DISC = 20", "tx tg tb", "middle", 12))
    b.append(text(180, 183, "a real value", "tx tm", "middle", 11))
    b.append(f'<rect class="dia" x="234" y="54" width="12" height="12" transform="rotate(45 240 60)"/>')
    b.append(arrow(240, 150, 240, 76, "m8"))
    b.append(text(250, 168, "CONT = 25", "tx ta tb", "start", 12))
    b.append(text(250, 183, "blended: between 20 and 30", "tx tm", "start", 11))
    b.append(line(0, 200, W, 200, "ln"))
    b.append(text(0, 222, "Percentile 0.75", "tx tb", "start", 12))
    b.append(text(0, 242, "DISC = 30 (first value that reaches 75%).", "tx", "start", 12))
    b.append(text(0, 260, "CONT = 32.5 (a quarter of the way from 30 to 40).", "tx", "start", 12))
    return svg(272, "".join(b), "Number line showing PERCENTILE_CONT interpolating and PERCENTILE_DISC picking a real value.", "m8")


def d_rollup():
    b = []
    b.append(text(0, 14, "Detail rows   GROUPING(Ward) = 0", "tx tb", "start", 12))
    det = [("2024", "A", "100"), ("2024", "B", "200"), ("2025", "A", "300"), ("2025", "NULL", "50")]
    for i, (y, w, t) in enumerate(det):
        x = i * 130
        b.append(box(x, 22, 120, 34, "bx"))
        b.append(text(x + 60, 44, f"{y} | {w} | {t}", "tx", "middle", 12))
    b.append(text(520, 74, "2025 NULL is real data", "tx tm", "end", 11))
    b.append(arrow(130, 58, 130, 96, "m9"))
    b.append(arrow(390, 58, 390, 96, "m9"))
    b.append(text(150, 90, "Subtotals: GROUPING(Ward) = 1", "tx tb", "start", 12))
    b.append(box(40, 104, 180, 34, "bxa"))
    b.append(text(130, 126, "2024 | NULL | 300", "tx", "middle", 12))
    b.append(box(300, 104, 180, 34, "bxa"))
    b.append(text(390, 126, "2025 | NULL | 350", "tx", "middle", 12))
    b.append(arrow(130, 140, 250, 176, "m9"))
    b.append(arrow(390, 140, 270, 176, "m9"))
    b.append(box(170, 180, 180, 34, "bxg"))
    b.append(text(260, 202, "NULL | NULL | 650", "tx", "middle", 12))
    b.append(text(360, 202, "grand total", "tx tg tb", "start", 12))
    return svg(228, "".join(b), "ROLLUP adds year subtotal rows and one grand total row above the detail rows.", "m9")


def d_correlated():
    b = []
    b.append(text(0, 14, "Correlated subquery", "tx tw tb"))
    for i in range(5):
        y = 28 + i * 24
        b.append(box(0, y, 56, 18, "bx", 4))
        b.append(text(28, y + 13, f"row {i + 1}", "tx", "middle", 10))
        b.append(arrow(56, y + 9, 100, y + 9, "m10"))
        b.append(box(102, y, 130, 18, "bxw", 4))
        b.append(text(167, y + 13, "inner scan", "tx", "middle", 10))
    b.append(text(0, 158, "5 outer rows = 5 inner scans", "tx tm", "start", 12))
    b.append(text(270, 14, "Window function", "tx tg tb"))
    for i in range(5):
        y = 28 + i * 24
        b.append(box(270, y, 56, 18, "bx", 4))
        b.append(text(298, y + 13, f"row {i + 1}", "tx", "middle", 10))
    b.append(arrow(340, 34, 340, 140, "m10", "ar arg"))
    b.append(box(356, 64, 164, 52, "bxg"))
    b.append(text(438, 86, "one ordered pass", "tx tb", "middle", 12))
    b.append(text(438, 104, "over the data", "tx", "middle", 12))
    b.append(text(270, 158, "5 rows = 1 pass", "tx tm", "start", 12))
    b.append(line(0, 176, W, 176, "ln"))
    b.append(text(0, 198, "Your case study (2,325 rows)", "tx tb", "start", 12))
    b.append(box(0, 208, 250, 44, "bxw"))
    b.append(text(125, 227, "Before: 6,233,958 reads", "tx tb", "middle", 12))
    b.append(text(125, 244, "61,785 ms", "tx", "middle", 12))
    b.append(box(270, 208, 250, 44, "bxg"))
    b.append(text(395, 227, "After: 9,470 reads", "tx tb", "middle", 12))
    b.append(text(395, 244, "16 ms", "tx", "middle", 12))
    return svg(266, "".join(b), "A correlated subquery runs once per outer row. A window function makes one pass.", "m10")


# --------------------------------------------------------------------- videos
def v(title, channel, url, role, verified, note=""):
    return {"title": title, "channel": channel, "url": url, "role": role, "verified": verified, "note": note}


V_LISTING = "Title and link match a search listing. The video page could not be read, so views and length are unchecked."
V_PAGE = "Title and channel read from the video page."

# ---------------------------------------------------------------------- topics
TOPICS = [
    # ------------------------------------------------------------------ PYTHON
    {
        "id": "py-dict-count", "track": "Python", "title": "Count items with a dictionary", "minutes": 30,
        "summary": "A tally is a dictionary that counts how many times each value appears.",
        "picture": {"svg": d_dict_count(), "caption": "The tally after each order. The highlighted line changes at that step."},
        "predict": {
            "q": "The tally is empty. The next order has the status 'shipped'. Does the code add 1 to an existing count, or create a new count?",
            "reveal": "It creates a new count. The key 'shipped' is not in the tally yet, so the else branch sets it to 1."},
        "explain": [
            {"h": "What it is", "p": [
                "A dictionary stores pairs. Each pair has a key and a value.",
                "A tally is a dictionary where each key is an item and each value is a count.",
                "Use a tally to count orders by status, sales by region, or errors by type."]},
            {"h": "How it works", "p": [
                "Start with an empty dictionary.",
                "Read one row at a time.",
                "Take the key from the row.",
                "Ask if the key is already in the tally.",
                "If it is, add 1 to its count.",
                "If it is not, set its count to 1.",
                "After the loop, return the tally."]},
            {"h": "Common mistakes", "p": [
                "Check the tally, not the row. The test is: key in tally.",
                "A row has its own keys, such as 'id' and 'status'. A status value is never one of them. The test is always false and every count stays at 1.",
                "Put the return after the loop. A return inside the loop stops the function after the first row.",
                "Return the tally. Do not return the loop variable.",
                "End the def line with a colon."]}],
        "example": {"title": "Count orders by status", "code": (
            "def count_by_status(orders):\n    counts = {}\n    for order in orders:\n        status = order[\"status\"]\n"
            "        if status in counts:\n            counts[status] = counts[status] + 1\n        else:\n            counts[status] = 1\n"
            "    return counts\n\norders = [\n    {\"id\": 1, \"status\": \"shipped\"},\n    {\"id\": 2, \"status\": \"pending\"},\n"
            "    {\"id\": 3, \"status\": \"shipped\"},\n]\nprint(count_by_status(orders))"),
            "output": "{'shipped': 2, 'pending': 1}"},
        "qa": {"q": "What does the function return for the customers Acme, Birch, Acme, Acme?",
               "a": "{'Acme': 3, 'Birch': 1}. Acme is new on order 1, so its count is set to 1. Orders 3 and 4 find Acme in the tally, so the count goes to 2 and then 3. Birch is new once."},
        "videos": [v("Python Tutorial for Beginners 5: Dictionaries - Working with Key-Value Pairs", "Corey Schafer",
                     "https://www.youtube.com/watch?v=daefaLgNkw0", "Keys, values and lookups. Use it for the dictionary basics. It does not teach the counting pattern.", "listing", V_LISTING)],
        "compared": "Search also listed 'Python 3 Tutorial for Beginners #14 - Dictionaries' and 'Python Dictionaries (Visually Explained)'. Those pages were not opened. Corey Schafer was chosen for the clear key/value basics.",
        "build": {"task": "Write count_by_customer(orders) from a blank page. Each row looks like {'id': 1, 'customer': 'Acme'}. For the sample rows Acme, Birch, Acme it must return {'Acme': 2, 'Birch': 1}.",
                  "hint": "Start with counts = {} and a for loop. Then write the if and else.",
                  "check": "Run it on the sample. Then run it on an empty list. It must return {}."},
        "teach": "Explain the counting pattern in 5 sentences. Say what the code asks at each row. Write it for a person who has never seen code.",
        "mistakes": ["Wrote 'customer in order' instead of 'customer in count' (2026-10-26).", "Wrote 'return customer' inside the loop (2026-10-26).", "Missed the colon on the def line (2026-10-26)."],
        "selfCheck": [
            {"q": "Which test is correct: 'status in order' or 'status in counts'?", "a": "'status in counts'. The tally remembers what the code has seen. The row does not."},
            {"q": "Where does the return line go?", "a": "After the loop. Inside the loop, the function stops after the first row."}],
    },
    {
        "id": "py-mutable-default", "track": "Python", "title": "Mutable default arguments", "minutes": 30,
        "summary": "A default list is made once. All calls without that argument share it.",
        "picture": {"svg": d_mutable(), "caption": "Left: both calls use the same list. Right: each call makes its own list."},
        "predict": {
            "q": "def add_item(item, cart=[]) adds the item to cart and returns cart. You call add_item('Laptop'), then add_item('Mouse'). What does the second call return?",
            "reveal": "['Laptop', 'Mouse']. Both calls use the same list."},
        "explain": [
            {"h": "What it is", "p": [
                "Python sets a default value when it runs the def line. It does this one time.",
                "A list is mutable. A function can change it.",
                "If the default is a list, all calls that skip the argument use the same list."]},
            {"h": "How it works", "p": [
                "Python runs the line def add_item(item, cart=[]).",
                "Python makes one empty list and stores it with the function.",
                "Call 1 gives no cart. The function uses the stored list and adds 'Laptop'.",
                "Call 2 gives no cart. The function uses the same stored list. It now holds 'Laptop' and 'Mouse'."]},
            {"h": "The fix", "p": [
                "Use None as the default.",
                "Inside the function, test if cart is None.",
                "If it is, make a new list. Each call then gets its own list."]},
            {"h": "Common mistakes", "p": [
                "No error appears. The output is wrong, and only from the second call.",
                "The problem applies to lists, dictionaries and sets.",
                "The problem does not apply to numbers, strings or None. These cannot change in place."]}],
        "example": {"title": "The bug and the fix", "code": (
            "def add_item(item, cart=[]):\n    cart.append(item)\n    return cart\n\nprint(add_item(\"Laptop\"))\nprint(add_item(\"Mouse\"))\n\n"
            "def add_item_fixed(item, cart=None):\n    if cart is None:\n        cart = []\n    cart.append(item)\n    return cart\n\n"
            "print(add_item_fixed(\"Laptop\"))\nprint(add_item_fixed(\"Mouse\"))"),
            "output": "['Laptop']\n['Laptop', 'Mouse']\n['Laptop']\n['Mouse']"},
        "qa": {"q": "def log(msg, entries=[]) appends msg to entries and returns entries. You call log('a'), then log('b'). What does the second call return? How do you fix it?",
               "a": "['a', 'b']. Change the default to None. Inside the function write: if entries is None: entries = []."},
        "videos": [v("Python Tutorial: Clarifying the Issues with Mutable Default Arguments", "Corey Schafer",
                     "https://www.youtube.com/watch?v=_JGmemuINww", "Explains why the default is made once and shows how it fails. 16 minutes.", "page",
                     V_PAGE + " 39,544 views at the time of the check.")],
        "compared": "Compared: Corey Schafer (39,544 views, 16 min), Finxter AI Nuggets (311 views, 12 min), Sonar (58-second short, 425 views), Python Morsels (April 2025, length not readable). Corey Schafer was chosen for the longest explanation and the most views. This video is the follow-up to an earlier one by the same channel.",
        "build": {"task": "Write add_item(item, cart=None) so a call without a cart starts a new list.",
                  "hint": "Test with: if cart is None.",
                  "check": "Call it three times without a cart. No result may contain items from another call."},
        "teach": "Explain in 4 sentences why cart=[] is shared between calls. Use the words 'def line' and 'one list'.",
        "mistakes": ["Logged in the warm-up on 2026-09-30. Review it again."],
        "selfCheck": [
            {"q": "Does the same problem happen with a default of 0?", "a": "No. A number cannot change in place. Each call starts with 0."},
            {"q": "When does Python make the default list?", "a": "When it runs the def line, one time."}],
    },
    {
        "id": "py-generators", "track": "Python", "title": "Generators and lists", "minutes": 35,
        "summary": "A list keeps its values. A generator gives each value once, then it is empty.",
        "picture": {"svg": d_generators(), "caption": "A list can be read many times. A generator is used up after one full pass."},
        "predict": {
            "q": "gen = (p * 0.9 for p in prices). You run list(gen) two times. What does the second call return?",
            "reveal": "[]. The first call used all the values. A generator cannot go back, and Python raises no error."},
        "explain": [
            {"h": "What it is", "p": [
                "A list comprehension uses square brackets. It builds the full list in memory.",
                "A generator expression uses round brackets. It builds nothing at first. It gives one value when asked.",
                "A function with yield also returns a generator.",
                "A generator is a one-way pass. After the last value, it is empty."]},
            {"h": "How it works", "p": [
                "print(gen) shows a generator object. It does not show values.",
                "list(gen) asks for every value. The generator gives them and reaches the end.",
                "A second list(gen) finds no values. It returns []."]},
            {"h": "When to use each", "p": [
                "Use a list when you read the values more than once.",
                "Use a generator when you read the values once and the data is large.",
                "To read a generator twice, make a new one. Or save it one time with list(gen)."]},
            {"h": "Common mistakes", "p": [
                "Square and round brackets look similar. They behave differently.",
                "A second loop over a used generator does nothing. No error appears."]}],
        "example": {"title": "Generator expression and list comprehension", "code": (
            "prices = [10, 25, 8, 40]\n\ngen = (p * 0.9 for p in prices)\nprint(gen)\nprint(list(gen))\nprint(list(gen))\n\n"
            "lst = [p * 0.9 for p in prices]\nprint(list(lst))\nprint(list(lst))"),
            "output": "<generator object <genexpr> at 0x...>\n[9.0, 22.5, 7.2, 36.0]\n[]\n[9.0, 22.5, 7.2, 36.0]\n[9.0, 22.5, 7.2, 36.0]"},
        "qa": {"q": "gen = (n * 2 for n in [1, 2, 3]); first = list(gen); second = list(gen). What are first and second?",
               "a": "first is [2, 4, 6]. second is []. The first list() used all the values."},
        "videos": [v("Python Tutorial: Generators - How to use them and the benefits you receive", "Corey Schafer",
                     "https://www.youtube.com/watch?v=bD05uGo_sVI", "Covers generators and why they save memory. Use the yield examples.", "listing", V_LISTING)],
        "compared": "Search also listed 'Python Lists vs Generators: Memory Efficiency & Performance Explained' (CodeLucky, page read, at least 11 minutes) and a sentdex video on list comprehensions and generator expressions. Corey Schafer was chosen for depth on yield. The CodeLucky video is a shorter option for the list-versus-generator comparison.",
        "build": {"task": "Write prices_with_vat(prices, rate=0.2) as a generator function with yield. Then show that a second list() of the same generator returns [].",
                  "hint": "Use: for p in prices, then yield p * (1 + rate).",
                  "check": "prices_with_vat([10, 25]) gives [12.0, 30.0] the first time and [] the second time."},
        "teach": "Explain in 5 sentences why the second list(gen) is empty. Use the words 'one-way'.",
        "mistakes": ["Predicted that a list comprehension also returns [] on the second read (2026-10-06). It does not."],
        "selfCheck": [
            {"q": "Which brackets make a generator expression?", "a": "Round brackets ( )."},
            {"q": "Can you loop over a list twice?", "a": "Yes. A list keeps its values."}],
    },
    {
        "id": "py-except-order", "track": "Python", "title": "try/except and the order of except blocks", "minutes": 30,
        "summary": "Python runs the first except block that matches. Put specific errors first.",
        "picture": {"svg": d_except(), "caption": "An error is checked against each except block from the top. The first match runs."},
        "predict": {
            "q": "try: raise InsufficientFundsError(...). The first block is except Exception. The second block is except InsufficientFundsError. Which block runs?",
            "reveal": "The first block, except Exception. InsufficientFundsError is a kind of Exception, so the first block matches. The second block can never run."},
        "explain": [
            {"h": "What it is", "p": [
                "try runs code that can fail. except runs when the code raises an error.",
                "A custom exception is a class that you make. It inherits from Exception.",
                "Python checks each except block from top to bottom."]},
            {"h": "How it works", "p": [
                "The code raises an error.",
                "Python compares the error with the first except block.",
                "If the error matches, Python runs that block and ignores all other blocks.",
                "A match includes subclasses. InsufficientFundsError is a kind of Exception, so except Exception matches it."]},
            {"h": "The rule", "p": [
                "Put the most specific exceptions first.",
                "Put except Exception last, as the general catch.",
                "If a general block is first, the specific blocks after it can never run.",
                "else runs when no error is raised. finally always runs."]},
            {"h": "Common mistakes", "p": [
                "Python shows no warning for a block that can never run."]}],
        "example": {"title": "Wrong order and right order", "code": (
            "class InsufficientFundsError(Exception):\n    pass\n\n# Wrong order\ntry:\n    raise InsufficientFundsError(\"low\")\nexcept Exception:\n    print(\"general\")\n"
            "except InsufficientFundsError:\n    print(\"specific\")\n\n# Right order\ntry:\n    raise InsufficientFundsError(\"low\")\nexcept InsufficientFundsError:\n    print(\"specific\")\n"
            "except Exception:\n    print(\"general\")"),
            "output": "general\nspecific"},
        "qa": {"q": "try: int('abc'). The first block is except Exception: print('A'). The second block is except ValueError: print('B'). What prints? How do you fix it?",
               "a": "A prints. int('abc') raises ValueError, which is a kind of Exception, so the first block matches. Put except ValueError before except Exception."},
        "videos": [v("Python Tutorial: Using Try/Except Blocks for Error Handling", "Corey Schafer",
                     "https://www.youtube.com/watch?v=NIWwJbo-9_8", "How to handle specific exceptions, and how try, except, else and finally flow.", "page",
                     V_PAGE + " The page text does not say if the video teaches the order rule. The rule is on this page.")],
        "compared": "Search also listed several beginner series (for example 'Python Tutorial for Beginners 36/37') and a custom-exceptions video. Only the Corey Schafer page was opened. Corey Schafer was chosen for the clear control-flow explanation.",
        "build": {"task": "Write safe_ratio(a, b) that returns a / b. Use three except blocks: ZeroDivisionError returns 'Cannot divide by zero', TypeError returns 'Numbers only', and Exception returns 'Unexpected'.",
                  "hint": "Put ZeroDivisionError and TypeError first. Put Exception last.",
                  "check": "safe_ratio(1, 0) gives 'Cannot divide by zero'. safe_ratio('a', 2) gives 'Numbers only'. safe_ratio(1, 2) gives 0.5."},
        "teach": "Explain in 4 sentences why the order of except blocks matters.",
        "mistakes": ["Predicted 'specific' when the answer was 'general' (2026-10-12)."],
        "selfCheck": [
            {"q": "Is ZeroDivisionError a kind of Exception?", "a": "Yes. Built-in errors like this inherit from Exception."},
            {"q": "When does finally run?", "a": "Always, with or without an error."}],
    },
    {
        "id": "py-class-property", "track": "Python", "title": "Classes, @property and __repr__", "minutes": 40,
        "summary": "A property is read without brackets. __repr__ must return a string.",
        "picture": {"svg": d_class(), "caption": "Read a property without brackets. Brackets try to call the value."},
        "predict": {
            "q": "class Order has a method total marked @property that returns qty * unit_price. The order has qty 3 and unit_price 10. What does print(order.total()) do?",
            "reveal": "It raises TypeError: 'int' object is not callable. order.total already gives 30. The brackets then try to call 30 like a function."},
        "explain": [
            {"h": "What it is", "p": [
                "A class is a plan for objects. An object holds data in attributes.",
                "__init__ sets the attributes when you make the object.",
                "@property makes a method behave like an attribute. You read it without brackets.",
                "__repr__ returns the text that Python shows for the object."]},
            {"h": "How it works", "p": [
                "order = Order('Acme', 3, 10) calls __init__.",
                "order.total runs the total method and gives 30.",
                "Python works out the value each time you read it. If qty changes, total changes."]},
            {"h": "Rules", "p": [
                "Read a property without brackets.",
                "__init__ and __repr__ have two underscores on each side. A name with fewer underscores is an ordinary method. Python does not use it as the constructor.",
                "__repr__ must return a string. If it builds the string but has no return, Python raises TypeError.",
                "A subclass __init__ must accept every value its parent needs, plus its own. It passes the parent values to super().__init__()."]}],
        "example": {"title": "Order with a property and __repr__", "code": (
            "class Order:\n    def __init__(self, customer, qty, unit_price):\n        self.customer = customer\n        self.qty = qty\n        self.unit_price = unit_price\n\n"
            "    @property\n    def total(self):\n        return self.qty * self.unit_price\n\n    def __repr__(self):\n        return f\"Order({self.customer!r}, total={self.total})\"\n\n"
            "order = Order(\"Acme\", 3, 10)\nprint(order.total)\nprint(order)"),
            "output": "30\nOrder('Acme', total=30)"},
        "qa": {"q": "class Invoice has __repr__ with only this line: f\"Invoice({self.amount})\". There is no return. What does print(Invoice(250)) do?",
               "a": "It raises TypeError: __str__ returned non-string (type NoneType). Without return, the method gives None. Add return before the f-string."},
        "videos": [v("Python OOP Tutorial 6: Property Decorators - Getters, Setters, and Deleters", "Corey Schafer",
                     "https://www.youtube.com/watch?v=jCzT9XFZ5bw", "How @property lets a method act like an attribute.", "listing",
                     V_LISTING + " Several page reads of this link returned the same title, which matches the listing."),
                   v("Python OOP Tutorial 5: Special (Magic/Dunder) Methods", "Corey Schafer",
                     "https://www.youtube.com/watch?v=3ohzBxoFHAY", "Use for __repr__ and the other double-underscore methods.", "listing", V_LISTING)],
        "compared": "Search listed several Corey Schafer OOP videos plus GitHub notes on the series. Corey Schafer was chosen because the series builds classes step by step. Page details could not be read for either video, so no view counts are given.",
        "build": {"task": "Write class Invoice with __init__(self, amount, vat_rate), a property total (amount * (1 + vat_rate)), and a __repr__ that returns text like Invoice(250, total=300.0).",
                  "hint": "Do not put brackets after total. Put return in __repr__.",
                  "check": "Invoice(250, 0.2).total gives 300.0. print(Invoice(250, 0.2)) shows Invoice(250, total=300.0)."},
        "teach": "Explain in 5 sentences the difference between order.total and order.total().",
        "mistakes": ["Predicted 30 for order.total() (2026-10-12). It raises TypeError.", "Predicted the __repr__ without return would print normally (2026-09-30).", "Wrote __init without the closing underscores earlier in the course."],
        "selfCheck": [
            {"q": "Do you write brackets after a property?", "a": "No."},
            {"q": "What must __repr__ do at the end?", "a": "Return a string."}],
    },
    # --------------------------------------------------------------------- SQL
    {
        "id": "sql-where-having", "track": "SQL", "title": "WHERE, HAVING and the logical order", "minutes": 35,
        "summary": "WHERE filters rows before grouping. HAVING filters groups after grouping.",
        "picture": {"svg": d_logical_order(), "caption": "SQL Server runs the clauses in this order, not the order you type them."},
        "predict": {
            "q": "Table Visits has Ward and WaitMins. A: 10, 50. B: 20, 20. C: 90, 70. The query uses WHERE WaitMins > 15, GROUP BY Ward, HAVING AVG(WaitMins) > 30. Which wards come back?",
            "reveal": "A (average 50) and C (average 80). WHERE removes the visit of 10 minutes first. Then A has one visit of 50. B has an average of 20, so HAVING removes it."},
        "explain": [
            {"h": "What it is", "p": [
                "SQL Server runs the clauses in a fixed logical order. This is not the order you type.",
                "The order is FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY."]},
            {"h": "WHERE and HAVING", "p": [
                "WHERE filters single rows before grouping.",
                "WHERE cannot use an aggregate such as AVG. No groups exist yet.",
                "HAVING filters groups after GROUP BY.",
                "HAVING is the place to filter on an aggregate, for example AVG(WaitMins) > 30.",
                "Write the full expression in HAVING. The alias from SELECT does not exist yet."]},
            {"h": "Window functions", "p": [
                "A window function runs at the SELECT stage. WHERE and HAVING cannot see its alias.",
                "To filter on it, put the query in a CTE. Then filter in the outer query."]},
            {"h": "Common mistakes", "p": [
                "WHERE AVG(WaitMins) > 30 gives an error. Use HAVING.",
                "A bare column in SELECT that is not in GROUP BY gives an error. Wrap it in an aggregate such as SUM.",
                "In SQL Server, AVG of an integer column returns an integer. It drops the decimals. Cast the column to a decimal type if you need them."]}],
        "example": {"title": "Wards with a high average wait", "code": (
            "SELECT Ward, AVG(WaitMins) AS AvgWait\nFROM Visits\nWHERE WaitMins > 15\nGROUP BY Ward\nHAVING AVG(WaitMins) > 30\nORDER BY Ward;"),
            "output": "Ward | AvgWait\nA    | 50\nC    | 80"},
        "qa": {"q": "Show each ward with an average wait above 30 minutes. Count only visits longer than 15 minutes.",
               "a": "Use WHERE WaitMins > 15 for the rows. Use GROUP BY Ward. Use HAVING AVG(WaitMins) > 30 for the groups. The query in the example does this."},
        "videos": [],
        "videoPending": {"note": "No single video was verified for this topic. The Data with Baraa SQL course appeared in search, but no chapter or link was checked.",
                         "candidate": {"title": "SQL Bootcamp Playlist (2025) - Zero to Hero", "channel": "Data with Baraa (as listed in search)",
                                       "url": "https://www.youtube.com/playlist?list=PLNcg_FV9n7qZY_2eAtUzEUulNjTJREhQe"}},
        "compared": "Search for a WHERE versus HAVING video returned mostly written articles. No video was opened.",
        "build": {"task": "Table Visits. Write one query that shows, for each ward, the number of visits and the average wait. Ignore visits of 10 minutes or less. Keep only wards with 2 or more visits and an average wait above 25.",
                  "hint": "Row filters go in WHERE. Aggregate filters go in HAVING. You can use COUNT(*) in HAVING.",
                  "check": "With the sample data, only ward C returns: 2 visits, average 80."},
        "teach": "Explain in 5 sentences why WHERE cannot use AVG(). Use the words 'row' and 'group'.",
        "mistakes": ["Standing weakness: WHERE versus HAVING.", "Put a bare MinstoTriage in SELECT with GROUP BY and no SUM (2026-10-06)."],
        "selfCheck": [
            {"q": "Which clause runs first, WHERE or HAVING?", "a": "WHERE."},
            {"q": "Can HAVING use the alias that SELECT defines?", "a": "No. SELECT runs after HAVING. Repeat the full expression."}],
    },
    {
        "id": "sql-window-frames", "track": "SQL", "title": "Window frames and LAST_VALUE", "minutes": 40,
        "summary": "The frame decides which rows a window function can see. The default frame stops at the current row.",
        "picture": {"svg": d_frames(), "caption": "Ward A has waits 10, 50, 30, 70. The bar shows the rows the function sees."},
        "predict": {
            "q": "Ward A waits are 10, 50, 30, 70 in VisitID order. LAST_VALUE(WaitMins) OVER (PARTITION BY Ward ORDER BY VisitID) has no frame. What does row 2 return?",
            "reveal": "50. The default frame ends at the current row, so the last value it sees is the current row's value."},
        "explain": [
            {"h": "What it is", "p": [
                "A window function calculates over a set of rows. This set is the window.",
                "PARTITION BY splits the rows into groups.",
                "ORDER BY puts the rows in order inside each group.",
                "The frame picks which rows, around the current row, the function can see."]},
            {"h": "Frame syntax", "p": [
                "Write ROWS BETWEEN start AND end.",
                "The boundaries are UNBOUNDED PRECEDING, n PRECEDING, CURRENT ROW, n FOLLOWING and UNBOUNDED FOLLOWING.",
                "n must be a number that you type in the query. A variable does not work."]},
            {"h": "The default frame", "p": [
                "A window with ORDER BY and no frame uses RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW.",
                "FIRST_VALUE reads the start of the window. It works with this default.",
                "LAST_VALUE reads the end of the window. The end is the current row. So LAST_VALUE returns the current row's own value.",
                "To get the true last value, write ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING."]},
            {"h": "Useful frames", "p": [
                "ROWS BETWEEN 2 PRECEDING AND CURRENT ROW averages the current row and the two rows before it.",
                "The first rows have fewer than two earlier rows. The average uses the rows that exist.",
                "ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING sees every earlier row but not the current row."]}],
        "example": {"title": "Moving average and LAST_VALUE", "code": (
            "SELECT VisitID,\n       AVG(WaitMins) OVER (PARTITION BY Ward ORDER BY VisitID\n           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS Moving3,\n"
            "       LAST_VALUE(WaitMins) OVER (PARTITION BY Ward ORDER BY VisitID) AS LastDefault,\n"
            "       LAST_VALUE(WaitMins) OVER (PARTITION BY Ward ORDER BY VisitID\n           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS LastFull\nFROM W\nORDER BY VisitID;"),
            "output": "VisitID | Moving3 | LastDefault | LastFull\n1       | 10      | 10          | 70\n2       | 30      | 50          | 70\n3       | 30      | 30          | 70\n4       | 50      | 70          | 70"},
        "qa": {"q": "For row 3 of ward A (waits 10, 50, 30, 70), what does AVG(WaitMins) return with ROWS BETWEEN 2 PRECEDING AND CURRENT ROW?",
               "a": "30. The frame holds rows 1, 2 and 3: 10, 50 and 30. The sum is 90. The average is 30."},
        "videos": [v("SQL Value Window Functions | LEAD, LAG, FIRST_VALUE, LAST_VALUE | #SQL Course 25", "Data with Baraa",
                     "https://www.youtube.com/watch?v=Jag6Eb2i-bQ", "Main video for LAST_VALUE and FIRST_VALUE. 45 minutes.", "page", V_PAGE + " 79,777 views at the time of the check."),
                   v("SQL Aggregate Window Functions | COUNT, AVG, SUM, MAX, MIN | #SQL Course 23", "Data with Baraa",
                     "https://www.youtube.com/watch?v=OdnxoJitdAg", "Running totals and moving averages. 1 hour 7 minutes.", "page",
                     V_PAGE + " 121,740 views. The page text does not confirm that the frame syntax is taught. Check as you watch."),
                   v("Unlock SQL Power: Understanding ROWS BETWEEN UNBOUNDED PRECEDING and FOLLOWING", "The Analyst Mind",
                     "https://www.youtube.com/watch?v=R1iZ5WLLl-4", "A short video that is only about the ROWS BETWEEN frame. 9 minutes.", "page",
                     V_PAGE + " 696 views. The demo uses MySQL, not SQL Server.")],
        "compared": "Compared the Data with Baraa course videos (large audience, long) against a short frame-only video with a small audience. Baraa was chosen as the main source for LAST_VALUE. The short video is the quickest way to see the frame syntax.",
        "build": {"task": "Use table W (ward A waits 10, 50, 30, 70). Write one query. For each visit it must show two things. First, the average of this visit and the two visits before it. Second, the true last wait in the ward.",
                  "hint": "You need two window functions. The second one needs a full frame.",
                  "check": "The Moving3 column is 10, 30, 30, 50. The last-wait column is 70 on every row."},
        "teach": "Explain in 5 sentences why LAST_VALUE returns the current row with the default frame.",
        "mistakes": ["LAST_VALUE default frame is on the cheat sheet. Check it again before you use LAST_VALUE.", "Wrote 'current_row AND preceding' and 'N preceding' instead of 'UNBOUNDED PRECEDING AND 1 PRECEDING' (2026-09-30)."],
        "selfCheck": [
            {"q": "Which frame gives every earlier row but not the current row?", "a": "ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING."},
            {"q": "Can the number in '2 PRECEDING' be a variable?", "a": "No. It must be a number typed in the query."}],
    },
    {
        "id": "sql-percentile", "track": "SQL", "title": "PERCENTILE_CONT and PERCENTILE_DISC", "minutes": 30,
        "summary": "CONT blends two values. DISC returns a value that exists in the data.",
        "picture": {"svg": d_percentile(), "caption": "The values 10, 20, 30, 40. CONT can land between values. DISC always lands on one."},
        "predict": {
            "q": "The values are 10, 20, 30, 40. What does PERCENTILE_DISC(0.5) return?",
            "reveal": "20. Each value holds 25% of the rows. The share at or below 20 is 50%. That is the first value that reaches 0.5."},
        "explain": [
            {"h": "What it is", "p": [
                "A percentile is the value below which a given share of the data falls.",
                "The median is the 0.5 percentile.",
                "SQL Server has two functions: PERCENTILE_CONT and PERCENTILE_DISC."]},
            {"h": "PERCENTILE_CONT", "p": [
                "CONT means continuous. It blends the two nearest values.",
                "The position is p x (n - 1), counting from 0. For 4 values and p = 0.5, the position is 1.5. That is halfway between 20 and 30, so the result is 25.",
                "The result may be a number that is not in your data."]},
            {"h": "PERCENTILE_DISC", "p": [
                "DISC means discrete. It returns a value that exists in the column.",
                "Sort the values. Work out the share of rows at or below each value.",
                "Return the first value whose share reaches the percentile you asked for.",
                "For 0.5 on 10, 20, 30, 40 the shares are 25%, 50%, 75% and 100%. The first to reach 50% is 20."]},
            {"h": "Syntax", "p": [
                "Write PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY column) OVER (...).",
                "ORDER BY goes inside WITHIN GROUP. It names the column to measure.",
                "Add PARTITION BY inside OVER to get one result per group. The words PARTITION BY are required.",
                "A window function returns the same value on every row. Add DISTINCT to get one row per group."]},
            {"h": "Which one to use", "p": [
                "Use DISC when the answer must be a value that really happened, such as a wait time of a real patient.",
                "Use CONT when a smooth statistical estimate is acceptable."]}],
        "example": {"title": "Median and quartiles of 10, 20, 30, 40", "code": (
            "SELECT DISTINCT\n       PERCENTILE_CONT(0.5)  WITHIN GROUP (ORDER BY x) OVER () AS ContMedian,\n"
            "       PERCENTILE_DISC(0.5)  WITHIN GROUP (ORDER BY x) OVER () AS DiscMedian,\n"
            "       PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY x) OVER () AS ContQ3,\n"
            "       PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY x) OVER () AS DiscQ3\nFROM P;"),
            "output": "ContMedian | DiscMedian | ContQ3 | DiscQ3\n25         | 20         | 32.5   | 30"},
        "qa": {"q": "The values are 10, 20, 30, 40. What do PERCENTILE_CONT(0.75) and PERCENTILE_DISC(0.75) return?",
               "a": "32.5 and 30. For CONT the position is 0.75 x 3 = 2.25. That is a quarter of the way from 30 to 40. For DISC the share at or below 30 is 75%, so 30 is the first value that reaches 0.75."},
        "videos": [v("SQL | PERCENTILE_DISC and PERCENTILE_CONT | Finding Median and Quartiles in SQL | SQL Analytical functions", "Data Project Hub",
                     "https://www.youtube.com/watch?v=4Gr93tPMXeo", "Compares the two functions: one returns a stored value, one interpolates.", "page", V_PAGE + " Small channel. View count not readable.")],
        "reading": {"title": "PERCENTILE_CONT (Transact-SQL) - Microsoft Learn", "url": "https://learn.microsoft.com/en-us/sql/t-sql/functions/percentile-cont-transact-sql?view=sql-server-ver17", "note": "Official reference. Found in search; page not opened."},
        "compared": "Search for this topic returned mostly written guides. One video was found and its page was read. No larger creator was found for this topic, so the choice is limited.",
        "build": {"task": "Table Visits. Write a query that returns each ward with its median wait using PERCENTILE_DISC, and also using PERCENTILE_CONT.",
                  "hint": "Use OVER (PARTITION BY Ward) and DISTINCT.",
                  "check": "A: 10 and 30. B: 20 and 20. C: 70 and 80 (DISC then CONT)."},
        "teach": "Explain in 5 sentences when you would choose DISC over CONT. Give one example.",
        "mistakes": ["Answered 30 for PERCENTILE_DISC(0.5) on 10, 20, 30, 40 (2026-10-12). The answer is 20.", "Chose CONT for 'a time a real patient spent' (2026-10-12). It needs DISC.", "Wrote OVER (TriageCategory) without PARTITION BY (2026-10-06)."],
        "selfCheck": [
            {"q": "Which function can return a number that is not in the data?", "a": "PERCENTILE_CONT."},
            {"q": "Where does ORDER BY go?", "a": "Inside WITHIN GROUP, not inside OVER."}],
    },
    {
        "id": "sql-rollup-grouping", "track": "SQL", "title": "ROLLUP and GROUPING", "minutes": 40,
        "summary": "ROLLUP adds subtotal and grand total rows. GROUPING shows which rows are subtotals.",
        "picture": {"svg": d_rollup(), "caption": "Detail rows, then subtotals for each year, then one grand total."},
        "predict": {
            "q": "Table R has 4 rows: (2024, A, 100), (2024, B, 200), (2025, A, 300), (2025, NULL, 50). How many rows does GROUP BY ROLLUP (Yr, Ward) return?",
            "reveal": "7 rows. There are 4 detail rows, 2 year subtotals and 1 grand total."},
        "explain": [
            {"h": "What it is", "p": [
                "A normal GROUP BY gives one row for each group.",
                "ROLLUP adds subtotal rows and a grand total to the same result.",
                "ROLLUP (a, b) makes three levels: (a, b), then (a), then ()."]},
            {"h": "How it works", "p": [
                "Subtotal rows show NULL in the column that was rolled up.",
                "The order of columns matters. ROLLUP (Yr, Ward) gives a subtotal for each year. ROLLUP (Ward, Yr) gives a subtotal for each ward.",
                "Repeat the full expression in GROUP BY, for example YEAR(Arrived_DTTM). The alias does not exist yet.",
                "Every other column in SELECT must be inside an aggregate such as SUM."]},
            {"h": "GROUPING", "p": [
                "A real NULL in your data looks the same as a subtotal NULL.",
                "GROUPING(column) returns 1 when the NULL is a subtotal marker. It returns 0 when the value is real, even if the value is NULL.",
                "Give GROUPING the raw column name. Do not give it an alias or an aggregate.",
                "A year subtotal and the grand total both give GROUPING(Ward) = 1. Add GROUPING(Yr) to tell them apart."]}],
        "example": {"title": "Subtotals with labels", "code": (
            "SELECT Yr,\n       CASE WHEN GROUPING(Ward) = 1 THEN 'All wards'\n            ELSE ISNULL(Ward, 'Unknown') END AS WardLabel,\n"
            "       SUM(Mins) AS Total,\n       GROUPING(Ward) AS IsWardSubtotal\nFROM R\nGROUP BY ROLLUP (Yr, Ward);"),
            "output": "Yr   | WardLabel | Total | IsWardSubtotal\n2024 | A         | 100   | 0\n2024 | B         | 200   | 0\n2024 | All wards | 300   | 1\n2025 | A         | 300   | 0\n2025 | Unknown   | 50    | 0\n2025 | All wards | 350   | 1\nNULL | All wards | 650   | 1"},
        "qa": {"q": "In the output above, which rows have GROUPING(Ward) = 1?",
               "a": "The two year subtotals (300 and 350) and the grand total (650). The row (2025, Unknown, 50) has 0 because its NULL is real data."},
        "videos": [v("Rollup in SQL Server", "kudvenkat", "https://www.youtube.com/watch?v=HLTdfCtfIJs", "Subtotals and grand totals with ROLLUP, in SQL Server.", "page",
                     V_PAGE + " Length and views not readable."),
                   v("Grouping function in SQL Server", "kudvenkat", "https://www.youtube.com/watch?v=h25K5S998fA", "How GROUPING separates subtotal rows from real NULLs. 12 minutes 48 seconds.", "page",
                     V_PAGE + " 85,175 views at the time of the check.")],
        "compared": "Compared kudvenkat (SQL Server, two matching videos, 85,175 views on the GROUPING video) against a 5-minute Matador Software video on ROLLUP (7,505 views). kudvenkat was chosen because he covers both ROLLUP and GROUPING in SQL Server.",
        "build": {"task": "Table R. Write a query with ROLLUP (Yr, Ward) and SUM(Mins). Add a label column: 'All wards' for subtotal rows, 'Unknown' for a real NULL, and the ward name otherwise.",
                  "hint": "Use CASE WHEN GROUPING(Ward) = 1 ... and ISNULL for the real NULL.",
                  "check": "You get 7 rows. Only the row (2025, Unknown, 50) is labelled Unknown."},
        "teach": "Explain in 5 sentences why GROUPING is needed when the data can contain NULL.",
        "mistakes": ["Put a bare MinstoTriage in SELECT with no SUM (2026-10-06).", "Wrote OVER (Triagecatgeory): a misspelt column name and a missing PARTITION BY (2026-10-06)."],
        "selfCheck": [
            {"q": "What does GROUPING return for a subtotal row?", "a": "1."},
            {"q": "Does ROLLUP (Ward, Yr) give the same subtotals as ROLLUP (Yr, Ward)?", "a": "No. The first gives a subtotal for each ward. The second gives a subtotal for each year."}],
    },
    {
        "id": "sql-correlated-vs-window", "track": "SQL", "title": "Correlated subquery or window function", "minutes": 40,
        "summary": "A correlated subquery runs once per outer row. A window function makes one pass.",
        "picture": {"svg": d_correlated(), "caption": "The bottom boxes are your own measured result from Portfolio Project 1."},
        "predict": {
            "q": "A table has 2,325 rows. A correlated subquery refers to the outer row. How many times does SQL Server run the inner query?",
            "reveal": "Once for each outer row: 2,325 times. Your STATISTICS IO output showed Scan count 2325 on the Worktable."},
        "explain": [
            {"h": "What it is", "p": [
                "A correlated subquery uses a value from the outer query. SQL Server cannot calculate it one time and reuse it.",
                "It runs the inner query again for each outer row. This is called row by row processing (RBAR).",
                "The query looks like one set-based statement. It runs like a loop."]},
            {"h": "The window function", "p": [
                "A window function calculates the same result in one ordered pass.",
                "Turn the correlated conditions into window clauses. 'Same ward' becomes PARTITION BY Ward. 'Earlier visits' becomes ORDER BY VisitID with a frame that ends at 1 PRECEDING.",
                "Both versions return NULL for the first visit of each ward. There is nothing earlier to average."]},
            {"h": "Why the speed changes", "p": [
                "The correlated version scans the table many times. The work grows with the square of the row count.",
                "The window version reads the table once.",
                "In your case study, reads fell from 6,233,958 to 9,470. Time fell from 61,785 ms to 16 ms."]},
            {"h": "A second step you identified", "p": [
                "A covering index on (AdmittingWard, VisitID) with WaitTimeMinutes in INCLUDE supports the window query.",
                "You could not create it because of permissions. Record it as identified, not applied."]}],
        "example": {"title": "Same result, two methods", "code": (
            "-- Correlated subquery\nSELECT VisitID,\n       (SELECT AVG(v2.WaitMins) FROM V v2\n        WHERE v2.Ward = v.Ward AND v2.VisitID < v.VisitID) AS AvgPrior\nFROM V v ORDER BY VisitID;\n\n"
            "-- Window function\nSELECT VisitID,\n       AVG(WaitMins) OVER (PARTITION BY Ward ORDER BY VisitID\n           ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS AvgPrior\nFROM V ORDER BY VisitID;"),
            "output": "VisitID | AvgPrior\n1       | NULL\n2       | NULL\n3       | 10\n4       | 20\n5       | 40"},
        "qa": {"q": "Rewrite this correlated subquery as a window function: (SELECT MAX(v2.WaitMins) FROM V v2 WHERE v2.Ward = v.Ward AND v2.VisitID < v.VisitID).",
               "a": "MAX(WaitMins) OVER (PARTITION BY Ward ORDER BY VisitID ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING). For table V it gives NULL, NULL, 10, 30, 40."},
        "videos": [v("SQL Subqueries and Correlated Subqueries", "KnowHow Academy", "https://www.youtube.com/watch?v=nTSy4vVVq_o",
                     "Defines correlated subqueries and compares them with plain subqueries. For the window side, use the frames topic.", "page",
                     V_PAGE + " The page confirms a worked correlated example. Length not readable.")],
        "compared": "Search returned a short video titled 'Subquery vs Window Function - Which Wins?' and several written guides. A fuller video was chosen for the correlated side. No video on the full comparison was verified.",
        "build": {"task": "Table V. Count the earlier visits in the same ward for each visit. Write it as a correlated subquery with COUNT(*), then as a window function.",
                  "hint": "Use COUNT(*) OVER with the same PARTITION BY, ORDER BY and frame.",
                  "check": "Both give 0, 0, 1, 2, 1 for VisitID 1 to 5."},
        "teach": "Explain in 6 sentences why 2,325 rows took 62 seconds. Use the words 'once per row'.",
        "mistakes": ["Named LAG first when the task needed an aggregate window function (2026-09-30).", "Used PARTITION BY VisitID, which makes one group per row (2026-09-30)."],
        "selfCheck": [
            {"q": "What does PARTITION BY VisitID do if VisitID is unique?", "a": "It makes one group per row, so the window holds one row."},
            {"q": "Which frame excludes the current row?", "a": "ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING."}],
    },
]

SITE = {
    "title": "Data Engineering Study Site",
    "generated": date.today().isoformat(),
    "defaultStart": "2026-10-26",
    "defaultFinish": "2027-01-04",
    "milestones": [
        {"date": "2027-01-04", "label": "DE Zoomcamp cohort starts (January 2027, exact day to confirm)"},
        {"date": "2027-03-31", "label": "Zoomcamp ends (about 12 weeks later, estimate)"},
        {"date": "2027-06-21", "label": "Summer 2027: target for first Data Engineer role applications"},
    ],
}


def main(out_dir):
    import os
    os.makedirs(os.path.join(out_dir, "data"), exist_ok=True)
    for i, t in enumerate(TOPICS, 1):
        t["num"] = i
    import mixed_tasks, py_mixed
    mixed = mixed_tasks.run_all()
    mixed.update(py_mixed.run_all())
    for t in TOPICS:
        t["mixed"] = mixed.get(t["id"], [])
    import subprocess
    for t in TOPICS:
        mp4 = os.path.join(out_dir, "videos", t["id"] + ".mp4")
        if os.path.exists(mp4):
            sec = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4],
                                       capture_output=True, text=True).stdout.strip() or 0)
            t["ownVideo"] = {"src": "videos/%s.mp4" % t["id"], "poster": "videos/%s.jpg" % t["id"], "minutes": max(1, round(sec / 60))}
    js = "window.SITE = " + json.dumps(SITE, ensure_ascii=False, indent=1) + ";\n"
    js += "window.TOPICS = " + json.dumps(TOPICS, ensure_ascii=False, indent=1) + ";\n"
    with open(os.path.join(out_dir, "data", "topics.js"), "w", encoding="utf-8") as f:
        f.write(js)
    print(f"Wrote {len(TOPICS)} topics")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
