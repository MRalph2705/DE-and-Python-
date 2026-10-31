"""Module 2 lessons, part B: type hints, logging, pytest, dates and times.
Every example and mixed task is RUN when the site is built. Claims are asserted in CHECKS / CHECKS_HAS."""
from build_topics import box, text, arrow, line, svg


def C(s):
    return s.strip("\n")


# ------------------------------------------------------------------ diagrams
def d_typing():
    b = []
    b.append(box(0, 40, 170, 60, "bxg"))
    b.append(text(85, 62, "report.py", "tx tb", "middle", 12))
    b.append(text(85, 82, "def add_vat(price: float)", "tx", "middle", 11))
    b.append(arrow(170, 60, 268, 28, "m2d")); b.append(arrow(170, 82, 268, 124, "m2d"))
    b.append(box(270, 6, 250, 50, "bxa"))
    b.append(text(395, 26, "python report.py", "tx tb", "middle", 12))
    b.append(text(395, 44, "ignores hints, runs the code", "tx", "middle", 11))
    b.append(box(270, 100, 250, 60, "bxw"))
    b.append(text(395, 120, "mypy report.py  (before running)", "tx tb", "middle", 12))
    b.append(text(395, 140, "reads hints, reports mismatches", "tx", "middle", 11))
    b.append(text(0, 186, "A hint is a promise. Only a checker holds you to it.", "tx tb", "start", 12))
    return svg(200, "".join(b), "Python ignores type hints when it runs. mypy reads them and reports mismatches before you run.", "m2d")


def d_logging():
    b = []
    levels = [("DEBUG", 10, "bx"), ("INFO", 20, "bxg"), ("WARNING", 30, "bxa"), ("ERROR", 40, "bxa"), ("CRITICAL", 50, "bxa")]
    for i, (n, v, cls) in enumerate(levels):
        y = 8 + i * 38
        b.append(box(0, y, 190, 30, cls))
        b.append(text(14, y + 20, n, "tx tb", "start", 12))
        b.append(text(176, y + 20, str(v), "tx tm", "end", 12))
    b.append(line(0, 45, 210, 45, "ln"))
    b.append(text(218, 40, "INFO and above are shown", "tx tb", "start", 11))
    b.append(text(218, 26, "hidden", "tx tm", "start", 11))
    b.append(text(218, 100, "log.info('loaded %s rows', n)", "tx", "start", 11))
    b.append(text(218, 120, "INFO:etl:loaded 2 rows", "tx tg tb", "start", 11))
    b.append(text(218, 160, "log.exception('failed')", "tx", "start", 11))
    b.append(text(218, 180, "ERROR line + the traceback", "tx tw tb", "start", 11))
    return svg(206, "".join(b), "Five log levels. A set level hides everything below it.", "m2e")


def d_pytest():
    b = []
    b.append(box(0, 8, 170, 44, "bxg")); b.append(text(85, 26, "etl.py", "tx tb", "middle", 12)); b.append(text(85, 43, "band(), clean_amount()", "tx", "middle", 11))
    b.append(box(0, 70, 170, 66, "bxa")); b.append(text(85, 88, "test_etl.py", "tx tb", "middle", 12))
    b.append(text(85, 106, "def test_band(): assert ...", "tx", "middle", 11)); b.append(text(85, 124, "def test_load(tmp_path): ...", "tx", "middle", 11))
    b.append(arrow(85, 70, 85, 54, "m2f"))
    b.append(text(98, 64, "imports", "tx tm", "start", 11))
    b.append(arrow(170, 103, 238, 103, "m2f"))
    b.append(box(240, 78, 130, 50, "bxw")); b.append(text(305, 100, "pytest -q", "tx tb", "middle", 12)); b.append(text(305, 118, "finds test_*", "tx", "middle", 11))
    b.append(arrow(370, 103, 410, 103, "m2f"))
    b.append(box(412, 82, 108, 42, "bxg")); b.append(text(466, 108, "6 passed", "tx tb", "middle", 12))
    b.append(text(0, 164, "Names that start with test_ are tests. Other names are ignored.", "tx tb", "start", 12))
    return svg(180, "".join(b), "pytest finds test files and test functions, runs them, and reports how many passed.", "m2f")


