"""Senior-style worked examples, one per lesson.

build_course.py replaces each lesson's 'example' with the entry here and adds the notes.
Rules for every example:
  * It uses only ideas taught in that lesson or in earlier lessons (the concept check still runs).
    'uses_add' lists the extra ideas an example uses, so the check can see them.
  * Python output is produced by RUNNING the code at build time. SQL results are checked in DuckDB
    (see SQL_CHECKS). The T-SQL text itself has not been run on SQL Server.
  * 'notes' say why the code is written this way. Sources for the Python habits: PEP 8 (style),
    PEP 20 (the Zen of Python), PEP 257 (docstrings) and the Python documentation.
"""


def C(s):
    return s.strip("\n")


EXAMPLES = {}

# ------------------------------------------------------------------ Module 1
EXAMPLES["py-types"] = {
    "title": "A price calculation written the way a colleague would want to read it",
    "code": C(r"""
# Fixed numbers get a name in UPPER_CASE, so nobody has to guess what 12 or 0.2 means.
VAT_RATE = 0.2
ITEMS_PER_BOX = 12

unit_price = 19.99
quantity = 3
product_name = "pen"
is_paid = True
discount_code = None          # None means "no value yet"

net_total = unit_price * quantity
gross_total = net_total * (1 + VAT_RATE)
print(product_name, quantity, unit_price)
print(round(gross_total, 2))  # round only when you show a number, never in the middle of a calculation
print(type(unit_price), type(quantity), type(product_name), type(is_paid), type(discount_code))

stock = 1_250                 # underscores make big numbers readable
print(stock // ITEMS_PER_BOX, stock % ITEMS_PER_BOX, stock / ITEMS_PER_BOX)
print("3" + "4", int("3") + 4)    # text joins, numbers add: convert first
print(0.1 + 0.2, round(0.1 + 0.2, 2))
"""),
    "notes": [
        "Names say what the value means (unit_price, not p). Variables and functions use snake_case (PEP 8).",
        "A fixed number gets a UPPER_CASE name at the top. This removes magic numbers and gives one place to change them.",
        "Round only for display. Rounding in the middle of a calculation adds small errors.",
        "Never compare floats with ==. 0.1 + 0.2 is not exactly 0.3. Compare with a tolerance, or use whole numbers such as pence.",
        "One statement on each line, and a comment that says why, not what.",
    ],
}

EXAMPLES["py-strings"] = {
    "title": "Parse, clean and format an order code",
    "code": C(r"""
ORDER_CODE = "ORD-1042-uk"
SEPARATOR = "-"

parts = ORDER_CODE.split(SEPARATOR)               # ['ORD', '1042', 'uk']
print(parts[0], int(parts[1]), parts[2].upper())
print(ORDER_CODE[0:3], ORDER_CODE[-2:], ORDER_CODE[4:8], len(ORDER_CODE))

clean_name = "  pen  ".strip().upper()            # chain methods: read left to right
print(clean_name)
print(ORDER_CODE.replace("-", "_"), "uk" in ORDER_CODE, ORDER_CODE.startswith("ORD"))
print(SEPARATOR.join(parts))

name = "pen"
price = 2.5
quantity = 1200
share = 0.256
print(f"{name:<8}|{price:.2f}|{quantity:,}|{share:.1%}")   # one f-string, formats inside the braces
"""),
    "notes": [
        "Use f-strings for all formatting. Do not build text with + and str(). F-strings are shorter and cannot hide a type error.",
        "Put the separator in one named constant. A change then happens in one place.",
        "Methods return a NEW string. Chain them (strip, then upper) instead of making a temporary variable for each step.",
        "Use startswith and in for checks. They say what you mean. Slicing and comparing is harder to read.",
        "Lesson 1.3 shows tuple unpacking: prefix, number, country = ORDER_CODE.split(SEPARATOR). It replaces the three index lines.",
    ],
}

EXAMPLES["py-lists-tuples"] = {
    "title": "Lists that change, copies that do not, tuples as records",
    "code": C(r"""
orders = [120, 40, 80, 200]
orders.append(60)                                   # append changes the list in place
print(orders[0], orders[-1], orders[1:3], len(orders))
print(sum(orders), min(orders), max(orders))        # built-ins: do not write a loop for these

top_two = sorted(orders, reverse=True)[:2]          # sorted() returns a NEW list; orders is untouched
print(top_two, orders)
last = orders.pop()                                 # pop changes the list AND returns the item
print(last, 80 in orders)

customer, quantity, unit_price = ("Acme", 3, 12.5)  # unpack a tuple into named parts
print(customer, quantity * unit_price)
print(type((5)), type((5,)))                        # the comma makes the tuple

alias = orders                                      # a second name for the SAME list
snapshot = orders.copy()                            # a separate list with the same values
alias.append(999)
print(orders[-1], snapshot[-1], orders == snapshot)
"""),
    "notes": [
        "Use the built-ins sum, min, max, len and sorted. They are shorter, faster and easier to trust than a hand-written loop.",
        "Prefer sorted(x) to x.sort() when you also need the original order. A function that returns a new value is easier to reason about.",
        "Use a tuple for a fixed record and unpack it into names. quantity * unit_price reads better than record[1] * record[2].",
        "Know when two names point at one list. Use .copy() when you need a separate list.",
        "Use negative indexes (orders[-1]) for the end. Do not compute len(orders) - 1.",
    ],
}

