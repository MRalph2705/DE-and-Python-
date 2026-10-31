"""Module 2 lessons, part A: classes, dataclasses, decorators (+ mixed tasks for the held class-property lesson).
Every example and mixed task is RUN when the site is built. Claims are asserted in CHECKS."""
from build_topics import box, text, arrow, line, svg


def C(s):
    return s.strip("\n")


# ------------------------------------------------------------------ diagrams
def d_class():
    b = []
    b.append(box(0, 8, 210, 100, "bxg"))
    b.append(text(105, 28, "class Order  (the plan)", "tx tb", "middle", 12))
    b.append(text(105, 52, "__init__(self, customer)", "tx", "middle", 11))
    b.append(text(105, 72, "add_item(self, name, qty, price)", "tx", "middle", 11))
    b.append(text(105, 92, "total(self)", "tx", "middle", 11))
    b.append(box(290, 8, 230, 44, "bxa"))
    b.append(text(405, 26, "a = Order('Acme')", "tx tb", "middle", 12))
    b.append(text(405, 43, "a.customer = 'Acme'   a.items = [ ]", "tx", "middle", 11))
    b.append(box(290, 64, 230, 44, "bxa"))
    b.append(text(405, 82, "b = Order('Birch')", "tx tb", "middle", 12))
    b.append(text(405, 99, "b.customer = 'Birch'   b.items = [ ]", "tx", "middle", 11))
    b.append(arrow(210, 36, 288, 30, "m2a")); b.append(arrow(210, 80, 288, 86, "m2a"))
    b.append(text(250, 14, "make", "tx tm", "middle", 11))
    b.append(line(0, 128, 520, 128, "ln"))
    b.append(box(0, 142, 210, 50, "bxw"))
    b.append(text(105, 162, "class RushOrder(Order)", "tx tb", "middle", 12))
    b.append(text(105, 181, "adds fee, reuses the rest", "tx", "middle", 11))
    b.append(arrow(105, 142, 105, 110, "m2a"))
    b.append(text(118, 128, "inherits", "tx tm", "start", 11))
    b.append(text(232, 160, "self is the object the method", "tx tb", "start", 12))
    b.append(text(232, 176, "is called on.", "tx tb", "start", 12))
    b.append(text(232, 194, "a.total() runs total with self = a.", "tx", "start", 11))
    return svg(208, "".join(b), "A class is a plan. Each object made from it has its own values. A subclass inherits from it.", "m2a")


def d_dataclass():
    b = []
    b.append(box(0, 8, 230, 98, "bxg"))
    b.append(text(115, 28, "@dataclass", "tx tb", "middle", 12))
    b.append(text(115, 48, "class Order:", "tx", "middle", 12))
    b.append(text(115, 68, "id: int   customer: str", "tx", "middle", 12))
    b.append(text(115, 88, "amount: float", "tx", "middle", 12))
    for i, (n, d) in enumerate([("__init__", "sets the fields"), ("__repr__", "Order(id=1, ...)"), ("__eq__", "compares fields")]):
        y = 8 + i * 36
        b.append(arrow(230, 57, 300, y + 15, "m2b"))
        b.append(box(302, y, 218, 30, "bxa"))
        b.append(text(312, y + 20, n, "tx tb", "start", 12))
        b.append(text(400, y + 20, d, "tx", "start", 11))
    b.append(text(0, 134, "You write the fields. Python writes the three methods.", "tx tb", "start", 12))
    b.append(text(0, 156, "A list field needs field(default_factory=list), not = [ ].", "tx tw tb", "start", 12))
    return svg(172, "".join(b), "A dataclass turns three field lines into an init, a repr and an equality method.", "m2b")