def d_datetime():
    b = []
    b.append(text(0, 20, "London wall clock", "tx tb", "start", 12))
    b.append(box(0, 28, 200, 40, "bxa")); b.append(text(100, 52, "Sat 28 Mar 12:00  (UTC+0)", "tx", "middle", 12))
    b.append(arrow(200, 48, 318, 48, "m2g")); b.append(text(260, 40, "+ 1 day", "tx tm", "middle", 11))
    b.append(box(320, 28, 200, 40, "bxa")); b.append(text(420, 52, "Sun 29 Mar 12:00  (UTC+1)", "tx", "middle", 12))
    b.append(text(0, 108, "The same two moments in UTC", "tx tb", "start", 12))
    b.append(box(0, 116, 200, 40, "bxg")); b.append(text(100, 140, "28 Mar 12:00 UTC", "tx", "middle", 12))
    b.append(arrow(200, 136, 318, 136, "m2g")); b.append(text(260, 128, "23 hours", "tx tw tb", "middle", 11))
    b.append(box(320, 116, 200, 40, "bxg")); b.append(text(420, 140, "29 Mar 11:00 UTC", "tx", "middle", 12))
    b.append(text(0, 184, "The clocks went forward on 29 March. One calendar day was only 23 hours.", "tx tb", "start", 12))
    b.append(text(0, 202, "Store UTC. Convert to local time only when you show it.", "tx", "start", 12))
    return svg(216, "".join(b), "Adding one day on a London clock across the March change gives a 23 hour gap in UTC.", "m2g")


# ------------------------------------------------------------------ lesson texts
TYPING_CODE = C(r"""
VAT_RATE = 0.2


def add_vat(price: float, rate: float = VAT_RATE) -> float:
    \"\"\"Return the price with VAT added.\"\"\"
    return price * (1 + rate)


def find_customer(orders: list[dict], customer: str) -> dict | None:
    \"\"\"Return the first order for the customer, or None when there is none.\"\"\"
    for order in orders:
        if order["customer"] == customer:
            return order
    return None


print(add_vat(10))
print(add_vat("10", 2))
found = find_customer([{"customer": "Acme", "amount": 5}], "Acme")
print(found["amount"])
""".replace('\\"', '"'))

LOGGING_CODE = C(r"""
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
log = logging.getLogger("etl")


def load(rows):
    bad = 0
    for row in rows:
        try:
            float(row["amount"])
        except ValueError:
            bad = bad + 1
            log.warning("bad amount %r in row %s", row["amount"], row["id"])
    log.info("loaded %s of %s rows", len(rows) - bad, len(rows))
    return len(rows) - bad


log.debug("this line is hidden")
rows = [{"id": "1", "amount": "120"}, {"id": "2", "amount": "abc"}, {"id": "3", "amount": "80"}]
load(rows)""")

ETL_PY = C(r"""
def clean_amount(text):
    return float(text.strip().replace(",", ""))


def band(amount):
    if amount >= 100:
        return "large"
    if amount >= 50:
        return "medium"
    return "small"


def load_amounts(path):
    with open(path) as f:
        return [clean_amount(line) for line in f if line.strip()]""")

TEST_PY = C(r"""
import pytest
from etl import band, clean_amount, load_amounts


def test_clean_amount():
    assert clean_amount(" 1,234.50 ") == 1234.5


@pytest.mark.parametrize("amount, expected", [(120, "large"), (60, "medium"), (10, "small")])
def test_band(amount, expected):
    assert band(amount) == expected


def test_bad_text_raises():
    with pytest.raises(ValueError):
        clean_amount("abc")


def test_load_amounts(tmp_path):
    path = tmp_path / "amounts.txt"
    with open(path, "w") as f:
        f.write("10\n20.5\n\n")
    assert load_amounts(path) == [10.0, 20.5]


def helper_not_a_test():
    assert False""")