EXAMPLES["py-control"] = {
    "title": "Totals, labels and a loop that stops, with no index juggling",
    "code": C(r"""
LARGE_LIMIT = 100
MEDIUM_LIMIT = 50

amounts = [120, 40, 80, 200, 60]
total = 0
large_count = 0
for amount in amounts:                    # loop over the values, not over range(len(amounts))
    total += amount
    if amount >= LARGE_LIMIT:
        large_count += 1
print(total, large_count, round(total / len(amounts), 1))

for position, amount in enumerate(amounts, start=1):   # enumerate gives the counter for free
    if amount >= LARGE_LIMIT:
        label = "large"
    elif amount >= MEDIUM_LIMIT:
        label = "medium"
    else:
        label = "small"
    print(position, amount, label)

customers = ["Acme", "Birch", "Cobalt"]
for customer, amount in zip(customers, amounts):       # zip walks two lists together
    print(f"{customer}: {amount}")

for amount in amounts:
    if amount > 150:
        print("first over 150:", amount)
        break                                          # stop as soon as the answer is known

if not []:                                             # an empty list is falsy
    print("nothing to process")
print(bool([]), bool([0]), bool(""), bool(None), bool(0))
"""),
    "notes": [
        "Loop over the items themselves. range(len(x)) with x[i] is the habit of someone coming from another language.",
        "enumerate(items, start=1) gives a counter and an item. zip pairs two lists. Both avoid index variables.",
        "Use += for an accumulator: total += amount. It is shorter and the intent is clear.",
        "Name the limits (LARGE_LIMIT). The if/elif chain then reads like the business rule.",
        "Use truthiness: if not items: instead of if len(items) == 0:. Break as soon as you have the answer.",
    ],
}

EXAMPLES["py-functions"] = {
    "title": "Small functions with one job, a docstring and clear arguments",
    "code": C(r"""
VAT_RATE = 0.2


def total_price(quantity, unit_price, vat_rate=VAT_RATE):
    \"\"\"Return the price including VAT.\"\"\"
    net = quantity * unit_price
    return net * (1 + vat_rate)


def min_max(values):
    \"\"\"Return the lowest and the highest value.\"\"\"
    return min(values), max(values)


print(total_price(3, 10))
print(total_price(quantity=3, unit_price=10, vat_rate=0))   # keyword arguments say what each number is

low, high = min_max([4, 9, 2])
print(low, high)


def show_total(price):
    total = price * 2          # forgot to return it


print(show_total(5))           # None

orders = [("Acme", 120), ("Birch", 40), ("Cobalt", 200)]
print(sorted(orders, key=lambda order: order[1], reverse=True))
print(max(orders, key=lambda order: order[1]))              # the biggest order, no sorting needed
print(total_price.__doc__)
""".replace('\\"', '"')),
    "notes": [
        "A function does one job and has a verb name: total_price, min_max. Two blank lines go between functions (PEP 8).",
        "Write a docstring: a text in triple quotes on the first line. It says what the function returns. Tools and help() show it (PEP 257).",
        "A function takes its inputs as parameters and gives its output with return. It does not read or change names outside itself.",
        "Use keyword arguments when a call has several numbers. total_price(quantity=3, unit_price=10) cannot be misread.",
        "Name the lambda parameter (order), not x. Use max(..., key=...) when you only need the biggest item. Sorting everything is wasted work.",
    ],
    "uses_add": [],
}

EXAMPLES["py-dict-count"] = {
    "title": "Count orders by status",
    "code": C(r"""
def count_by_status(orders):
    \"\"\"Return a dict that says how many orders have each status.\"\"\"
    counts = {}
    for order in orders:
        status = order["status"]
        counts[status] = counts.get(status, 0) + 1     # ask the TALLY, with 0 as the starting value
    return counts


orders = [
    {"id": 1, "status": "shipped"},
    {"id": 2, "status": "pending"},
    {"id": 3, "status": "shipped"},
]
counts = count_by_status(orders)
print(counts)
for status, count in sorted(counts.items()):            # a fixed order makes output easy to compare
    print(f"{status:<8}{count}")
""".replace('\\"', '"')),
    "notes": [
        "counts.get(status, 0) + 1 is the whole tally pattern in one line. It replaces the if/else that checks whether the key exists.",
        "Check the tally, never the row. 'status in order' asks about the row's keys and gives a wrong answer without an error.",
        "Sort before you print, so the output is the same on every run and easy to test.",
        "The function returns the dict and prints nothing. A caller can then test it, print it or save it.",
        "Python also has collections.Counter for this job. Learn the hand-written pattern first. Counter is a shortcut for the same idea.",
    ],
}