def d_decorator():
    b = []
    b.append(text(0, 36, "total_price(3, 10)", "tx tb", "start", 12))
    b.append(arrow(120, 30, 168, 30, "m2c"))
    b.append(box(170, 6, 220, 196, "bxa", 10))
    b.append(text(280, 24, "wrapper  (from @log_calls)", "tx tb", "middle", 12))
    steps = [("print 'calling ...'", "bx"), ("func(*args, **kwargs)", "bxg"), ("print 'returned ...'", "bx"), ("return result", "bx")]
    for i, (lab, cls) in enumerate(steps):
        y = 36 + i * 42
        b.append(box(190, y, 180, 32, cls))
        b.append(text(280, y + 21, lab, "tx", "middle", 12))
        if i < 3:
            b.append(arrow(280, y + 32, 280, y + 42, "m2c"))
    b.append(arrow(390, 184, 438, 184, "m2c"))
    b.append(text(444, 188, "36.0", "tx tb", "start", 12))
    b.append(text(0, 100, "@log_calls", "tx tw tb", "start", 12))
    b.append(text(0, 118, "means", "tx tm", "start", 11))
    b.append(text(0, 136, "total_price =", "tx", "start", 11))
    b.append(text(0, 152, "log_calls(total_price)", "tx", "start", 11))
    return svg(212, "".join(b), "A decorator wraps a function. The wrapper runs extra steps around the original call.", "m2c")