LESSONS = [
 {"id": "py-typing", "track": "Python", "title": "Type hints", "minutes": 35,
  "summary": "A type hint says what a function expects and returns. A checker finds mismatches before you run.",
  "teaches": ["type-hints", "optional-none", "generic-hints", "mypy"],
  "uses": ["def", "return", "params-defaults", "dataclass", "annotation", "none", "list", "dict", "tuple", "import", "print", "f-string", "str", "int", "float", "if"],
  "picture": {"svg": d_typing(), "caption": "Python runs the code and ignores hints. mypy reads the hints and reports problems first."},
  "predict": {"q": C("""
def double(n: int) -> int:
    return n * 2

print(double("ab"))
Python 3 runs this. The hint says n is an int. What does it print?"""), "reveal": "abab. Python does not check the hint. The text 'ab' times 2 is 'abab'. The mistake stays hidden."},
  "explain": [
   {"h": "What it is", "p": [
     "A type hint is a note about the type of a value. You write it after a colon: price: float.",
     "-> float after the brackets is the hint for the return value.",
     "Python does not check hints when the code runs. Wrong code still runs.",
     "A checker such as mypy reads the hints and reports mismatches. It does not run your code."]},
   {"h": "Common hints", "p": [
     "Simple types: int, float, str, bool.",
     "Lists and dicts: list[str] is a list of text. dict[str, float] is a dict with text keys and float values.",
     "A tuple of fixed shape: tuple[int, str].",
     "A value that can be None: dict | None. This needs Python 3.10 or newer. Older code writes Optional[dict]."]},
   {"h": "Why a data engineer uses them", "p": [
     "A function with hints states its inputs and its output. A reader does not have to guess.",
     "mypy finds the case where a function can return None and the caller forgets to check.",
     "Editors use hints to suggest names and to warn you.",
     "Dataclasses and many data libraries read hints. You already used them in the dataclass lesson."]},
   {"h": "Run mypy", "p": [
     "Install it in your virtual environment: pip install mypy.",
     "Run it on a file: mypy report.py. It prints one line for each problem, with the line number.",
     "On the example below, mypy reports line 18 and line 20. Line 18 passes a str where a float is expected. Line 20 uses the result without a check for None.",
     "Fix line 20 with if found is not None: before you use found."]},
   {"h": "Rules", "p": [
     "Add hints to function parameters and return values first. Skip hints on simple local variables.",
     "Do not fight the checker with the word Any. Fix the code or the hint.",
     "Hints are a promise. They are not a test. You still need tests."]}],
  "example": {"title": "Hints that Python ignores", "code": TYPING_CODE},
  "qa": {"q": C("""
def find_customer(orders: list[dict], customer: str) -> dict | None:
    ...
result = find_customer(orders, "Zed")
print(result["amount"])
Zed is not in orders. What happens when you run this? What does mypy say before you run it?"""), "a": "At run time it raises TypeError: 'NoneType' object is not subscriptable, because the function returned None. mypy reports Value of type 'dict[Any, Any] | None' is not indexable, before you run anything. Fix it with if result is not None:."},
  "build": {"task": "From a blank page write a dataclass Line with sku (str), qty (int) and price (float). Write total(lines: list[Line]) -> float that returns the sum of qty * price. Write find_line(lines: list[Line], sku: str) -> Line | None. Print the total for two lines. Print find_line for a missing sku and check the result with is None before you read it. Run mypy on the file.",
            "hint": "Install mypy with pip install mypy. Use if line is None: print('not found') else: print(line.qty).",
            "check": "The file runs and mypy prints: Success: no issues found in 1 source file."},
  "teach": "Explain in 5 sentences why Python runs code with wrong hints and what mypy adds.",
  "mistakes": [],
  "selfCheck": [{"q": "Does Python stop a wrong type hint at run time?", "a": "No. Hints are not checked when the code runs."},
                {"q": "How do you write a hint for a dict or None?", "a": "dict | None on Python 3.10 or newer."},
                {"q": "What does mypy do?", "a": "It reads the hints and reports mismatches without running the code."}]},

 {"id": "py-logging", "track": "Python", "title": "Logging", "minutes": 35,
  "summary": "Logging records what a job did, with a level for each message. It replaces print in real jobs.",
  "teaches": ["logging-levels", "basicconfig", "getlogger", "lazy-format", "log-exception"],
  "uses": ["import", "def", "return", "try-except", "loop-for", "dict", "str", "int", "float", "print", "if"],
  "picture": {"svg": d_logging(), "caption": "Each message has a level. The level you set decides which messages appear."},
  "predict": {"q": C("""
import logging
logging.info("hello")
logging.warning("careful")
You have not set up anything. What appears?"""), "reveal": "Only WARNING:root:careful appears. The default level is WARNING, so the info message is hidden. The text goes to the error stream, not to normal output."},
  "explain": [
   {"h": "Why not print", "p": [
     "A job that runs at night has nobody watching. You read its record the next morning.",
     "print has no levels and no names. You cannot turn it down when the job is noisy.",
     "logging gives each message a level, a name and an optional time. You choose where it goes."]},
   {"h": "Levels", "p": [
     "DEBUG for detail while you build. INFO for normal progress. WARNING for a problem you handled.",
     "ERROR for a failure. CRITICAL for a failure that stops the whole job.",
     "You set a level. Messages below that level are hidden."]},
   {"h": "Set up once", "p": [
     "Call logging.basicConfig(...) once, at the start of the program.",
     "level=logging.INFO shows INFO and above. format says what each line looks like.",
     "stream=sys.stdout sends the lines to normal output. filename='etl.log' sends them to a file.",
     "log = logging.getLogger('etl') gives you a named logger. Use the same name for one part of the job."]},
   {"h": "Write good messages", "p": [
     "Write log.warning('bad amount %r in row %s', value, row_id). Do not build the text with an f-string.",
     "Logging fills in the %r and %s only if the message is shown. That saves work.",
     "Put numbers in the message: how many rows were read, how many were rejected.",
     "In an except block, call log.exception('failed'). It adds the full traceback. log.error does not."]},
   {"h": "Rules", "p": [
     "Do not log passwords or customer data.",
     "Do not call basicConfig in a library or in a function. Call it once in the main program.",
     "Log at the start and the end of each step, with row counts."]}],
  "example": {"title": "Count and log the bad rows", "code": LOGGING_CODE},
  "qa": {"q": C("""
try:
    1 / 0
except ZeroDivisionError:
    log.error("failed")
What is missing compared with log.exception("failed")? """), "a": "The traceback. log.exception writes the same message at ERROR level and adds the full traceback. log.error writes only the message."},
  "build": {"task": "From a blank page take a function that reads a list of order dicts and checks each amount. Add logging: INFO at the start with the row count, WARNING for each negative amount (with the row id), and INFO at the end with the number of good rows. Set the level to INFO and send the lines to normal output. Run it with one negative row. Then change the level to WARNING and run it again.",
            "hint": "Call logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s %(message)s') once. Use %s in the messages.",
            "check": "With INFO you see three kinds of lines. With WARNING you see only the warning line."},
  "teach": "Explain in 5 sentences why a nightly job should log with levels and not print.",
  "mistakes": [],
  "selfCheck": [{"q": "Which level is the default?", "a": "WARNING. INFO and DEBUG are hidden until you set a lower level."},
                {"q": "Why write log.info('rows %s', n) and not log.info(f'rows {n}')?", "a": "Logging builds the text only if the message is shown. It also keeps the message pattern constant."},
                {"q": "Which call adds the traceback inside an except block?", "a": "log.exception(...)."}]},

 {"id": "py-pytest", "track": "Python", "title": "Testing with pytest", "minutes": 45,
  "summary": "A test is a small function with assert. pytest finds the tests, runs them and counts the passes.",
  "teaches": ["assert", "pytest-discovery", "parametrize", "pytest-raises", "tmp-path", "approx"],
  "uses": ["def", "return", "import", "import-module", "file-open", "try-except", "list", "float", "str", "if", "venv"],
  "picture": {"svg": d_pytest(), "caption": "pytest finds test_ files and test_ functions. Everything else is ignored."},
  "predict": {"q": C("""
assert 2 + 2 == 5
What happens when Python runs this line?"""), "reveal": "It raises AssertionError. assert checks a claim. If the claim is False, the program stops with an error. If the claim is True, nothing happens."},
  "explain": [
   {"h": "What it is", "p": [
     "A test runs your code on a known input and checks the result.",
     "assert is the check: assert band(120) == 'large'. A False claim raises AssertionError.",
     "pytest is a tool that finds your tests, runs them and shows which passed.",
     "Install it in your virtual environment: pip install pytest."]},
   {"h": "How pytest finds tests", "p": [
     "It looks for files named test_*.py. It runs functions named test_*.",
     "Other names are ignored. A helper function that does not start with test_ is never run.",
     "Run it in the project folder: pytest -q. The -q option keeps the output short.",
     "A dot means one test passed. F means one failed."]},
   {"h": "Useful tools", "p": [
     "@pytest.mark.parametrize runs one test with many inputs. Each input counts as one test.",
     "with pytest.raises(ValueError): checks that the code inside raises that error.",
     "tmp_path is a built-in folder for one test. Add a name with tmp_path / 'file.txt'. pytest deletes it later.",
     "pytest.approx(0.3) compares floats. 0.1 + 0.2 == 0.3 is False, because floats are not exact."]},
   {"h": "Rules", "p": [
     "Test the code that holds your rules: cleaning, banding, parsing, joins.",
     "One test checks one idea. Give it a name that says what it checks.",
     "Write a test for each bug you find. The bug then cannot come back."]}],
  "example": {"title": "A module and its tests", "code": "# etl.py\n" + ETL_PY + "\n\n# test_etl.py\n" + TEST_PY,
              "script": {"display_only": True, "files": {"etl.py": ETL_PY + "\n", "test_etl.py": TEST_PY + "\n"},
                         "cmd": ["-m", "pytest", "-q", "-p", "no:cacheprovider"], "show": "pytest -q", "tidy": True}},
  "qa": {"q": "A test file has five def lines. Four names start with test_. One is helper_not_a_test. One of the four tests uses parametrize with three inputs. How many tests does pytest run?",
         "a": "Six. The helper is ignored. The three plain tests count once each. The parametrized test counts three times. 3 + 3 = 6."},
  "build": {"task": "From a blank page write a small file rules.py with two functions from your earlier lessons, for example band(amount) and a cleaning function. Write test_rules.py. It needs at least one plain test, one parametrize test with three inputs and one pytest.raises test. Run pytest -q.",
            "hint": "Put both files in the same folder. In the test file write from rules import band. Name each test function test_something.",
            "check": "pytest -q prints a line of dots and then N passed, where N counts every parametrized input."},
  "teach": "Explain in 5 sentences how pytest decides what to run and what a dot means.",
  "mistakes": [],
  "selfCheck": [{"q": "What does assert do when the claim is False?", "a": "It raises AssertionError."},
                {"q": "Does pytest run a function called check_band?", "a": "No. Only names that start with test_ are run."},
                {"q": "Why use pytest.approx for floats?", "a": "Floats are not exact. approx allows a tiny difference."}]},

 {"id": "py-datetime", "track": "Python", "title": "Dates, times and time zones", "minutes": 45,
  "summary": "Parse text into dates, add time with timedelta, and keep time zones correct. Store UTC.",
  "teaches": ["datetime-types", "strptime-strftime", "timedelta", "tz-aware", "zoneinfo", "utc-store"],
  "uses": ["import", "def", "f-string", "str", "int", "list", "sorted", "loop-for", "try-except", "comparison", "dict", "csv", "lambda", "sort-key", "print"],
  "picture": {"svg": d_datetime(), "caption": "Adding one day on a London clock across the March change is 23 real hours."},
  "predict": {"q": C("""
from datetime import datetime
datetime.strptime("27/10/2026", "%m/%d/%Y")
What happens?"""), "reveal": "It raises ValueError: time data '27/10/2026' does not match format '%m/%d/%Y'. The format says month first. There is no month 27."},
  "explain": [
   {"h": "The types", "p": [
     "date holds a day. datetime holds a day and a time. timedelta holds a length of time.",
     "date(2026, 12, 25) - date(2026, 10, 27) gives a timedelta. Its .days is 59.",
     "datetime + timedelta(days=7) gives a new datetime. The original does not change."]},
   {"h": "Text to date and back", "p": [
     "strptime reads text: datetime.strptime('27/10/2026 14:30', '%d/%m/%Y %H:%M').",
     "strftime writes text: d.strftime('%Y-%m-%d').",
     "%d is the day. %m is the month. %Y is the four digit year. %H is the hour. %M is the minute.",
     "A wrong format raises ValueError. Write the format to match the text exactly.",
     "ISO text such as 2026-10-27T14:30:00+00:00 is the safest format. Use fromisoformat and isoformat."]},
   {"h": "Naive and aware", "p": [
     "A naive datetime has no time zone. An aware datetime has one.",
     "You cannot compare a naive and an aware value. Python raises TypeError.",
     "Use zoneinfo for zones: ZoneInfo('Europe/London'). On Windows run pip install tzdata once.",
     "datetime.now(timezone.utc) gives the current time as an aware UTC value."]},
   {"h": "Daylight saving", "p": [
     "UK clocks go forward on the last Sunday of March. In 2026 that is 29 March.",
     "Adding timedelta(days=1) to an aware London time moves the clock by one calendar day.",
     "The gap in real time can be 23 hours. Convert both values to UTC to measure real time.",
     "Subtracting two values with the same zone uses the clock. Subtracting values from different zones uses real time."]},
   {"h": "Rules for data jobs", "p": [
     "Store and move times in UTC. Convert to local time only when you show them.",
     "Keep the time zone with the data. A time without a zone is a guess.",
     "Name the format for each source file. Day first and month first look the same for the 1st to the 12th."]}],
  "example": {"title": "Parse, add, convert", "code": C(r"""
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

d = datetime.strptime("27/10/2026 14:30", "%d/%m/%Y %H:%M")
print(d, d.strftime("%Y-%m-%d"))
print(d + timedelta(days=7))
print((date(2026, 12, 25) - date(2026, 10, 27)).days)

london = ZoneInfo("Europe/London")
start = datetime(2026, 3, 28, 12, 0, tzinfo=london)
nxt = start + timedelta(days=1)
print(start)
print(nxt)
print(nxt - start)
print(nxt.astimezone(timezone.utc) - start.astimezone(timezone.utc))
print(nxt.astimezone(timezone.utc))""")},
  "qa": {"q": C("""
from datetime import datetime, timezone
a = datetime(2026, 10, 27, 12, 0)
b = datetime(2026, 10, 27, 13, 0, tzinfo=timezone.utc)
print(a < b)
What does this do? Why?"""), "a": "It raises TypeError: can't compare offset-naive and offset-aware datetimes. a has no time zone. b has one. Give a a zone first, for example tzinfo=timezone.utc."},
  "build": {"task": "From a blank page: two London times are '28/03/2026 12:00' and '29/03/2026 12:00' (day first). Parse both. Make them aware with ZoneInfo('Europe/London'). Convert both to UTC. Print the hours between them. Then print the first time in New York time as ISO text.",
            "hint": "Use strptime, then .replace(tzinfo=london). Subtract the UTC values and use .total_seconds() / 3600.",
            "check": "The gap is 23.0 hours. The New York time of the first value is 2026-03-28T08:00:00-04:00."},
  "teach": "Explain in 5 sentences why you store times in UTC.",
  "mistakes": [],
  "selfCheck": [{"q": "What is the difference between a naive and an aware datetime?", "a": "An aware datetime carries a time zone. A naive one does not."},
                {"q": "How long is a London day when the clocks go forward?", "a": "23 hours."},
                {"q": "Which format text reads 27/10/2026 as day first?", "a": "%d/%m/%Y."}]},
]