EXAMPLES["py-comprehensions"] = {
    "title": "Six comprehensions, each doing one clear job",
    "code": C(r"""
LARGE_LIMIT = 100
VAT_RATE = 0.2

orders = [
    {"id": 1, "customer": "Acme", "amount": 120},
    {"id": 2, "customer": "Birch", "amount": 40},
    {"id": 3, "customer": "Acme", "amount": 80},
    {"id": 4, "customer": "Cobalt", "amount": 200},
    {"id": 5, "customer": "Birch", "amount": 60},
    {"id": 6, "customer": "Acme", "amount": 50},
]
amounts = [order["amount"] for order in orders]
large_ids = [order["id"] for order in orders if order["amount"] >= LARGE_LIMIT]
amounts_with_vat = [round(amount * (1 + VAT_RATE), 2) for amount in amounts]
labels = ["large" if amount >= LARGE_LIMIT else "small" for amount in amounts]
amount_by_id = {order["id"]: order["amount"] for order in orders}      # a lookup table
customers = sorted({order["customer"] for order in orders})           # a set removes duplicates
print(amounts)
print(large_ids)
print(amounts_with_vat)
print(labels)
print(amount_by_id)
print(customers)
print(sum([amount for amount in amounts if amount >= LARGE_LIMIT]))
"""),
    "notes": [
        "Name the loop variable after what it is: order, amount. A single letter makes a long comprehension hard to read.",
        "One comprehension builds one thing. If you need two loops and an if inside, write a normal for loop.",
        "Use a dict comprehension for a lookup table and a set comprehension for unique values. The right container saves later code.",
        "Name the limits (LARGE_LIMIT, VAT_RATE) so the filter reads like the rule.",
        "A comprehension builds a whole list in memory. For one pass over a huge file, lesson 2.1 shows the generator version.",
    ],
}

EXAMPLES["py-mutable-default"] = {
    "title": "The bug, and the pattern that avoids it",
    "code": C(r"""
def add_item_buggy(item, cart=[]):
    \"\"\"BUG: the default list is made once, when def runs, and every call shares it.\"\"\"
    cart.append(item)
    return cart


print(add_item_buggy("Laptop"))
print(add_item_buggy("Mouse"))         # the first call's item is still there


def add_item(item, cart=None):
    \"\"\"Add the item to the cart. Start a new cart when none is given.\"\"\"
    if cart is None:                   # None is the signal for "make a fresh one"
        cart = []
    cart.append(item)
    return cart


print(add_item("Laptop"))
print(add_item("Mouse"))
""".replace('\\"', '"')),
    "notes": [
        "A default value is created ONCE, when def runs. A list or dict default is therefore shared by every call.",
        "The standard fix is a None default and a new list inside the function. Write 'is None', not '== None'.",
        "Use only numbers, text, True, False and None as defaults. Linters flag a list or dict default for this reason.",
        "A docstring that names the trap (BUG, or Start a new cart) helps the next reader.",
    ],
    "uses_add": ["docstring"],
}

EXAMPLES["py-files"] = {
    "title": "Read a CSV, total it, write CSV and JSON with real files",
    "code": C(r"""
import csv
import io
import json

ORDERS_FILE = "orders.csv"

with open(ORDERS_FILE, newline="", encoding="utf-8") as file:     # with closes the file for you
    rows = list(csv.DictReader(file))
print(rows[0])
print(type(rows[0]["amount"]))                                    # every value from a CSV is text

totals = {}
for row in rows:
    customer = row["customer"]
    totals[customer] = totals.get(customer, 0) + float(row["amount"])   # convert where you use it
print(totals)

with open("totals.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["customer", "total"])
    writer.writeheader()
    for customer, total in totals.items():
        writer.writerow({"customer": customer, "total": total})

with open("totals.json", "w", encoding="utf-8") as file:
    json.dump({"totals": totals}, file, indent=2)

with open("totals.csv", newline="", encoding="utf-8") as file:
    print(file.read().splitlines())
with open("totals.json", encoding="utf-8") as file:
    print(json.load(file)["totals"]["Acme"])

# io.StringIO is a file that lives in memory. It is how the examples in this course feed text to csv.
sample = list(csv.DictReader(io.StringIO("id,customer,amount\n1,Acme,120\n")))
print(sample[0]["customer"])
"""),
    "script": {"name": "example.py", "files": {"orders.csv": "id,customer,amount\n1,Acme,120\n2,Birch,40\n3,Acme,80\n"},
               "cmd": ["example.py"], "show": "python example.py"},
    "notes": [
        "Always open files with 'with'. It closes the file even when an error happens.",
        "Always pass encoding='utf-8', and newline='' for CSV. The defaults differ between Windows and other systems, and this is a classic source of broken files.",
        "csv.DictReader gives each row as a dict with the header names. row['amount'] is clearer than row[2].",
        "Every CSV value is text. Convert it once, at the place you use it, and fail loudly if it is bad.",
        "Keep file names in a constant. Real projects use pathlib for paths. You will meet it in a later module.",
    ],
}

EXAMPLES["py-except-order"] = {
    "title": "Catch the error you expect, in the right order",
    "code": C(r"""
class InsufficientFundsError(Exception):
    \"\"\"Raised when a withdrawal is larger than the balance.\"\"\"      # a docstring is enough: no pass needed


def parse_amount(text):
    \"\"\"Return the amount as a float, or None when the text is not a number.\"\"\"
    try:
        return float(text)
    except ValueError:                 # catch only the error you expect
        return None


print([parse_amount(text) for text in ["12.5", "abc", "7"]])

# Wrong order: Exception catches everything first, so the specific block never runs.
try:
    raise InsufficientFundsError("low")
except Exception:
    print("general")
except InsufficientFundsError:
    print("specific")

# Right order: the most specific error first, the general one last.
try:
    raise InsufficientFundsError("low")
except InsufficientFundsError:
    print("specific")
except Exception:
    print("general")
""".replace('\\"', '"')),
    "notes": [
        "Catch the narrowest error you can: except ValueError. A bare except or except Exception hides real bugs.",
        "Keep the try block small. Only the line that can fail goes inside it.",
        "Python checks except blocks from the top. The first match runs. Put the specific error first and the general one last.",
        "Custom errors are classes that inherit from Exception. A docstring explains when to raise it.",
        "Return a clear value (None here) or raise a clear error. Never let the program carry on with a silent wrong answer.",
    ],
    "uses_add": ["docstring"],
}

