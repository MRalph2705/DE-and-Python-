"""Python mixed practice. Every setup, broken snippet and answer is RUN; output is captured."""
import contextlib, io

ORDERS = '''orders = [
    {"id": 1, "customer": "Acme", "amount": 120.0},
    {"id": 2, "customer": "Birch", "amount": 40.0},
    {"id": 3, "customer": "Acme", "amount": 80.0},
    {"id": 4, "customer": "Cobalt", "amount": 200.0},
    {"id": 5, "customer": "Birch", "amount": 60.0},
    {"id": 6, "customer": "Acme", "amount": 50.0},
]'''

COUNTS = '''counts = {}
for order in orders:
    customer = order["customer"]
    if customer in counts:
        counts[customer] = counts[customer] + 1
    else:
        counts[customer] = 1
'''

TASKS = {
 "py-dict-count": [
  {"title": "A. Count, then sort", "setup": ORDERS,
   "task": "Count the orders for each customer. Print one line for each customer: the name and the count. Show the highest count first. If two counts are equal, sort by name.",
   "hint": "Build the tally first. Then sort counts.items() with a key. A key can return a tuple. Use a minus sign to sort a number from high to low.",
   "answer": COUNTS + '''for name, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
    print(name, n)'''},
  {"title": "B. Add up, not count", "setup": ORDERS,
   "task": "Find the total amount for each customer. Print the dictionary.",
   "hint": "The pattern is the same. Add the amount instead of 1. The method dict.get(key, 0) gives 0 when the key is missing.",
   "answer": '''totals = {}
for order in orders:
    customer = order["customer"]
    totals[customer] = totals.get(customer, 0) + order["amount"]
print(totals)'''},
  {"title": "C. Filter a tally", "setup": ORDERS,
   "task": "Build the count for each customer. Then make a new dictionary with only the customers that have 2 or more orders. Print it.",
   "hint": "A dictionary comprehension: {key: value for key, value in d.items() if test}.",
   "answer": COUNTS + '''repeat = {c: n for c, n in counts.items() if n >= 2}
print(repeat)'''},
  {"title": "D. Read a file and skip bad rows", "setup": 'import csv\nimport io\n\nraw = "id,customer,amount\\n1,Acme,120\\n2,Birch,abc\\n3,Acme,80\\n4,Cobalt,\\n5,Birch,60\\n"',
   "task": "The text raw is a small CSV file. Read it with csv.DictReader. Add up the amount for each customer. If an amount is not a number, do not stop. Save the id of that row in a list. Print the totals, then the list of bad ids.",
   "hint": "Use io.StringIO(raw) in place of a file. Put float() inside try. The error to catch is ValueError. The id is a string.",
   "answer": '''totals = {}
bad = []
for row in csv.DictReader(io.StringIO(raw)):
    try:
        amount = float(row["amount"])
    except ValueError:
        bad.append(row["id"])
        continue
    customer = row["customer"]
    totals[customer] = totals.get(customer, 0) + amount
print(totals)
print(bad)'''},
 ],
 "py-mutable-default": [
  {"title": "A. Fix a shared list", "setup": "",
   "broken": '''def add_order(order, orders=[]):
    orders.append(order)
    return orders

print(add_order("A"))
print(add_order("B"))''',
   "task": "The code below should print ['A'] and then ['B']. Run it in your head. Say what it prints. Then rewrite add_order so it prints ['A'] and then ['B'].",
   "hint": "Use None as the default. Make the new list inside the function.",
   "answer": '''def add_order(order, orders=None):
    if orders is None:
        orders = []
    orders.append(order)
    return orders

print(add_order("A"))
print(add_order("B"))'''},
  {"title": "B. Fix a shared list inside a class", "setup": "",
   "broken": '''class Customer:
    def __init__(self, name, tags=[]):
        self.name = name
        self.tags = tags

a = Customer("Acme")
b = Customer("Birch")
a.tags.append("vip")
print(a.tags, b.tags)''',
   "task": "Birch should have no tags. Say what the code below prints. Then fix the class so b.tags is empty.",
   "hint": "The same rule applies to __init__. The default is made one time. Use None.",
   "answer": '''class Customer:
    def __init__(self, name, tags=None):
        self.name = name
        self.tags = [] if tags is None else tags

a = Customer("Acme")
b = Customer("Birch")
a.tags.append("vip")
print(a.tags, b.tags)'''},
 ],
 "py-generators": [
  {"title": "A. A generator function in use", "setup": ORDERS,
   "task": "Write a generator function large_orders(orders, threshold). It yields each order with an amount at or above the threshold. Then print the sum of the amounts of orders of 100 or more.",
   "hint": "Use for, if and yield. Pass a generator expression to sum(): sum(o['amount'] for o in large_orders(orders, 100)).",
   "answer": '''def large_orders(orders, threshold):
    for order in orders:
        if order["amount"] >= threshold:
            yield order

print(sum(o["amount"] for o in large_orders(orders, 100)))'''},
  {"title": "B. Used up twice", "setup": ORDERS,
   "broken": '''amounts = (o["amount"] for o in orders)
print(sum(amounts))
print(sum(amounts))''',
   "task": "A new analyst wants the total and the average amount. Say what the code below prints. Then rewrite it so it prints the total, and then the average (total divided by count).",
   "hint": "Make a list once with square brackets. Then use sum() and len() on the list.",
   "answer": '''amounts = [o["amount"] for o in orders]
print(sum(amounts))
print(sum(amounts) / len(amounts))'''},
 ],
 "py-except-order": [
  {"title": "A. A custom error that is also a ValueError", "setup": "",
   "broken": '''class NegativeAmountError(ValueError):
    pass

def parse_amount(text):
    value = float(text)
    if value < 0:
        raise NegativeAmountError(text)
    return value

for text in ["12.5", "abc", "-3"]:
    try:
        print(parse_amount(text))
    except ValueError:
        print("not a number")
    except NegativeAmountError:
        print("negative")''',
   "task": "Say what the code below prints for the three inputs. One result is wrong for the job. Fix the code so '-3' prints negative and 'abc' prints not a number.",
   "hint": "NegativeAmountError is a kind of ValueError. Which block must come first?",
   "answer": '''class NegativeAmountError(ValueError):
    pass

def parse_amount(text):
    value = float(text)
    if value < 0:
        raise NegativeAmountError(text)
    return value

for text in ["12.5", "abc", "-3"]:
    try:
        print(parse_amount(text))
    except NegativeAmountError:
        print("negative")
    except ValueError:
        print("not a number")'''},
 ],
 "py-class-property": [
  {"title": "A. A class with a list, a property and a sort", "setup": "",
   "task": "Write class Order. It starts with a customer name and an empty list of items. The method add_item(name, qty, price) saves one item. The property total is the sum of qty times price. __repr__ returns text like Order('Acme', total=45.0). Make three orders. Print them from highest total to lowest.",
   "hint": "Make the list inside __init__, not as a default. Use sorted(list, key=lambda o: o.total, reverse=True). Do not write brackets after total.",
   "answer": '''class Order:
    def __init__(self, customer):
        self.customer = customer
        self.items = []

    def add_item(self, name, qty, price):
        self.items.append((name, qty, price))

    @property
    def total(self):
        return sum(qty * price for _, qty, price in self.items)

    def __repr__(self):
        return f"Order({self.customer!r}, total={self.total})"

a = Order("Acme")
a.add_item("pen", 10, 2.5)
a.add_item("ink", 2, 10)
b = Order("Birch")
b.add_item("desk", 1, 120)
c = Order("Cobalt")
c.add_item("pad", 4, 5)
print(sorted([a, b, c], key=lambda o: o.total, reverse=True))'''},
 ],
}

def run(code):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(code, {"__name__": "__main__"})
    except Exception as e:  # an error is a valid result for a "broken code" task
        buf.write(("\n" if buf.getvalue() and not buf.getvalue().endswith("\n") else "") + f"{type(e).__name__}: {e}")
    return buf.getvalue().rstrip()

def run_all():
    out = {}
    for tid, tasks in TASKS.items():
        res = []
        for t in tasks:
            setup = t.get("setup", "")
            item = {"title": t["title"], "task": t["task"], "hint": t["hint"], "setup": setup, "sql": t["answer"],
                    "output": run(setup + "\n" + t["answer"]), "lang": "python"}
            if t.get("broken"):
                item["broken"] = t["broken"]; item["brokenOutput"] = run(setup + "\n" + t["broken"])
            res.append(item)
        out[tid] = res
    return out

if __name__ == "__main__":
    for tid, ts in run_all().items():
        for t in ts:
            print("=====", tid, t["title"])
            if "broken" in t: print("-- broken prints:\n" + t["brokenOutput"])
            print("-- answer prints:\n" + t["output"])