# ------------------------------------------------------------------ mixed tasks
MIXED = {
 "py-typing": [
  {"title": "A. Add hints to a small program", "setup": "",
   "task": "Add type hints to every parameter and return value. Then run the code. average takes a list of floats and returns a float. label takes a float and returns text: 'high' for 100 or more, otherwise 'low'. Print average([80.0, 120.0]) and its label.",
   "hint": "def average(values: list[float]) -> float. Use sum(values) / len(values).",
   "answer": C(r"""
def average(values: list[float]) -> float:
    return sum(values) / len(values)


def label(value: float) -> str:
    if value >= 100:
        return "high"
    return "low"


avg = average([80.0, 120.0])
print(avg, label(avg))""")},
  {"title": "B. Handle the None result", "setup": "",
   "task": "find_price(prices, sku) returns the price or None. The code below crashes for a missing sku. Add a check so it prints 'no price' for a missing sku, and the price for a known one. Update the hint on the return value.",
   "broken": C(r"""
def find_price(prices: dict[str, float], sku: str) -> float:
    return prices.get(sku)


prices = {"A1": 2.5}
print(find_price(prices, "A1") * 2)
print(find_price(prices, "Z9") * 2)"""),
   "hint": "The return hint must be float | None. Use price = find_price(...), then if price is None.",
   "answer": C(r"""
def find_price(prices: dict[str, float], sku: str) -> float | None:
    return prices.get(sku)


prices = {"A1": 2.5}
for sku in ["A1", "Z9"]:
    price = find_price(prices, sku)
    if price is None:
        print("no price")
    else:
        print(price * 2)""")},
  {"title": "C. A hint that does not protect you", "setup": "",
   "broken": C(r"""
def pack(qty: int) -> int:
    return qty * 3


print(pack("4"))"""),
   "task": "Say what this prints, and why Python does not stop it. Fix the call so the result is 12.",
   "hint": "Convert the text to an int before you call the function.",
   "answer": C(r"""
def pack(qty: int) -> int:
    return qty * 3


print(pack(int("4")))""")},
 ],
 "py-logging": [
  {"title": "A. Log the progress of a load", "setup": "",
   "task": "Set up logging to normal output at INFO level with the format '%(levelname)s %(message)s'. Process these amounts: 120, -5, 40. Log INFO 'read 3 rows' first. Log a WARNING for each negative amount. At the end log INFO with the number of good rows.",
   "hint": "Import logging and sys. Use logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=...). Use %s in the messages.",
   "answer": C(r"""
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("load")

amounts = [120, -5, 40]
log.info("read %s rows", len(amounts))
good = 0
for amount in amounts:
    if amount < 0:
        log.warning("negative amount %s", amount)
    else:
        good = good + 1
log.info("good rows: %s", good)""")},
  {"title": "B. Why is the INFO line missing?", "setup": "",
   "broken": C(r"""
import logging
import sys

logging.basicConfig(stream=sys.stdout, format="%(levelname)s %(message)s")
log = logging.getLogger("etl")
log.info("start")
log.warning("one row skipped")"""),
   "task": "Say what this prints and why the first message is missing. Fix it so both lines appear.",
   "hint": "The default level is WARNING. Set the level in basicConfig.",
   "answer": C(r"""
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("etl")
log.info("start")
log.warning("one row skipped")""")},
  {"title": "C. One summary line with the right level", "setup": "",
   "task": "A job has results ok = 8 and failed = 2. Log one summary line: 'done: 8 ok, 2 failed'. Use INFO when failed is 0 and ERROR when failed is more than 0. Use the format '%(levelname)s %(message)s' and normal output.",
   "hint": "Choose the method with an if: log.error(...) or log.info(...). Use the same message pattern in both.",
   "answer": C(r"""
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("job")

ok = 8
failed = 2
if failed > 0:
    log.error("done: %s ok, %s failed", ok, failed)
else:
    log.info("done: %s ok, %s failed", ok, failed)""")},
 ],
 "py-pytest": [
  {"title": "A. Write the checks", "setup": "",
   "task": "band(amount) returns 'large' for 100 or more, 'medium' for 50 or more, otherwise 'small'. Write plain assert lines for 120, 60, 10 and for the edge values 100 and 50. If all pass, print 'all checks passed'.",
   "hint": "Test the edges. The rule says 100 or more, so band(100) is large.",
   "answer": C(r"""
def band(amount):
    if amount >= 100:
        return "large"
    if amount >= 50:
        return "medium"
    return "small"


assert band(120) == "large"
assert band(60) == "medium"
assert band(10) == "small"
assert band(100) == "large"
assert band(50) == "medium"
print("all checks passed")""")},
  {"title": "B. Read the failure", "setup": "",
   "broken": C(r"""
def clean(text):
    return text.strip().upper()


assert clean(" ab ") == "ab", "clean should give uppercase"
print("ok")"""),
   "task": "Say what this prints. The test is wrong, not the function. Fix the test.",
   "hint": "The function makes the text uppercase. The test expects lowercase.",
   "answer": C(r"""
def clean(text):
    return text.strip().upper()


assert clean(" ab ") == "AB", "clean should give uppercase"
print("ok")""")},
  {"title": "C. Compare floats safely", "setup": "",
   "broken": C(r"""
total = 0.1 + 0.2
assert total == 0.3
print("ok")"""),
   "task": "Say why this fails. Fix it with pytest.approx.",
   "hint": "import pytest. Then compare with pytest.approx(0.3).",
   "answer": C(r"""
import pytest

total = 0.1 + 0.2
assert total == pytest.approx(0.3)
print("ok")""")},
 ],
 "py-datetime": [
  {"title": "A. Parse day-first dates and sort them", "setup": "",
   "task": "These dates are day first: '03/11/2026', '25/12/2025', '01/02/2026'. Parse them, sort them from oldest to newest and print each one as ISO text.",
   "hint": "Use datetime.strptime(text, '%d/%m/%Y').date(). sorted() works on dates. Use .isoformat().",
   "answer": C(r"""
from datetime import datetime

texts = ["03/11/2026", "25/12/2025", "01/02/2026"]
dates = sorted(datetime.strptime(t, "%d/%m/%Y").date() for t in texts)
for d in dates:
    print(d.isoformat())""")},
  {"title": "B. Convert a meeting time", "setup": "",
   "task": "A meeting is at 15:00 on 5 October 2026 in New York. Print the time in London and in UTC, both as ISO text.",
   "hint": "Make the datetime with tzinfo=ZoneInfo('America/New_York'). Then use astimezone(ZoneInfo('Europe/London')) and astimezone(timezone.utc).",
   "answer": C(r"""
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

meeting = datetime(2026, 10, 5, 15, 0, tzinfo=ZoneInfo("America/New_York"))
print(meeting.astimezone(ZoneInfo("Europe/London")).isoformat())
print(meeting.astimezone(timezone.utc).isoformat())""")},
  {"title": "C. Fix the comparison", "setup": "",
   "broken": C(r"""
from datetime import datetime, timezone

loaded = datetime(2026, 10, 27, 9, 0)
deadline = datetime(2026, 10, 27, 17, 0, tzinfo=timezone.utc)
print(loaded < deadline)"""),
   "task": "Say what error this raises. The load time is UTC but the code forgot to say so. Fix it. It should print True.",
   "hint": "Give loaded the same zone: tzinfo=timezone.utc.",
   "answer": C(r"""
from datetime import datetime, timezone

loaded = datetime(2026, 10, 27, 9, 0, tzinfo=timezone.utc)
deadline = datetime(2026, 10, 27, 17, 0, tzinfo=timezone.utc)
print(loaded < deadline)""")},
 ],
}