EXAMPLES["py-scripts"] = {
    "title": "A small command line tool with a clear structure",
    "code": C(r"""
\"\"\"List the orders at or above a threshold.\"\"\"
import argparse
import csv

DEFAULT_THRESHOLD = 100.0


def read_orders(path):
    \"\"\"Read a CSV file and return one dict per row, with the amount as a float.\"\"\"
    orders = []
    with open(path, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            row["amount"] = float(row["amount"])       # convert once, here
            orders.append(row)
    return orders


def filter_large(orders, threshold):
    \"\"\"Return the orders with an amount at or above the threshold.\"\"\"
    return [order for order in orders if order["amount"] >= threshold]


def parse_args():
    parser = argparse.ArgumentParser(description="List the large orders in a CSV file.")
    parser.add_argument("filename", help="CSV file with id, customer and amount columns")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help="smallest amount to show (default: %(default)s)")
    return parser.parse_args()


def main():
    args = parse_args()
    for order in filter_large(read_orders(args.filename), args.threshold):
        print(f"{order['id']:<4}{order['customer']:<8}{order['amount']:>8.2f}")


if __name__ == "__main__":
    main()
""".replace('\\"', '"')),
    "script": {"name": "tool.py", "files": {"orders.csv": "id,customer,amount\n1,Acme,120\n2,Birch,40\n3,Acme,80\n4,Cobalt,200\n"},
               "cmd": ["tool.py", "orders.csv", "--threshold", "100"], "show": "python tool.py orders.csv --threshold 100"},
    "notes": [
        "Split the script into functions that each do one job: read, filter, parse the arguments, run. Each can be tested alone.",
        "if __name__ == '__main__': main() lets another file import the functions without running the tool.",
        "argparse gives you --help and clear errors for free. Write a help text for each argument.",
        "Convert types once, at the edge (read_orders). The rest of the code works with real numbers.",
        "A module docstring on the first line says what the file is for. Imports come next, standard library first (PEP 8).",
    ],
    "uses_add": ["docstring"],
}

# ------------------------------------------------------------------ Module 2
EXAMPLES["py-generators"] = {
    "title": "A generator that yields one value at a time",
    "code": C(r"""
prices = [10, 25, 8, 40]

discounted = (price * 0.9 for price in prices)    # nothing is calculated yet
print(sum(discounted))                           # sum pulls the values through, one by one
print(list(discounted))                          # []: a generator is used up after one pass


def large_prices(values, limit):
    \"\"\"Yield the values above the limit, one at a time.\"\"\"
    for value in values:
        if value > limit:
            yield value


print(list(large_prices(prices, 20)))
print(sum(price for price in prices if price > 20))   # no extra brackets when it is the only argument
""".replace('\\"', '"')),
    "notes": [
        "A generator makes values on demand. It never holds the whole list in memory. This is how you process a file that is bigger than your RAM.",
        "A generator is used up after one pass. If you need two passes, make a list or make the generator again.",
        "Use a generator expression inside sum, min, max and any. Write sum(x for x in items), with no list brackets, so no list is built.",
        "A function with yield is a generator function. Give it a docstring that says what it yields.",
    ],
    "uses_add": ["docstring"],
}

EXAMPLES["py-classes"] = {
    "title": "Order and RushOrder: one plan, one subclass",
    "code": C(r"""
class Order:
    \"\"\"A customer order made of items.\"\"\"

    def __init__(self, customer):
        self.customer = customer
        self.items = []                      # every order gets its own list

    def add_item(self, name, quantity, unit_price):
        self.items.append((name, quantity, unit_price))

    def total(self):
        \"\"\"Return the sum of quantity * unit price for all items.\"\"\"
        return sum(quantity * unit_price for _, quantity, unit_price in self.items)


class RushOrder(Order):
    \"\"\"An order with a fixed rush fee on top.\"\"\"

    def __init__(self, customer, fee):
        super().__init__(customer)           # let the parent set up what it owns
        self.fee = fee

    def total(self):
        return super().total() + self.fee    # reuse the parent's rule, then add to it


standard = Order("Acme")
standard.add_item("pen", 10, 2.5)
standard.add_item("ink", 2, 10)
rush = RushOrder("Birch", 5)
rush.add_item("desk", 1, 120)
print(standard.customer, standard.total())
print(rush.customer, rush.total())
print(isinstance(rush, Order), isinstance(standard, RushOrder))
another = Order("Acme")
print(another.items, standard.items is another.items)
""".replace('\\"', '"')),
    "notes": [
        "Class names use PascalCase. Methods and attributes use snake_case (PEP 8). A class has a docstring.",
        "Create mutable attributes (self.items = []) inside __init__, so each object has its own. A shared list is the same trap as a mutable default.",
        "A subclass calls super().__init__ and super().total() to reuse the parent. It does not copy the parent's code.",
        "Keep methods short, with one job. A method that returns a value (total) is easier to test than one that prints.",
        "Prefer small classes with clear names. If a class only holds data, lesson 2.4 shows a shorter way: a dataclass.",
    ],
    "uses_add": ["docstring"],
}