# ------------------------------------------------------------------ lessons
LESSONS = [
 {"id": "py-classes", "track": "Python", "title": "Classes: objects, attributes and methods", "minutes": 45,
  "summary": "A class is a plan. Each object keeps its own data. Methods work on that data.",
  "teaches": ["class", "init", "self", "methods", "inherit", "isinstance", "raise"],
  "uses": ["def", "return", "list", "tuple", "unpack", "list-methods", "generator-expr", "sum-min-max", "float", "int", "str", "print", "loop-for", "try-except", "f-string"],
  "picture": {"svg": d_class(), "caption": "One plan, many objects. Each object has its own values. A subclass reuses the plan."},
  "predict": {"q": C("""
class Counter:
    def __init__(self):
        self.n = 0

    def hit(self):
        self.n = self.n + 1

c = Counter()
c.hit()
c.hit()
print(c.n)
What does the last line print?"""), "reveal": "2. __init__ sets n to 0. Each call to hit adds 1 to the n of this one object."},
  "explain": [
   {"h": "What it is", "p": [
     "A class is a plan for objects. An object holds data and has methods.",
     "The data in an object is stored in attributes. self.customer is an attribute.",
     "A method is a function that belongs to a class. Its first parameter is self.",
     "You make an object by calling the class: a = Order('Acme')."]},
   {"h": "self and __init__", "p": [
     "self is the object that the method works on. Python passes it for you.",
     "In a.total(), Python runs total with self set to a. You do not write self in the call.",
     "__init__ runs when the object is made. It sets the first attributes.",
     "Write self. before every attribute: self.items. Without self. the name is only a local variable."]},
   {"h": "Each object has its own data", "p": [
     "Make a new list inside __init__: self.items = [ ]. Each object then gets its own list.",
     "Two objects do not share attributes. a.items is not b.items."]},
   {"h": "Inheritance", "p": [
     "A subclass takes everything from its parent class. Write the parent in brackets: class RushOrder(Order).",
     "A subclass __init__ must accept every value the parent needs, plus its own.",
     "super().__init__(customer) runs the parent __init__. super().total() runs the parent method.",
     "isinstance(b, Order) is True when b is an Order or a subclass of Order."]},
   {"h": "Your own errors", "p": [
     "raise stops the code and sends an error: raise ValueError('too much').",
     "A custom error is a small subclass: class InsufficientFundsError(Exception): pass.",
     "except catches it by name, exactly as in the try/except lesson."]},
   {"h": "Common mistakes", "p": [
     "Forget self in def: def total(): fails with a TypeError when you call a.total().",
     "Forget self. in front of an attribute: items = [ ] makes a local name and loses it.",
     "Write __init without the closing underscores. Python then does not treat it as the constructor."]}],
  "example": {"title": "Order, RushOrder and isinstance", "code": C(r"""
class Order:
    def __init__(self, customer):
        self.customer = customer
        self.items = []

    def add_item(self, name, qty, price):
        self.items.append((name, qty, price))

    def total(self):
        return sum(qty * price for _, qty, price in self.items)


class RushOrder(Order):
    def __init__(self, customer, fee):
        super().__init__(customer)
        self.fee = fee

    def total(self):
        return super().total() + self.fee


a = Order("Acme")
a.add_item("pen", 10, 2.5)
a.add_item("ink", 2, 10)
b = RushOrder("Birch", 5)
b.add_item("desk", 1, 120)
print(a.customer, a.total())
print(b.customer, b.total())
print(isinstance(b, Order), isinstance(a, RushOrder))
a2 = Order("Acme")
print(a2.items, a.items is a2.items)""")},
  "qa": {"q": C("""
class Box:
    def describe():
        return "a box"

print(Box().describe())
What does this do? How do you fix it?"""), "a": "It raises TypeError: Box.describe() takes 0 positional arguments but 1 was given. Python passes the object as the first argument. Write def describe(self):."},
  "build": {"task": "From a blank page write class Account with __init__(self, owner, balance=0), deposit(amount) and withdraw(amount). withdraw raises ValueError('insufficient funds') when the amount is more than the balance. Then write SavingsAccount(Account) with an extra rate and a method add_interest() that adds balance * rate. Test: Account('Ann', 100) deposit 50 gives 150. withdraw 500 raises ValueError. SavingsAccount('Ben', 200, 0.1) after add_interest has balance 220.0.",
            "hint": "SavingsAccount.__init__(self, owner, balance, rate) calls super().__init__(owner, balance) and then sets self.rate. Catch the error with try/except ValueError in your test.",
            "check": "You should see 150, then the text insufficient funds, then 220.0."},
  "teach": "Explain in 5 sentences what self is and why a method needs it.",
  "mistakes": [],
  "selfCheck": [{"q": "Where do you make a list that each object must own?", "a": "Inside __init__, as self.items = [ ]."},
                {"q": "What does super().__init__(customer) do?", "a": "It runs the __init__ of the parent class, so the parent sets its attributes."},
                {"q": "Do you write self when you call a method?", "a": "No. Python passes it. You write it only in the def line."}]},

 {"id": "py-dataclasses", "track": "Python", "title": "Dataclasses", "minutes": 35,
  "summary": "A dataclass writes __init__, __repr__ and __eq__ for you. You list the fields.",
  "teaches": ["dataclass", "annotation", "default-factory", "frozen", "asdict"],
  "uses": ["class", "init", "self", "methods", "repr", "property", "list", "dict", "csv", "stringio", "json", "import", "mutable-default", "loop-for", "list-comp", "sorted", "lambda", "sort-key", "float", "int", "str", "print", "f-string"],
  "picture": {"svg": d_dataclass(), "caption": "You write the fields. The decorator writes the methods."},
  "predict": {"q": C("""
from dataclasses import dataclass

@dataclass
class Parcel:
    id: int
    tags: list = []
What happens when Python reads this class?"""), "reveal": "It raises ValueError: mutable default <class 'list'> for field tags is not allowed: use default_factory. This is the mutable default problem again. A dataclass stops it for you."},
  "explain": [
   {"h": "What it is", "p": [
     "A dataclass is a class made mostly of data. You list the fields. Python writes the rest.",
     "Put @dataclass above the class. It writes __init__, __repr__ and __eq__.",
     "A field line has a name and a type hint: amount: float. A type hint is the part after the colon.",
     "Python does not check the hint when the code runs. The next lessons show a tool that does."]},
   {"h": "Defaults", "p": [
     "A field with a simple default: rate: float = 0.2. Fields with defaults go last.",
     "A list or dict default needs field(default_factory=list). Each object then gets a new list.",
     "tags: list = [ ] is refused with a ValueError."]},
   {"h": "Useful features", "p": [
     "Two dataclass objects are equal when all fields are equal.",
     "@dataclass(frozen=True) makes the object read-only. Changing a field raises an error.",
     "asdict(obj) turns the object into a dict. Use it with json.dumps.",
     "You can still add methods and @property to a dataclass."]},
   {"h": "Where you use them", "p": [
     "Turn each CSV row into one dataclass object. Convert the types once, in one place.",
     "Then the rest of the code uses order.amount as a float, not text.",
     "A dataclass is a clear record type for data you load, move and save."]}],
  "example": {"title": "CSV rows into dataclass objects", "code": C(r"""
from dataclasses import dataclass, field, asdict
import csv
import io
import json


@dataclass
class Order:
    id: int
    customer: str
    amount: float
    tags: list = field(default_factory=list)


raw = "id,customer,amount\n1,Acme,120\n2,Birch,40\n"
orders = [Order(int(r["id"]), r["customer"], float(r["amount"])) for r in csv.DictReader(io.StringIO(raw))]
print(orders[0])
print(orders[0] == Order(1, "Acme", 120.0))
orders[1].tags.append("late")
print(orders[0].tags, orders[1].tags)
print(json.dumps(asdict(orders[1])))""")},
  "qa": {"q": C("""
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

p = Point(1, 2)
p.x = 5
What happens?"""), "a": "It raises FrozenInstanceError: cannot assign to field 'x'. A frozen dataclass is read-only."},
  "build": {"task": "From a blank page write a dataclass Trip with id (int), km (float) and rate (float, default 0.45), and a property cost that returns km * rate. Read these rows with csv: id,km  then 1,10  2,4  3,25. Make a Trip for each row. Print the trips from the highest cost to the lowest.",
            "hint": "Put the dataclass on top. Use csv.DictReader with io.StringIO. Convert with int() and float(). Sort with key=lambda t: t.cost and reverse=True.",
            "check": "The order is trip 3 (cost 11.25), trip 1 (4.5), trip 2 (1.8)."},
  "teach": "Explain in 5 sentences what @dataclass writes for you and why that is useful for CSV rows.",
  "mistakes": [],
  "selfCheck": [{"q": "How do you give a dataclass field an empty list as its default?", "a": "tags: list = field(default_factory=list)."},
                {"q": "What does frozen=True do?", "a": "It makes the object read-only. Changing a field raises an error."},
                {"q": "Does Python check that amount: float really holds a float?", "a": "No. The hint is not checked when the code runs."}]},

 {"id": "py-decorators", "track": "Python", "title": "Decorators and closures", "minutes": 45,
  "summary": "A closure remembers values. A decorator wraps a function to add steps around it.",
  "teaches": ["args-kwargs", "closure", "decorator", "wraps"],
  "uses": ["def", "return", "scope", "params-defaults", "import", "loop-for", "range", "list", "dict", "f-string", "try-except", "raise", "print", "tuple", "int", "round"],
  "picture": {"svg": d_decorator(), "caption": "The wrapper runs before and after the real function. The caller does not notice."},
  "predict": {"q": C("""
def make_adder(n):
    def add(x):
        return x + n
    return add

add5 = make_adder(5)
print(add5(10))
What does this print?"""), "reveal": "15. The inner function add remembers n from the call that made it. This is a closure."},
  "explain": [
   {"h": "Functions are values", "p": [
     "A function is a value. You can store it, pass it and return it.",
     "A function inside a function is a nested function.",
     "A closure is a nested function that remembers names from the outer function. add remembers n."]},
   {"h": "*args and **kwargs", "p": [
     "*args collects extra positional arguments into a tuple.",
     "**kwargs collects extra keyword arguments into a dict.",
     "func(*args, **kwargs) passes them on unchanged. A wrapper needs this to accept any call."]},
   {"h": "A decorator", "p": [
     "A decorator is a function that takes a function and returns a new function.",
     "@log_calls above def total_price means total_price = log_calls(total_price).",
     "The new function is the wrapper. It runs your extra steps and calls the original.",
     "Always return the result of the original call, or the caller gets None."]},
   {"h": "functools.wraps", "p": [
     "Without @functools.wraps(func), the wrapper hides the name of the original function.",
     "Put @functools.wraps(func) on the wrapper. The name and the docstring then stay correct."]},
   {"h": "A decorator with an argument", "p": [
     "@retry(3) needs one more level. retry(3) returns the decorator. The decorator returns the wrapper.",
     "Read it from the outside in: retry gets the number, decorator gets the function, wrapper gets the call.",
     "Data jobs use this for retries, logging and timing."]}],
  "example": {"title": "A logging decorator and a retry decorator", "code": C(r"""
import functools


def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__} with {args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper


@log_calls
def total_price(qty, unit_price, vat_rate=0.2):
    return round(qty * unit_price * (1 + vat_rate), 2)


total_price(3, 10, vat_rate=0)
print(total_price.__name__)


def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError:
                    print(f"attempt {attempt} failed")
            raise ConnectionError("gave up")
        return wrapper
    return decorator


calls = []


@retry(3)
def fetch():
    calls.append(1)
    if len(calls) < 3:
        raise ConnectionError("down")
    return "data"


print(fetch())""")},
  "qa": {"q": C("""
import functools

def log_calls(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@log_calls
def total_price(qty):
    return qty

print(total_price.__name__)
What does this print? Why?"""), "a": "It prints wrapper. The decorator replaced total_price with the wrapper function, and the wrapper has its own name. Add @functools.wraps(func) above def wrapper to keep the name total_price."},
  "build": {"task": "From a blank page write a decorator audit that adds the name of each called function to a list called audit_log. Decorate two functions, for example add(a, b) and shout(text). Call each one. The return values must stay correct. Then print audit_log and the __name__ of one decorated function.",
            "hint": "Make audit_log a list outside the decorator. Use *args and **kwargs in the wrapper. Return the result. Use functools.wraps.",
            "check": "audit_log shows the two names in the order of the calls. The __name__ is the original name, not wrapper."},
  "teach": "Explain in 5 sentences what @log_calls above a function really does.",
  "mistakes": [],
  "selfCheck": [{"q": "What is a closure?", "a": "A nested function that remembers names from the outer function."},
                {"q": "What do *args and **kwargs collect?", "a": "Extra positional arguments (as a tuple) and extra keyword arguments (as a dict)."},
                {"q": "What happens if the wrapper does not return the result?", "a": "The caller gets None instead of the real result."}]},
]