# Claims that must be true (code, expected output) -- run at build time
CHECKS = [
 (C("""
def double(n: int) -> int:
    return n * 2

print(double("ab"))"""), "abab"),
 (TYPING_CODE, "12.0\n101010\n5"),
 (C("""
orders = [{"customer": "Acme", "amount": 5}]
def find_customer(orders, customer):
    for o in orders:
        if o["customer"] == customer:
            return o
    return None
result = find_customer(orders, "Zed")
print(result["amount"])"""), "TypeError: 'NoneType' object is not subscriptable"),
 (C("""
import logging
logging.info("hello")
logging.warning("careful")"""), "WARNING:root:careful"),
 (LOGGING_CODE, "WARNING:etl:bad amount 'abc' in row 2\nINFO:etl:loaded 2 of 3 rows"),
 (C("assert 2 + 2 == 5"), "AssertionError:"),
 (C("""
from datetime import datetime
datetime.strptime("27/10/2026", "%m/%d/%Y")"""), "ValueError: time data '27/10/2026' does not match format '%m/%d/%Y'"),
 (C("""
from datetime import datetime, timezone
a = datetime(2026, 10, 27, 12, 0)
b = datetime(2026, 10, 27, 13, 0, tzinfo=timezone.utc)
print(a < b)"""), "TypeError: can't compare offset-naive and offset-aware datetimes"),
 (C(r"""
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

london = ZoneInfo("Europe/London")
first = datetime.strptime("28/03/2026 12:00", "%d/%m/%Y %H:%M").replace(tzinfo=london)
second = datetime.strptime("29/03/2026 12:00", "%d/%m/%Y %H:%M").replace(tzinfo=london)
gap = second.astimezone(timezone.utc) - first.astimezone(timezone.utc)
print(gap.total_seconds() / 3600)
print(first.astimezone(ZoneInfo("America/New_York")).isoformat())"""), "23.0\n2026-03-28T08:00:00-04:00"),
 (C("""
from datetime import date
print((date(2026, 12, 25) - date(2026, 10, 27)).days)"""), "59"),
]

# Claims that only need to CONTAIN some text (code, [text, ...])
CHECKS_HAS = [
 (C(r"""
import logging
import sys

logging.basicConfig(stream=sys.stdout, format="%(levelname)s:%(name)s:%(message)s")
log = logging.getLogger("etl")
try:
    1 / 0
except ZeroDivisionError:
    log.exception("failed")"""), ["ERROR:etl:failed\nTraceback (most recent call last):", "ZeroDivisionError: division by zero"]),
]