EXAMPLES["py-class-property"] = {
    "title": "A property for a derived value, and a useful repr",
    "code": C(r"""
class Order:
    \"\"\"One order line.\"\"\"

    def __init__(self, customer, quantity, unit_price):
        self.customer = customer
        self.quantity = quantity
        self.unit_price = unit_price

    @property
    def total(self):
        \"\"\"The order total. It is worked out each time you read it.\"\"\"
        return self.quantity * self.unit_price

    def __repr__(self):
        return f"Order({self.customer!r}, total={self.total})"


order = Order("Acme", 3, 10)
print(order.total)
print(order)
order.quantity = 4              # change an input ...
print(order.total)              # ... and the property is always up to date
""".replace('\\"', '"')),
    "notes": [
        "Store the inputs and work out the rest. A property (total) cannot go out of date. A copied attribute can.",
        "Read a property without brackets: order.total. A property that is expensive or can fail should be a method.",
        "__repr__ is for developers. It should look like the code that makes the object. !r puts quote marks around text.",
        "Always return the string from __repr__. Building it without return gives None and a TypeError.",
    ],
    "uses_add": ["docstring"],
}

EXAMPLES["py-dataclasses"] = {
    "title": "CSV rows into dataclass objects, with the types fixed in one place",
    "code": C(r"""
from dataclasses import asdict, dataclass, field
import csv
import io
import json


@dataclass
class Order:
    \"\"\"One order line from the orders file.\"\"\"

    id: int
    customer: str
    amount: float
    tags: list = field(default_factory=list)   # each order gets its own list


def order_from_row(row):
    \"\"\"Convert one CSV row (all text) into an Order with real types.\"\"\"
    return Order(id=int(row["id"]), customer=row["customer"], amount=float(row["amount"]))


raw = "id,customer,amount\n1,Acme,120\n2,Birch,40\n"
orders = [order_from_row(row) for row in csv.DictReader(io.StringIO(raw))]
print(orders[0])
print(orders[0] == Order(1, "Acme", 120.0))        # equality compares every field
orders[1].tags.append("late")
print(orders[0].tags, orders[1].tags)
print(json.dumps(asdict(orders[1])))
""".replace('\\"', '"')),
    "notes": [
        "A dataclass names and types every field, and writes __init__, __repr__ and __eq__ for you. Less code, fewer bugs.",
        "Put the conversion from text to real types in ONE function (order_from_row). The rest of the program then works with typed data.",
        "Use keyword arguments when you build an object with several fields. Order(id=..., amount=...) cannot swap two values by mistake.",
        "Use field(default_factory=list) for a list or dict field. A plain [] default is refused, for the same reason as in lesson 1.8.",
        "Use @dataclass(frozen=True) for records that must not change. asdict turns a record into a dict for JSON.",
    ],
    "uses_add": ["docstring"],
}

EXAMPLES["py-decorators"] = {
    "title": "A logging decorator and a retry decorator",
    "code": C(r"""
import functools


def log_calls(func):
    \"\"\"Print each call to func with its arguments and its result.\"\"\"
    @functools.wraps(func)                           # keeps the name and docstring of func
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__} with {args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result                                # never forget to return the result
    return wrapper


@log_calls
def total_price(quantity, unit_price, vat_rate=0.2):
    \"\"\"Return the price including VAT.\"\"\"
    return round(quantity * unit_price * (1 + vat_rate), 2)


total_price(3, 10, vat_rate=0)
print(total_price.__name__)


def retry(times):
    \"\"\"Call the function up to `times` times while it raises ConnectionError.\"\"\"
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError:              # retry only the error that can pass by itself
                    print(f"attempt {attempt} failed")
            raise ConnectionError("gave up")
        return wrapper
    return decorator


attempts_made = []


@retry(3)
def fetch():
    attempts_made.append(1)
    if len(attempts_made) < 3:
        raise ConnectionError("down")
    return "data"


print(fetch())
""".replace('\\"', '"')),
    "notes": [
        "Always use @functools.wraps(func) on the wrapper. Without it the name, docstring and help of the original function are lost.",
        "Accept *args and **kwargs in the wrapper and pass them on unchanged. The decorator then works on any function.",
        "Return the result of the call. Forgetting it turns every decorated function into one that returns None.",
        "Retry only errors that can pass by themselves (ConnectionError). Never retry on a bare except: it hides real bugs.",
        "A decorator is the right tool for a rule that applies to many functions: logging, timing, retry, checks.",
    ],
    "uses_add": ["docstring"],
}

EXAMPLES["py-typing"] = {
    "title": "Hints that Python ignores and mypy checks",
    "code": "TYPING_CODE",       # replaced in build_course with lessons_m2b.TYPING_CODE
    "notes": [
        "Hint every function parameter and return value. Skip hints on simple local variables: the checker can infer them.",
        "Write X | None when a function can return nothing. mypy then forces the caller to check, which prevents the classic None crash.",
        "Use the specific type: list[Order], not list. A reader and the checker then know what is inside.",
        "Run mypy in your checks, next to pytest. A hint that nothing checks is only a comment.",
        "Avoid Any. It switches the checker off for that value. Fix the hint instead.",
    ],
    "uses_add": ["docstring"],
}