# ------------------------------------------------------------------ mixed tasks
MIXED = {
 "py-classes": [
  {"title": "A. Stock item with a sale method", "setup": "",
   "task": "Write class Item with name and stock (the number in stock). Add a method sell(qty). It lowers stock by qty. It raises ValueError('not enough stock') if qty is more than stock. Make Item('pen', 10). Sell 4. Print the stock. Then try to sell 20 inside try/except ValueError and print the error text.",
   "hint": "Use self.stock. The check goes before the subtraction. In the except line, use as e and print(e).",
   "answer": C(r"""
class Item:
    def __init__(self, name, stock):
        self.name = name
        self.stock = stock

    def sell(self, qty):
        if qty > self.stock:
            raise ValueError("not enough stock")
        self.stock = self.stock - qty


pen = Item("pen", 10)
pen.sell(4)
print(pen.stock)
try:
    pen.sell(20)
except ValueError as e:
    print(e)""")},
  {"title": "B. Fix the class", "setup": "",
   "broken": C(r"""
class Counter:
    def __init__(self):
        n = 0

    def hit():
        self.n = self.n + 1

c = Counter()
c.hit()
print(c.n)"""),
   "task": "This code has two errors. Say what Python reports first. Then fix both so it prints 1.",
   "hint": "One method is missing self in its def line. One attribute is missing the self. prefix.",
   "answer": C(r"""
class Counter:
    def __init__(self):
        self.n = 0

    def hit(self):
        self.n = self.n + 1

c = Counter()
c.hit()
print(c.n)""")},
  {"title": "C. A subclass with super", "setup": "",
   "task": "A class Person has name. Write class Customer(Person) with a credit limit. Customer.describe() returns the name and the limit, like: Acme (limit 500). Person has its own describe() that returns just the name. Print both for Person('Ann') and Customer('Acme', 500).",
   "hint": "Customer.__init__(self, name, limit) calls super().__init__(name). describe in Customer can call super().describe().",
   "answer": C(r"""
class Person:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return self.name


class Customer(Person):
    def __init__(self, name, limit):
        super().__init__(name)
        self.limit = limit

    def describe(self):
        return f"{super().describe()} (limit {self.limit})"


print(Person("Ann").describe())
print(Customer("Acme", 500).describe())""")},
 ],
 "py-class-property": [
  {"title": "A. A class with a list, a property and a sort", "setup": "",
   "task": "Write class Order. It starts with a customer name and an empty list of items. The method add_item(name, qty, price) saves one item. The property total is the sum of qty times price. __repr__ returns text like Order('Acme', total=45.0). Make three orders. Print them from highest total to lowest.",
   "hint": "Make the list inside __init__, not as a default. Use sorted(list, key=lambda o: o.total, reverse=True). Do not write brackets after total.",
   "answer": C(r"""
class Order:
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
print(sorted([a, b, c], key=lambda o: o.total, reverse=True))""")},
  {"title": "B. Fix the repr and the call", "setup": "",
   "broken": C(r"""
class Invoice:
    def __init__(self, amount, vat_rate):
        self.amount = amount
        self.vat_rate = vat_rate

    @property
    def total(self):
        return self.amount * (1 + self.vat_rate)

    def __repr__(self):
        f"Invoice({self.amount}, total={self.total})"


inv = Invoice(250, 0.2)
print(inv.total())
print(inv)"""),
   "task": "This code has two errors. Say what Python reports for the first one. Fix both so it prints 300.0 and then Invoice(250, total=300.0).",
   "hint": "A property is read without brackets. __repr__ must return the text.",
   "answer": C(r"""
class Invoice:
    def __init__(self, amount, vat_rate):
        self.amount = amount
        self.vat_rate = vat_rate

    @property
    def total(self):
        return self.amount * (1 + self.vat_rate)

    def __repr__(self):
        return f"Invoice({self.amount}, total={self.total})"


inv = Invoice(250, 0.2)
print(inv.total)
print(inv)""")},
 ],
 "py-dataclasses": [
  {"title": "A. Rows to records, then totals", "setup": "",
   "task": "Make a dataclass Line with sku (str), qty (int) and price (float). Read these rows with csv: sku,qty,price  then A1,3,2.5  B2,1,10  A1,2,2.5. Make a Line for each row. Print the total value of all lines. Then print the quantity for each sku in a dict.",
   "hint": "Convert qty with int() and price with float(). For the dict, loop and use dict.get(sku, 0) + qty.",
   "answer": C(r"""
from dataclasses import dataclass
import csv
import io

raw = "sku,qty,price\nA1,3,2.5\nB2,1,10\nA1,2,2.5\n"


@dataclass
class Line:
    sku: str
    qty: int
    price: float


lines = [Line(r["sku"], int(r["qty"]), float(r["price"])) for r in csv.DictReader(io.StringIO(raw))]
print(sum(l.qty * l.price for l in lines))
by_sku = {}
for l in lines:
    by_sku[l.sku] = by_sku.get(l.sku, 0) + l.qty
print(by_sku)""")},
  {"title": "B. Fix the shared list", "setup": "",
   "broken": C(r"""
from dataclasses import dataclass

@dataclass
class Basket:
    owner: str
    items: list = []

a = Basket("Ann")
print(a)"""),
   "task": "This code fails when Python reads the class. Say what the error is. Fix it. Then make two baskets, add one item to the first and show that the second stays empty.",
   "hint": "Import field from dataclasses. Use field(default_factory=list).",
   "answer": C(r"""
from dataclasses import dataclass, field


@dataclass
class Basket:
    owner: str
    items: list = field(default_factory=list)


a = Basket("Ann")
b = Basket("Bo")
a.items.append("pen")
print(a)
print(b)""")},
  {"title": "C. A read-only record to JSON", "setup": "",
   "task": "Make a frozen dataclass Rate with currency (str) and value (float). Make Rate('EUR', 1.17). Try to change value to 2.0 inside try/except and print the name of the error type. Then print the record as JSON.",
   "hint": "Use except Exception as e and print(type(e).__name__). Use json.dumps(asdict(rate)).",
   "answer": C(r"""
from dataclasses import dataclass, asdict
import json


@dataclass(frozen=True)
class Rate:
    currency: str
    value: float


rate = Rate("EUR", 1.17)
try:
    rate.value = 2.0
except Exception as e:
    print(type(e).__name__)
print(json.dumps(asdict(rate)))""")},
 ],
 "py-decorators": [
  {"title": "A. Count the calls", "setup": "",
   "task": "Write a decorator count_calls. It counts how many times the function runs. Keep the count on the wrapper as wrapper.calls. Decorate a function square(n). Call it three times. Print the count.",
   "hint": "Set wrapper.calls = 0 after you define the wrapper. Add 1 inside the wrapper. Return the result of the call.",
   "answer": C(r"""
import functools


def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


@count_calls
def square(n):
    return n * n


print(square(2), square(3), square(4))
print(square.calls)""")},
  {"title": "B. Check the input", "setup": "",
   "task": "Write a decorator require_positive. It checks that the first argument is more than 0. If not, it raises ValueError('must be positive'). Decorate net_to_gross(net) that returns net * 1.2. Call it with 100 and with -5. Catch the error and print its text.",
   "hint": "In the wrapper, check args[0] before you call func. Remember to return the result.",
   "answer": C(r"""
import functools


def require_positive(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args[0] <= 0:
            raise ValueError("must be positive")
        return func(*args, **kwargs)
    return wrapper


@require_positive
def net_to_gross(net):
    return net * 1.2


print(net_to_gross(100))
try:
    net_to_gross(-5)
except ValueError as e:
    print(e)""")},
  {"title": "C. Fix the decorator", "setup": "",
   "broken": C(r"""
def shout(func):
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        text.upper()
    return wrapper

@shout
def greet(name):
    return "hello " + name

print(greet("ann"))"""),
   "task": "This prints something unexpected. Say what and why. Fix it so it prints HELLO ANN.",
   "hint": "Two lines work out a value but never send it back.",
   "answer": C(r"""
def shout(func):
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        return text.upper()
    return wrapper


@shout
def greet(name):
    return "hello " + name


print(greet("ann"))""")},
 ],
}