EXAMPLES["py-logging"] = {
    "title": "A module logger, configured once in main",
    "code": C(r"""
import logging
import sys

log = logging.getLogger(__name__)         # one logger per module, named after the module


def count_valid_rows(rows):
    \"\"\"Return how many rows have a numeric amount. Log each bad row.\"\"\"
    valid = 0
    for row in rows:
        try:
            float(row["amount"])
        except ValueError:
            log.warning("bad amount %r in row %s", row["amount"], row["id"])
        else:
            valid += 1                       # else runs only when no error was raised
    log.info("loaded %s of %s rows", valid, len(rows))
    return valid


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(levelname)s %(message)s")
    log.debug("this line is hidden")
    rows = [{"id": "1", "amount": "120"}, {"id": "2", "amount": "abc"}, {"id": "3", "amount": "80"}]
    count_valid_rows(rows)


if __name__ == "__main__":
    main()
""".replace('\\"', '"')),
    "notes": [
        "Each module gets log = logging.getLogger(__name__). Only the main program calls basicConfig. A library never configures logging.",
        "Pass values as arguments: log.warning('bad amount %r', value). Do not use an f-string. The text is built only when the message is shown.",
        "Log the counts: rows read, rows rejected, rows loaded. They are the first thing you look at when a nightly job is wrong.",
        "Use the right level: INFO for progress, WARNING for a problem you handled, ERROR for a failure. Use log.exception inside except to keep the traceback.",
        "try / except / else keeps the success path in else, so only the risky line sits inside try.",
    ],
    "uses_add": ["docstring", "main-guard"],
}

_ETL = C(r"""
\"\"\"Cleaning and banding rules for order amounts.\"\"\"

LARGE_LIMIT = 100
MEDIUM_LIMIT = 50


def clean_amount(text):
    \"\"\"Turn text such as ' 1,234.50 ' into the float 1234.5.\"\"\"
    return float(text.strip().replace(",", ""))


def band(amount):
    \"\"\"Return 'large', 'medium' or 'small' for an amount.\"\"\"
    if amount >= LARGE_LIMIT:
        return "large"
    if amount >= MEDIUM_LIMIT:
        return "medium"
    return "small"


def load_amounts(path):
    \"\"\"Read one amount per line and skip blank lines.\"\"\"
    with open(path, encoding="utf-8") as file:
        return [clean_amount(line) for line in file if line.strip()]
""".replace('\\"', '"'))

_TEST = C(r"""
import pytest
from etl import band, clean_amount, load_amounts


def test_clean_amount_removes_spaces_and_commas():
    assert clean_amount(" 1,234.50 ") == 1234.5


@pytest.mark.parametrize("amount, expected", [(120, "large"), (60, "medium"), (10, "small")])
def test_band(amount, expected):
    assert band(amount) == expected


def test_clean_amount_rejects_text():
    with pytest.raises(ValueError):
        clean_amount("abc")


def test_load_amounts_skips_blank_lines(tmp_path):
    path = tmp_path / "amounts.txt"
    with open(path, "w", encoding="utf-8") as file:
        file.write("10\n20.5\n\n")
    assert load_amounts(path) == [10.0, 20.5]


def helper_not_a_test():
    assert False
""")

EXAMPLES["py-pytest"] = {
    "title": "A module and its tests",
    "code": "# etl.py\n" + _ETL + "\n\n# test_etl.py\n" + _TEST,
    "script": {"display_only": True, "files": {"etl.py": _ETL + "\n", "test_etl.py": _TEST + "\n"},
               "cmd": ["-m", "pytest", "-q", "-p", "no:cacheprovider"], "show": "pytest -q", "tidy": True},
    "notes": [
        "A test name says what is checked: test_clean_amount_rejects_text. A failing test then explains itself.",
        "One test checks one idea. parametrize runs the same check on many inputs without copy and paste.",
        "Test the edges: the values at exactly 100 and 50, blank lines, bad text. Bugs live at the edges.",
        "tmp_path gives each test its own clean folder, so tests never depend on files on your machine.",
        "Keep the rules (limits, cleaning) in a small module with no printing. Such code is easy to test.",
    ],
    "uses_add": ["docstring"],
}

EXAMPLES["py-datetime"] = {
    "title": "Parse day-first text as London time and keep UTC for storage",
    "code": C(r"""
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

LONDON = ZoneInfo("Europe/London")
INPUT_FORMAT = "%d/%m/%Y %H:%M"            # day first: say the format once, in one place


def parse_london(text):
    \"\"\"Parse day-first text as a London time and return an aware datetime.\"\"\"
    return datetime.strptime(text, INPUT_FORMAT).replace(tzinfo=LONDON)


def to_utc(moment):
    \"\"\"Convert an aware datetime to UTC.\"\"\"
    return moment.astimezone(timezone.utc)


opened = parse_london("27/10/2026 14:30")
print(opened, opened.strftime("%Y-%m-%d"))
print((date(2026, 12, 25) - date(2026, 10, 27)).days)

start = parse_london("28/03/2026 12:00")
next_day = start + timedelta(days=1)       # one calendar day on the London clock
print(start)
print(next_day)
print(next_day - start)                    # same zone: the clock difference
print(to_utc(next_day) - to_utc(start))    # UTC: the real time that passed
print(to_utc(next_day))
""".replace('\\"', '"')),
    "notes": [
        "Store and exchange times in UTC. Convert to a local zone only when you show a time to a person.",
        "Never use a naive datetime in a data pipeline. Attach the zone at the edge, as parse_london does.",
        "Put the format string in one named constant. Day-first and month-first look the same for the 1st to the 12th.",
        "Use zoneinfo for zones. Do not add a fixed number of hours by hand: the offset changes with daylight saving.",
        "To measure real elapsed time, convert both values to UTC first.",
    ],
    "uses_add": ["docstring"],
}

# ------------------------------------------------------------------ SQL (T-SQL)
# Style used below: UPPERCASE keywords, one clause per line, schema-qualified tables (dbo.),
# a short alias for every table and every column reference, comments that say why.
# Results are checked in DuckDB (see SQL_CHECKS). The T-SQL has not been run on SQL Server.
EXAMPLES["sql-where-having"] = {
    "title": "Wards with a high average wait",
    "code": C(r"""
-- Wards whose average wait is above 30 minutes, counting only visits longer than 15 minutes.
SELECT
    v.Ward,
    AVG(v.WaitMins) AS AvgWait
FROM dbo.Visits AS v
WHERE v.WaitMins > 15            -- row filter: runs before grouping
GROUP BY v.Ward
HAVING AVG(v.WaitMins) > 30      -- group filter: needs the aggregate, so it cannot go in WHERE
ORDER BY v.Ward;
"""),
    "output": "Ward | AvgWait\nA    | 50\nC    | 80",
    "notes": [
        "Uppercase keywords, one clause on each line and indented columns make the logical order of the query easy to see.",
        "Qualify the table with its schema (dbo.Visits) and every column with an alias (v.Ward). This avoids ambiguity when the query grows a join.",
        "Comment the WHY of each filter. WHERE and HAVING are different stages, and the comment says which one runs first.",
        "End the statement with a semicolon and always give ORDER BY when order matters. Without it SQL Server does not promise any order.",
        "In SQL Server, AVG of an integer column returns an integer. Use AVG(CAST(v.WaitMins AS DECIMAL(9, 2))) when you need decimals.",
    ],
}

EXAMPLES["sql-window-frames"] = {
    "title": "Moving average and LAST_VALUE",
    "code": C(r"""
SELECT
    w.VisitID,
    AVG(w.WaitMins) OVER (
        PARTITION BY w.Ward
        ORDER BY w.VisitID
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW         -- this row and the 2 before it
    ) AS Moving3,
    LAST_VALUE(w.WaitMins) OVER (
        PARTITION BY w.Ward
        ORDER BY w.VisitID                               -- no frame: the default stops at the current row
    ) AS LastDefault,
    LAST_VALUE(w.WaitMins) OVER (
        PARTITION BY w.Ward
        ORDER BY w.VisitID
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING   -- the whole partition
    ) AS LastFull
FROM dbo.W AS w
ORDER BY w.VisitID;
"""),
    "output": "VisitID | Moving3 | LastDefault | LastFull\n1       | 10      | 10          | 70\n2       | 30      | 50          | 70\n3       | 30      | 30          | 70\n4       | 50      | 70          | 70",
    "notes": [
        "Write each OVER clause on several lines: PARTITION BY, ORDER BY and the frame each get a line. A one-line OVER is hard to review.",
        "Always write the frame explicitly (ROWS BETWEEN ...). The default frame is a known trap. LAST_VALUE with the default frame returns the current row.",
        "Use ROWS, not RANGE, unless you want ties treated together. ROWS is faster and its meaning is exact.",
        "Give every output column a clear alias (Moving3, LastDefault) so the result can be read without the query.",
        "Comment the frame at the point where it can mislead. The comment is for the next person, and for you in six months.",
    ],
}

EXAMPLES["sql-percentile"] = {
    "title": "Median and quartiles of 10, 20, 30, 40",
    "code": C(r"""
-- PERCENTILE_CONT blends values. PERCENTILE_DISC returns a value that really exists.
SELECT DISTINCT                                   -- OVER () repeats one answer on every row
    PERCENTILE_CONT(0.5)  WITHIN GROUP (ORDER BY p.x) OVER () AS ContMedian,
    PERCENTILE_DISC(0.5)  WITHIN GROUP (ORDER BY p.x) OVER () AS DiscMedian,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY p.x) OVER () AS ContQ3,
    PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY p.x) OVER () AS DiscQ3
FROM dbo.P AS p;
"""),
    "output": "ContMedian | DiscMedian | ContQ3 | DiscQ3\n25         | 20         | 32.5   | 30",
    "notes": [
        "Line up the repeated pattern. Columns that do the same thing in the same layout are quick to check by eye.",
        "Choose CONT or DISC on purpose, and say why in a comment. CONT can return a value that is not in the data. DISC never does.",
        "PERCENTILE_CONT needs WITHIN GROUP and OVER. Use PARTITION BY inside OVER for one answer per group.",
        "DISTINCT here only removes the repeated rows that OVER () creates. The result is one row.",
    ],
}

EXAMPLES["sql-rollup-grouping"] = {
    "title": "Subtotals with labels",
    "code": C(r"""
SELECT
    r.Yr,
    CASE
        WHEN GROUPING(r.Ward) = 1 THEN 'All wards'          -- a subtotal row, not real data
        ELSE ISNULL(r.Ward, 'Unknown')                      -- a real NULL in the data
    END AS WardLabel,
    SUM(r.Mins) AS Total,
    GROUPING(r.Ward) AS IsWardSubtotal
FROM dbo.R AS r
GROUP BY ROLLUP (r.Yr, r.Ward)
ORDER BY GROUPING(r.Yr), r.Yr, GROUPING(r.Ward), r.Ward;    -- subtotals after their detail rows
"""),
    "output": "Yr   | WardLabel | Total | IsWardSubtotal\n2024 | A         | 100   | 0\n2024 | B         | 200   | 0\n2024 | All wards | 300   | 1\n2025 | Unknown   | 50    | 0\n2025 | A         | 300   | 0\n2025 | All wards | 350   | 1\nNULL | All wards | 650   | 1",
    "notes": [
        "Use GROUPING() to tell a subtotal NULL from a real NULL. Testing 'Ward IS NULL' would mix them up.",
        "Write the labels in a CASE with one WHEN on each line. The branches are then easy to read and to change.",
        "Put GROUPING() in ORDER BY. Subtotals then follow their detail rows and the grand total is last. Without it, NULL sorts first in SQL Server.",
        "Every column in the SELECT is either in GROUP BY, or wrapped in an aggregate (SUM). A bare column is an error.",
        "The Yr column shows NULL on the grand total row. Add a label for it in a report.",
    ],
}