CHECKS = [
 (C("""
class Counter:
    def __init__(self):
        self.n = 0

    def hit(self):
        self.n = self.n + 1

c = Counter()
c.hit()
c.hit()
print(c.n)"""), "2"),
 (C("""
class Box:
    def describe():
        return "a box"

print(Box().describe())"""), "TypeError: Box.describe() takes 0 positional arguments but 1 was given"),
 (C("""
class Counter:
    def __init__(self):
        n = 0

    def hit():
        self.n = self.n + 1

c = Counter()
c.hit()
print(c.n)"""), "TypeError: Counter.hit() takes 0 positional arguments but 1 was given"),
 (C("""
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance = self.balance - amount


class SavingsAccount(Account):
    def __init__(self, owner, balance, rate):
        super().__init__(owner, balance)
        self.rate = rate

    def add_interest(self):
        self.balance = self.balance + self.balance * self.rate


acc = Account("Ann", 100)
acc.deposit(50)
print(acc.balance)
try:
    acc.withdraw(500)
except ValueError as e:
    print(e)
sav = SavingsAccount("Ben", 200, 0.1)
sav.add_interest()
print(sav.balance)"""), "150\ninsufficient funds\n220.0"),
 (C("""
from dataclasses import dataclass

@dataclass
class Parcel:
    id: int
    tags: list = []"""), "ValueError: mutable default <class 'list'> for field tags is not allowed: use default_factory"),
 (C("""
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

p = Point(1, 2)
p.x = 5"""), "FrozenInstanceError: cannot assign to field 'x'"),
 (C(r"""
from dataclasses import dataclass, field
import csv
import io


@dataclass
class Trip:
    id: int
    km: float
    rate: float = 0.45

    @property
    def cost(self):
        return self.km * self.rate


raw = "id,km\n1,10\n2,4\n3,25\n"
trips = [Trip(int(r["id"]), float(r["km"])) for r in csv.DictReader(io.StringIO(raw))]
for t in sorted(trips, key=lambda t: t.cost, reverse=True):
    print(t.id, round(t.cost, 2))"""), "3 11.25\n1 4.5\n2 1.8"),
 (C("""
def make_adder(n):
    def add(x):
        return x + n
    return add

add5 = make_adder(5)
print(add5(10))"""), "15"),
 (C("""
import functools

def log_calls(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@log_calls
def total_price(qty):
    return qty

print(total_price.__name__)"""), "wrapper"),
 (C("""
import functools

audit_log = []

def audit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        audit_log.append(func.__name__)
        return func(*args, **kwargs)
    return wrapper

@audit
def add(a, b):
    return a + b

@audit
def shout(text):
    return text.upper()

print(add(2, 3), shout("hi"))
print(audit_log, add.__name__)"""), "5 HI\n['add', 'shout'] add"),
 (C("""
def shout(func):
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        text.upper()
    return wrapper

@shout
def greet(name):
    return "hello " + name

print(greet("ann"))"""), "None"),
 (C("""
class Invoice:
    def __init__(self, amount, vat_rate):
        self.amount = amount
        self.vat_rate = vat_rate

    @property
    def total(self):
        return self.amount * (1 + self.vat_rate)

    def __repr__(self):
        f"Invoice({self.amount}, total={self.total})"

inv = Invoice(250, 0.2)
print(inv.total())"""), "TypeError: 'float' object is not callable"),
]