EXAMPLES["sql-correlated-vs-window"] = {
    "title": "Same result, two methods",
    "code": C(r"""
-- Method 1: correlated subquery. It runs once for every outer row.
SELECT
    v.VisitID,
    (
        SELECT AVG(v2.WaitMins)
        FROM dbo.V AS v2
        WHERE v2.Ward = v.Ward
          AND v2.VisitID < v.VisitID               -- only earlier visits in the same ward
    ) AS AvgPrior
FROM dbo.V AS v
ORDER BY v.VisitID;

-- Method 2: window function. One pass over the data.
SELECT
    v.VisitID,
    AVG(v.WaitMins) OVER (
        PARTITION BY v.Ward
        ORDER BY v.VisitID
        ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING   -- everything before this row
    ) AS AvgPrior
FROM dbo.V AS v
ORDER BY v.VisitID;
"""),
    "output": "VisitID | AvgPrior\n1       | NULL\n2       | NULL\n3       | 10\n4       | 20\n5       | 40",
    "notes": [
        "Prefer the window function. It reads the table once. The correlated subquery runs again for every outer row, which is slow on large tables.",
        "Use different aliases for the inner and outer table (v2 and v). Reusing one alias is a common source of wrong results.",
        "Write the same rule in the same words in both methods. The comments name what the frame and the WHERE clause mean.",
        "Check the first rows of a 'previous rows' calculation. They have no earlier rows, so the result is NULL, not 0.",
    ],
}


# SQL results are checked in DuckDB: (query for DuckDB, expected rows). T-SQL-only parts (dbo., ISNULL) are adapted.
def sql_checks():
    import duckdb
    con = duckdb.connect()
    con.execute("SET default_null_order='nulls_first'")      # SQL Server sorts NULL first in ascending order
    con.execute("CREATE TABLE Visits(VisitID INT, Ward VARCHAR, WaitMins INT)")
    con.execute("INSERT INTO Visits VALUES (1,'A',10),(2,'A',50),(3,'B',20),(4,'B',20),(5,'C',90),(6,'C',70)")
    con.execute("CREATE TABLE W(VisitID INT, Ward VARCHAR, WaitMins INT)")
    con.execute("INSERT INTO W VALUES (1,'A',10),(2,'A',50),(3,'A',30),(4,'A',70)")
    con.execute("CREATE TABLE R(Yr INT, Ward VARCHAR, Mins INT)")
    con.execute("INSERT INTO R VALUES (2024,'A',100),(2024,'B',200),(2025,'A',300),(2025,NULL,50)")
    con.execute("CREATE TABLE V(VisitID INT, Ward VARCHAR, WaitMins INT)")
    con.execute("INSERT INTO V VALUES (1,'A',10),(2,'B',40),(3,'A',30),(4,'A',50),(5,'B',20)")

    def duck(sql):
        return sql.replace("dbo.", "").replace("ISNULL(", "COALESCE(")

    def rows(sql):
        return con.execute(duck(sql)).fetchall()

    r = rows(EXAMPLES["sql-where-having"]["code"])
    assert r == [("A", 50.0), ("C", 80.0)], r
    r = rows(EXAMPLES["sql-window-frames"]["code"])
    assert r == [(1, 10.0, 10, 70), (2, 30.0, 50, 70), (3, 30.0, 30, 70), (4, 50.0, 70, 70)], r
    r = rows(EXAMPLES["sql-rollup-grouping"]["code"])
    assert r == [(2024, "A", 100, 0), (2024, "B", 200, 0), (2024, "All wards", 300, 1),
                 (2025, "Unknown", 50, 0), (2025, "A", 300, 0), (2025, "All wards", 350, 1),
                 (None, "All wards", 650, 1)], r
    code = EXAMPLES["sql-correlated-vs-window"]["code"]
    first, second = code.split("-- Method 2")
    expected = [(1, None), (2, None), (3, 10.0), (4, 20.0), (5, 40.0)]
    assert rows(first) == expected, rows(first)
    assert rows("SELECT" + second.split("SELECT", 1)[1]) == expected, rows("SELECT" + second.split("SELECT", 1)[1])
    # Percentile: DuckDB has no PERCENTILE_CONT ... OVER, so check the numbers with its own function.
    con.execute("CREATE TABLE P(x INT)")
    con.execute("INSERT INTO P VALUES (10),(20),(30),(40)")
    r = con.execute("SELECT quantile_cont(x,0.5), quantile_disc(x,0.5), quantile_cont(x,0.75), quantile_disc(x,0.75) FROM P").fetchone()
    assert r == (25.0, 20, 32.5, 30), r
    return True
