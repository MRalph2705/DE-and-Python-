"""Module 1 lessons (new). Every example and every mixed task is RUN when the site is built.
Claims in predict/Q&A text are asserted in CHECKS (run at build time)."""
from build_topics import box, text, arrow, line, svg


# ------------------------------------------------------------------ diagrams
def d_types():
    b = []
    rows = [("price", "19.99", "float"), ("qty", "3", "int"), ("name", '"pen"', "str"), ("paid", "True", "bool"), ("note", "None", "NoneType")]
    for i, (n, v, t) in enumerate(rows):
        y = 8 + i * 44
        b.append(box(0, y, 110, 34, "bx"))
        b.append(text(55, y + 23, n, "tx tb", "middle"))
        b.append(arrow(110, y + 17, 168, y + 17, "t1"))
        b.append(box(170, y, 150, 34, "bxa"))
        b.append(text(245, y + 23, v, "tx", "middle"))
        b.append(box(350, y, 110, 34, "bxg"))
        b.append(text(405, y + 23, t, "tx tb", "middle"))
    b.append(text(55, 238, "name", "tx tm", "middle", 11))
    b.append(text(245, 238, "value", "tx tm", "middle", 11))
    b.append(text(405, 238, "type of the value", "tx tm", "middle", 11))
    return svg(250, "".join(b), "Five variable names, each pointing to a value with a type.", "t1")


def d_strings():
    b = []
    s = "ORD-1042-uk"
    for i, ch in enumerate(s):
        x = 10 + i * 45
        b.append(text(x + 20, 18, str(i), "tx tm", "middle", 11))
        b.append(box(x, 24, 40, 36, "bx", 6))
        b.append(text(x + 20, 48, ch, "tx tb", "middle", 15))
    bars = [(0, 3, "bxa", "code[0:3]  gives  ORD", 82), (4, 8, "bxg", "code[4:8]  gives  1042", 118), (9, 11, "bxw", "code[-2:]  gives  uk", 154)]
    for a, z, cls, lab, y in bars:
        b.append(box(10 + a * 45, y - 14, (z - a) * 45 - 5, 10, cls, 4))
        b.append(text(10 + a * 45, y + 10, lab, "tx tb", "start", 12))
    b.append(text(10, 192, "A slice stops before its end index.", "tx tm", "start", 12))
    return svg(204, "".join(b), "The string ORD-1042-uk with index numbers and three slices.", "t2")


def d_lists():
    b = []
    vals = [120, 40, 80, 200]
    b.append(text(0, 14, "orders = [120, 40, 80, 200]", "tx tb", "start", 12))
    for i, v in enumerate(vals):
        x = i * 100
        b.append(text(x + 45, 34, f"{i}  /  {i - 4}", "tx tm", "middle", 11))
        b.append(box(x, 40, 90, 34, "bx"))
        b.append(text(x + 45, 63, str(v), "tx tb", "middle"))
    b.append(box(100, 82, 190, 8, "bxa", 3))
    b.append(text(100, 106, "orders[1:3]  gives  [40, 80]", "tx ta tb", "start", 12))
    b.append(line(0, 122, 520, 122, "ln"))
    b.append(text(0, 144, "b = a  (same list)", "tx tw tb", "start", 12))
    b.append(box(0, 154, 50, 28, "bx")); b.append(text(25, 173, "a", "tx tb", "middle"))
    b.append(box(0, 190, 50, 28, "bx")); b.append(text(25, 209, "b", "tx tb", "middle"))
    b.append(box(130, 168, 120, 36, "bxw")); b.append(text(190, 191, "[1, 2, 3]", "tx", "middle"))
    b.append(arrow(50, 168, 128, 182, "t3")); b.append(arrow(50, 204, 128, 192, "t3"))
    b.append(text(280, 144, "b = a.copy()  (two lists)", "tx tg tb", "start", 12))
    b.append(box(280, 154, 50, 28, "bx")); b.append(text(305, 173, "a", "tx tb", "middle"))
    b.append(box(280, 190, 50, 28, "bx")); b.append(text(305, 209, "b", "tx tb", "middle"))
    b.append(box(390, 154, 120, 28, "bxg")); b.append(text(450, 173, "[1, 2, 3]", "tx", "middle"))
    b.append(box(390, 190, 120, 28, "bxg")); b.append(text(450, 209, "[1, 2, 3, 9]", "tx", "middle"))
    b.append(arrow(330, 168, 388, 168, "t3")); b.append(arrow(330, 204, 388, 204, "t3"))
    return svg(228, "".join(b), "A list with indexes and a slice. Two names for one list, and a real copy.", "t3")


def d_control():
    b = []
    b.append(box(0, 8, 190, 36, "bxa")); b.append(text(95, 31, "for amount in amounts:", "tx tb", "middle", 12))
    b.append(arrow(95, 44, 95, 78, "t4"))
    b.append(box(10, 80, 170, 36, "bx")); b.append(text(95, 103, "amount >= 100 ?", "tx tb", "middle", 12))
    b.append(arrow(180, 98, 238, 98, "t4")); b.append(text(209, 90, "True", "tx tg tb", "middle", 11))
    b.append(box(240, 80, 220, 36, "bxg")); b.append(text(350, 103, "large = large + 1", "tx", "middle", 12))
    b.append(arrow(95, 116, 95, 150, "t4")); b.append(text(104, 138, "False: skip", "tx tm", "start", 11))
    b.append(box(10, 152, 170, 36, "bx")); b.append(text(95, 175, "total = total + amount", "tx", "middle", 12))
    b.append(line(350, 116, 350, 205, "ar")); b.append(line(350, 205, 270, 205, "ar")); b.append(arrow(270, 205, 4, 205, "t4"))
    b.append(line(4, 205, 4, 26, "ar")); b.append(arrow(4, 26, 0, 26, "t4"))
    b.append(text(140, 222, "next value: back to the top", "tx tm", "middle", 11))
    b.append(arrow(180, 170, 238, 170, "t4"))
    b.append(box(240, 152, 220, 36, "bx")); b.append(text(350, 175, "after the loop: print(total, large)", "tx", "middle", 11))
    return svg(236, "".join(b), "A for loop with an if test inside it, and a total that grows on every pass.", "t4")


def d_function():
    b = []
    for i, (lab, cls) in enumerate([("qty = 3", "bx"), ("unit_price = 10", "bx"), ("vat_rate = 0.2 (default)", "bxa")]):
        y = 8 + i * 42
        b.append(box(0, y, 170, 32, cls)); b.append(text(85, y + 21, lab, "tx", "middle", 12))
        b.append(arrow(170, y + 16, 218, 62, "t5"))
    b.append(box(220, 20, 170, 86, "bxg"))
    b.append(text(305, 42, "def total_price(...)", "tx tb", "middle", 12))
    b.append(text(305, 62, "net = qty * unit_price", "tx", "middle", 11))
    b.append(text(305, 80, "return net * (1 + vat_rate)", "tx", "middle", 11))
    b.append(arrow(390, 62, 432, 62, "t5"))
    b.append(box(434, 40, 86, 44, "bxa")); b.append(text(477, 66, "36.0", "tx tb", "middle"))
    b.append(line(0, 140, 520, 140, "ln"))
    b.append(text(0, 162, "Scope", "tx tb", "start", 12))
    b.append(box(0, 172, 240, 40, "bxg", 8)); b.append(text(120, 197, "inside: net exists (local)", "tx", "middle", 12))
    b.append(box(270, 172, 250, 40, "bxw", 8, True)); b.append(text(395, 197, "outside: print(net) is NameError", "tx tw", "middle", 12))
    return svg(226, "".join(b), "A function takes inputs, returns an output, and keeps its own names inside.", "t5")


def d_comp():
    b = []
    b.append(text(0, 14, "Loop", "tx tb", "start", 12))
    for i, l in enumerate(["large = []", "for o in orders:", "    if o[\"amount\"] >= 100:", "        large.append(o[\"id\"])"]):
        b.append(text(0, 36 + i * 20, l, "tx", "start", 12))
    b.append(line(0, 130, 520, 130, "ln"))
    b.append(text(0, 152, "Comprehension: same result in one line", "tx tb", "start", 12))
    segs = [("[", 0, 14, "bx"), ("o[\"id\"]", 14, 78, "bxg"), ("for o in orders", 94, 124, "bxa"), ("if o[\"amount\"] >= 100", 220, 192, "bxw"), ("]", 414, 14, "bx")]
    for lab, x, w, cls in segs:
        b.append(box(x, 164, w, 32, cls, 6)); b.append(text(x + w / 2, 185, lab, "tx", "middle", 11))
    b.append(text(53, 216, "what goes in", "tx tg", "middle", 11))
    b.append(text(156, 216, "the loop", "tx ta", "middle", 11))
    b.append(text(316, 216, "the filter (at the end)", "tx tw", "middle", 11))
    return svg(228, "".join(b), "A for loop with append next to the same job as a list comprehension, with each part labelled.", "t6")


def d_files():
    b = []
    steps = [("orders.csv", "text on disk", "bx"), ("csv.DictReader", "reads rows", "bxa"), ("rows", "list of dicts, values are str", "bxw"), ("float(row[...])", "make numbers", "bxa"), ("totals", "dict of floats", "bxg")]
    for i, (a, c, cls) in enumerate(steps):
        x = i * 104
        b.append(box(x, 10, 96, 62, cls)); b.append(text(x + 48, 34, a, "tx tb", "middle", 11)); b.append(text(x + 48, 54, c, "tx tm", "middle", 9))
        if i < 4:
            b.append(arrow(x + 96, 41, x + 104, 41, "t7"))
    b.append(arrow(480, 72, 480, 108, "t7"))
    b.append(box(300, 110, 180, 40, "bxg")); b.append(text(390, 135, "json.dumps(totals)", "tx tb", "middle", 12))
    b.append(arrow(300, 130, 262, 130, "t7"))
    b.append(box(100, 110, 160, 40, "bx")); b.append(text(180, 135, "totals.json (text)", "tx tb", "middle", 12))
    b.append(text(0, 182, "with open(...) as f:  Python closes the file when the block ends.", "tx tm", "start", 12))
    b.append(text(0, 202, "CSV and JSON are both text. CSV numbers arrive as str.", "tx tw", "start", 12))
    return svg(214, "".join(b), "A CSV file is read into rows of text values, converted to numbers, totalled, and saved as JSON.", "t7")


def d_scripts():
    b = []
    toks = [("python", 0, 80, "bx"), ("tool.py", 90, 90, "bxa"), ("orders.csv", 190, 110, "bxg"), ("--threshold 100", 310, 150, "bxw")]
    for lab, x, w, cls in toks:
        b.append(box(x, 8, w, 34, cls, 6)); b.append(text(x + w / 2, 30, lab, "tx tb", "middle", 12))
    notes = [("runs the file", 40), ("__name__ is '__main__'", 135), ("args.filename", 245), ("args.threshold = 100.0", 385)]
    for lab, x in notes:
        b.append(arrow(x, 42, x, 66, "t8")); b.append(text(x, 82, lab, "tx tm", "middle", 10))
    b.append(line(0, 104, 520, 104, "ln"))
    b.append(box(0, 118, 250, 58, "bxg")); b.append(text(125, 140, "python tool.py", "tx tb", "middle", 12)); b.append(text(125, 160, "main() runs", "tx", "middle", 12))
    b.append(box(270, 118, 250, 58, "bxw")); b.append(text(395, 140, "import tool  (from another file)", "tx tb", "middle", 12)); b.append(text(395, 160, "__name__ is 'tool'. main() does not run.", "tx", "middle", 11))
    b.append(text(0, 202, ".venv keeps this project's packages apart from every other project.", "tx tm", "start", 12))
    return svg(214, "".join(b), "The parts of a command line, and the difference between running a file and importing it.", "t8")


# -------------------------------------------------------------------- lessons
LESSONS = [
 {"id": "py-types", "track": "Python", "title": "Values, types and variables", "minutes": 35,
  "summary": "A variable is a name for a value. Every value has a type.",
  "teaches": ["run-code", "print", "variable", "int", "float", "str", "bool", "none", "type-fn", "arithmetic", "comparison", "convert-types", "round"], "uses": [],
  "picture": {"svg": d_types(), "caption": "Each name points to a value. Each value has a type."},
  "predict": {"q": "x = 7 / 2. What value does x hold? Is it an int or a float?",
              "reveal": "3.5. It is a float. The / sign always gives a float. Even 6 / 3 gives 2.0."},
  "explain": [
   {"h": "What it is", "p": [
     "A variable is a name that points to a value.",
     "The sign = stores a value in a name. Read it as 'set to'. price = 10 means: price is set to 10.",
     "Every value has a type. The type decides what you can do with the value.",
     "Five types matter first: int (a whole number), float (a number with a decimal point), str (text in quotes), bool (True or False) and None (no value)."]},
   {"h": "Run code", "p": [
     "Save code in a file that ends in .py. Run it with: python file.py.",
     "print() shows a value on the screen.",
     "A line that starts with # is a comment. Python ignores it.",
     "type(x) tells you the type of x."]},
   {"h": "Operators", "p": [
     "Use + - * / to add, subtract, multiply and divide.",
     "The / sign always gives a float. 6 / 3 gives 2.0.",
     "Use // for division that drops the decimal part. 7 // 2 gives 3.",
     "Use % for the remainder. 7 % 2 gives 1.",
     "Use ** for a power. 2 ** 3 gives 8.",
     "A comparison gives a bool. These are the signs: == != < > <= >=.",
     "One = stores a value. Two == compare two values. Mixing them up is a common mistake."]},
   {"h": "Text and numbers", "p": [
     "Quotes make text. '3' is a str. 3 is an int.",
     "The + sign joins two strings: '3' + '4' gives '34'.",
     "The + sign cannot join a str and an int. It raises TypeError.",
     "Use int() or float() to turn text into a number. Use str() to turn a number into text."]},
   {"h": "Floats", "p": [
     "A float stores an approximation. 0.1 + 0.2 gives 0.30000000000000004.",
     "Use round(value, 2) to show money with 2 decimal places.",
     "For exact money, store pence as an int, or use a decimal type in the database."]},
   {"h": "Names", "p": [
     "A name has letters, digits and underscores. It cannot start with a digit.",
     "Names are case sensitive. Price and price are two different names.",
     "Use lowercase names with underscores, such as unit_price."]}],
  "example": {"title": "Order arithmetic and types", "code": (
      "price = 19.99\nqty = 3\nname = \"pen\"\npaid = True\nnote = None\n\ntotal = price * qty\nprint(name, qty, price)\nprint(total)\n"
      "print(type(price), type(qty), type(name), type(paid), type(note))\nprint(7 / 2, 7 // 2, 7 % 2, 2 ** 3)\n"
      "print(\"3\" + \"4\", int(\"3\") + 4)\nprint(0.1 + 0.2)\nprint(round(0.1 + 0.2, 2))")},
  "qa": {"q": "age = '30'. What does print(age + 5) do? How do you make it show 35?",
         "a": "It raises TypeError: can only concatenate str (not \"int\") to str. The variable age holds text. Convert it first: print(int(age) + 5)."},
  "build": {"task": "Write a script from a blank page. A shop sells 4 items at 12.5 each. Add 20% VAT. Print the net total, the VAT and the gross total, each on its own line. Then print the type of the gross total.",
            "hint": "Store qty, unit_price and vat_rate in variables first. Do each sum on its own line.",
            "check": "You should see 50.0, 10.0 and 60.0, and then <class 'float'>."},
  "teach": "Explain in 4 sentences the difference between '3' + '4' and 3 + 4. Use the words 'str' and 'int'.",
  "mistakes": [],
  "selfCheck": [{"q": "What does 7 // 2 give?", "a": "3."}, {"q": "Which type does 6 / 3 give?", "a": "A float: 2.0."}]},

 {"id": "py-strings", "track": "Python", "title": "Strings and f-strings", "minutes": 35,
  "summary": "A string is text. Slices, methods and f-strings let you clean and show it.",
  "teaches": ["str-index", "str-slice", "str-methods", "f-string", "in-operator", "len"], "uses": ["str", "int", "print", "variable", "convert-types", "arithmetic"],
  "picture": {"svg": d_strings(), "caption": "Each character has an index. A slice stops before its end index."},
  "predict": {"q": "What does print('3' + '4') show?", "reveal": "34. The + sign joins two strings. It does not add them."},
  "explain": [
   {"h": "Index and slice", "p": [
     "A string is a row of characters. Each character has an index. The first index is 0.",
     "text[0] gives the first character. text[-1] gives the last.",
     "A slice text[2:5] gives the characters from index 2 up to, but not including, index 5.",
     "text[:3] starts at the start. text[3:] runs to the end.",
     "len(text) gives the number of characters.",
     "A string cannot change in place. Every method gives a new string."]},
   {"h": "Cleaning methods", "p": [
     ".strip() removes spaces at both ends.",
     ".upper() and .lower() change the case.",
     ".replace(old, new) swaps text.",
     ".split(sep) cuts a string into a list of parts.",
     "sep.join(list) joins a list into one string.",
     ".startswith(x) and the word in give True or False."]},
   {"h": "f-strings", "p": [
     "Put f before the quote. Put a value in braces: f'Hello {name}'.",
     "A format code follows a colon. {price:.2f} shows 2 decimal places.",
     "{n:,} adds commas: 1200 becomes 1,200.",
     "{rate:.1%} shows a percentage: 0.256 becomes 25.6%.",
     "{name:<8} pads the text to 8 characters, left aligned."]},
   {"h": "Common mistakes", "p": [
     "A method such as strip or upper does not change the original. Save the result: clean = raw.strip().",
     "A slice stops before the end index. code[4:8] has 4 characters, not 5.",
     "An f-string needs the f. Without it, Python prints the braces as they are."]}],
  "example": {"title": "Slice, clean and format", "code": (
      "code = \"ORD-1042-uk\"\nprint(code[0:3], code[-2:], code[4:8], len(code))\nparts = code.split(\"-\")\nprint(parts)\nprint(\"-\".join(parts))\n"
      "print(\"  pen  \".strip().upper())\nprint(code.replace(\"-\", \"_\"), \"uk\" in code, code.startswith(\"ORD\"))\n"
      "name = \"pen\"\nprice = 2.5\nqty = 1200\nprint(f\"{name:<8}|{price:.2f}|{qty:,}|{0.256:.1%}\")")},
  "qa": {"q": "code = 'uk-2024-q3'. Which slice gives 2024? How do you show the code in capital letters?",
         "a": "code[3:7] gives 2024. code.upper() gives UK-2024-Q3."},
  "build": {"task": "A raw order id is ' ord-1042 '. From a blank page: clean it, print it in capitals, then print its number part plus 1 as an int.",
            "hint": "Use strip, upper, split and int. Save each result in a variable.", "check": "You should see ORD-1042 and then 1043."},
  "teach": "Explain in 4 sentences what code[4:8] gives and why it stops at index 7.",
  "mistakes": [],
  "selfCheck": [{"q": "What is the first index of a string?", "a": "0."}, {"q": "Does name.upper() change name?", "a": "No. It gives a new string. Save it in a variable to keep it."}]},

 {"id": "py-lists-tuples", "track": "Python", "title": "Lists and tuples", "minutes": 40,
  "summary": "A list holds values in order and can change. A tuple holds values in order and cannot change.",
  "teaches": ["list", "list-index", "list-slice", "list-methods", "sorted", "tuple", "unpack", "alias", "in-list", "sum-min-max"],
  "uses": ["str-slice", "f-string", "arithmetic", "print", "variable", "len", "int", "float"],
  "picture": {"svg": d_lists(), "caption": "Top: list indexes and a slice. Bottom: b = a shares one list. A copy makes two lists."},
  "predict": {"q": "code = 'ORD-1042'. What does print(code[0:3]) show?", "reveal": "ORD. The slice starts at index 0 and stops before index 3."},
  "explain": [
   {"h": "Lists", "p": [
     "A list holds values in order. Write it with square brackets: [120, 40, 80].",
     "A list can change. A string cannot.",
     "Indexes work like strings. orders[0] is the first value. orders[-1] is the last.",
     "A slice gives a new list: orders[1:3].",
     "append(x) adds one value at the end. pop() removes the last value and gives it to you.",
     "len, sum, min and max work on a list of numbers.",
     "The word in tests if a value is in the list."]},
   {"h": "Sorting", "p": [
     "sorted(list) gives a new sorted list. The original stays the same.",
     "list.sort() sorts the list in place. It returns None.",
     "Add reverse=True to sort from high to low."]},
   {"h": "Tuples", "p": [
     "A tuple uses round brackets: (10, 20). It cannot change.",
     "Use a tuple for a fixed record, such as ('Acme', 3, 12.5).",
     "Unpacking gives each name one value: name, qty, price = record.",
     "A one-value tuple needs a comma: (5,). Without the comma, (5) is just the number 5.",
     "A trailing comma makes a tuple even without brackets: x = 5, makes a tuple."]},
   {"h": "Shared lists", "p": [
     "b = a does not copy the list. Both names point to the same list.",
     "A change through b also shows in a.",
     "Make a real copy with a.copy() or a[:]."]},
   {"h": "Common mistakes", "p": [
     "x = orders.sort() sets x to None. Use sorted(orders) when you need a new list.",
     "orders[10] on a list of 4 values raises IndexError.",
     "orders.append(5) changes the list. It does not return the list."]}],
  "example": {"title": "Lists, tuples and shared lists", "code": (
      "orders = [120, 40, 80, 200]\nprint(orders[0], orders[-1], orders[1:3], len(orders))\norders.append(60)\nprint(orders, sum(orders), min(orders), max(orders))\n"
      "print(sorted(orders, reverse=True)[:2])\nprint(orders)\nlast = orders.pop()\nprint(last, orders, 80 in orders)\n"
      "record = (\"Acme\", 3, 12.5)\nname, qty, price = record\nprint(name, qty * price)\nprint(type((5)), type((5,)))\n"
      "a = [1, 2]\nb = a\nb.append(3)\nprint(a)\nc = a.copy()\nc.append(9)\nprint(a, c)")},
  "qa": {"q": "scores = [3, 1, 2]. result = scores.sort(). What does print(result) show? How do you get a sorted copy?",
         "a": "None. The sort method changes the list in place and returns None. Use sorted(scores) to get a new sorted list."},
  "build": {"task": "prices = [12.5, 8.0, 20.0, 5.5]. From a blank page print: the cheapest price, the dearest price, the total, and the two dearest prices from high to low. Then print prices again to show it did not change.",
            "hint": "Use min, max, sum and sorted with reverse=True and a slice.",
            "check": "You should see 5.5, 20.0, 46.0, [20.0, 12.5] and then [12.5, 8.0, 20.0, 5.5]."},
  "teach": "Explain in 5 sentences why changing b also changes a after b = a.",
  "mistakes": [],
  "selfCheck": [{"q": "What does sorted(x) do to x?", "a": "Nothing. It returns a new list."}, {"q": "How do you write a tuple with one value?", "a": "(5,) with a comma."}]},

 {"id": "py-control", "track": "Python", "title": "Conditions and loops", "minutes": 40,
  "summary": "if chooses what to run. for repeats code for each value. Together they build totals, counts and labels.",
  "teaches": ["if", "loop-for", "range", "enumerate", "zip", "break", "while", "accumulator", "truthiness", "aug-assign"],
  "uses": ["list", "list-index", "len", "f-string", "arithmetic", "comparison", "round", "print", "variable", "sum-min-max"],
  "picture": {"svg": d_control(), "caption": "A loop visits each value. The if test decides which line runs."},
  "predict": {"q": "items = [10, 20, 30]. What do print(items[-1]) and print(len(items)) show?", "reveal": "30 and 3."},
  "explain": [
   {"h": "Conditions", "p": [
     "if runs a block only when the test is True.",
     "elif means 'else if'. else runs when no test was True.",
     "A colon ends the if line. The block under it is indented by 4 spaces.",
     "Combine tests with and, or and not.",
     "An empty list, an empty string, 0 and None count as False. This is called truthiness."]},
   {"h": "for loops", "p": [
     "for x in items: runs the block once for each value.",
     "range(n) gives 0 to n - 1. range(1, 4) gives 1, 2, 3.",
     "enumerate(items) gives the index and the value together.",
     "zip(a, b) walks two lists in step.",
     "break stops the loop. continue skips to the next value.",
     "while runs as long as its test is True. Make sure the test can become False."]},
   {"h": "The accumulator pattern", "p": [
     "Start a variable before the loop: total = 0.",
     "Change it inside the loop: total = total + amount.",
     "total += amount is a short way to write the same line.",
     "Use the result after the loop.",
     "This pattern builds totals, counts, the largest value and flags."]},
   {"h": "Common mistakes", "p": [
     "A missing colon gives SyntaxError. A wrong indent gives IndentationError.",
     "Set total = 0 before the loop. If you set it inside the loop, it resets on every pass.",
     "Use == in a test. Use = only to store a value.",
     "A while loop with a test that never turns False runs forever."]}],
  "example": {"title": "Totals, labels and a loop that stops", "code": (
      "amounts = [120, 40, 80, 200, 60]\ntotal = 0\nlarge = 0\nfor amount in amounts:\n    total = total + amount\n    if amount >= 100:\n        large = large + 1\n"
      "print(total, large, round(total / len(amounts), 1))\n\nfor i, amount in enumerate(amounts):\n    if amount >= 100:\n        label = \"large\"\n    elif amount >= 50:\n        label = \"medium\"\n    else:\n        label = \"small\"\n    print(i, amount, label)\n\n"
      "names = [\"Acme\", \"Birch\", \"Cobalt\"]\nfor name, amount in zip(names, amounts):\n    print(f\"{name}: {amount}\")\n\nfor amount in amounts:\n    if amount > 150:\n        print(\"first over 150:\", amount)\n        break\n\n"
      "print(bool([]), bool([0]), bool(\"\"), bool(None), bool(0))")},
  "qa": {"q": "What does this code print?\ncount = 0\nfor n in [5, 12, 7, 20, 3]:\n    if n > 6:\n        count = count + 1\nprint(count)",
         "a": "3. The values 12, 7 and 20 are above 6."},
  "build": {"task": "amounts = [120, 40, 80, 200, 60]. From a blank page print on one line: the total, the average to 1 decimal place, how many amounts are above the average, and the index of the largest amount.",
            "hint": "Loop once for the total. Loop again with enumerate for the count and the largest index.",
            "check": "You should see: 500 100.0 2 3."},
  "teach": "Explain in 5 sentences why total = 0 must come before the loop.",
  "mistakes": [],
  "selfCheck": [{"q": "What does range(1, 4) give?", "a": "1, 2, 3."}, {"q": "How does an empty list count in an if test?", "a": "As False."}]},

 {"id": "py-functions", "track": "Python", "title": "Functions", "minutes": 40,
  "summary": "A function packs code into a named tool. It takes inputs and returns an output.",
  "teaches": ["def", "return", "params-defaults", "scope", "lambda", "sort-key", "tuple-return", "docstring"],
  "uses": ["loop-for", "accumulator", "if", "list", "tuple", "unpack", "f-string", "round", "sorted", "sum-min-max", "list-methods", "print", "none", "arithmetic"],
  "picture": {"svg": d_function(), "caption": "Inputs go in. return sends one result out. Names made inside stay inside."},
  "predict": {"q": "total = 0. for n in [1, 2, 3]: total = total + n. What is total after the loop?", "reveal": "6. The loop adds 1, then 2, then 3."},
  "explain": [
   {"h": "What it is", "p": [
     "A function is a named block of code. You call it by name.",
     "def starts a function. The line ends with a colon. The body is indented.",
     "Parameters are the names in the brackets. Arguments are the values you pass in.",
     "return sends a value back to the caller. The function stops at return."]},
   {"h": "Calling a function", "p": [
     "A positional argument goes by position: total_price(3, 10).",
     "A keyword argument goes by name: total_price(3, 10, vat_rate=0).",
     "A default value is used when you give no argument: vat_rate=0.2.",
     "Put parameters with defaults after parameters without defaults.",
     "Use only numbers, text, True, False or None as defaults. A later lesson explains why."]},
   {"h": "Return values", "p": [
     "A function with no return gives back None.",
     "print shows a value. return gives it back. They are different.",
     "return a, b returns a tuple. Unpack it: low, high = min_max(values)."]},
   {"h": "Docstrings", "p": [
     "A docstring is a text in triple quotes on the first line inside a function.",
     "It says what the function does and what it returns. Keep it to one short line when you can.",
     "help(total_price) and your editor show the docstring. You can read it with total_price.__doc__.",
     "A good docstring says what and why. It does not repeat the code."]},
   {"h": "Scope", "p": [
     "A name made inside a function is local. It does not exist outside.",
     "Pass values in with parameters. Send values out with return.",
     "Avoid the global keyword. It makes code hard to follow."]},
   {"h": "lambda and sort keys", "p": [
     "A lambda is a small function in one line: lambda o: o[1].",
     "sorted(items, key=...) uses the key function to decide the order.",
     "Use a lambda only for short, simple rules. Use def for anything longer."]},
   {"h": "Common mistakes", "p": [
     "Forget return and the caller gets None.",
     "total_price without brackets is the function itself, not its result.",
     "Give each function one job and a clear verb name."]}],
  "example": {"title": "Parameters, return, scope and a sort key", "code": (
      "def total_price(qty, unit_price, vat_rate=0.2):\n    net = qty * unit_price\n    return net * (1 + vat_rate)\n\nprint(total_price(3, 10))\nprint(total_price(3, 10, vat_rate=0))\n\n"
      "def min_max(values):\n    return min(values), max(values)\n\nlow, high = min_max([4, 9, 2])\nprint(low, high)\n\ndef show_total(price):\n    total = price * 2\n\nprint(show_total(5))\n\n"
      "orders = [(\"Acme\", 120), (\"Birch\", 40), (\"Cobalt\", 200)]\nprint(sorted(orders, key=lambda o: o[1], reverse=True))")},
  "qa": {"q": "def add_vat(price):\n    price * 1.2\nWhat does print(add_vat(10)) show? How do you fix it?",
         "a": "None. The function works out 12.0 but does not return it. Write return price * 1.2."},
  "build": {"task": "From a blank page write band(amount) and summarise(amounts). band returns 'large' for 100 or more, 'medium' for 50 or more, and 'small' otherwise. summarise returns the count and the total of a list. Test band with 120, 60 and 10. Test summarise with [120, 40, 80].",
            "hint": "band needs if, elif and else with a return in each. summarise returns two values separated by a comma.",
            "check": "You should see: large medium small, then 3 240."},
  "teach": "Explain in 5 sentences the difference between print and return.",
  "mistakes": [],
  "selfCheck": [{"q": "What does a function without return give back?", "a": "None."}, {"q": "What does key=lambda o: o[1] do in sorted?", "a": "It sorts by the second value of each item."}]},

 {"id": "py-comprehensions", "track": "Python", "title": "List, dict and set comprehensions", "minutes": 35,
  "summary": "A comprehension builds a list, dict or set from a loop in one line.",
  "teaches": ["list-comp", "dict-comp", "set-comp", "conditional-expr", "set"],
  "uses": ["dict", "dict-items", "tally", "dict-get", "list", "loop-for", "if", "sorted", "sum-min-max", "round", "list-methods", "f-string", "print", "def", "return"],
  "picture": {"svg": d_comp(), "caption": "The loop and the comprehension do the same job. Each part has a place."},
  "predict": {"q": "squares = []. for n in [1, 2, 3]: squares.append(n * n). What is squares?", "reveal": "[1, 4, 9]. The loop adds 1 times 1, then 2 times 2, then 3 times 3."},
  "explain": [
   {"h": "What it is", "p": [
     "A list comprehension builds a list in one line: [expression for item in items].",
     "It does the same job as a for loop with append.",
     "Add if at the end to keep only some items: [x for x in items if test]."]},
   {"h": "How to read it", "p": [
     "Read it in this order: first for item in items, then if test, then the expression.",
     "The expression is what goes into the new list.",
     "Use a conditional expression to choose a value: 'large' if a >= 100 else 'small'."]},
   {"h": "Dict and set comprehensions", "p": [
     "A dict comprehension uses braces and a colon: {key: value for ...}.",
     "A set comprehension uses braces and no colon: {x for x in items}.",
     "A set keeps each value one time. Its order is not guaranteed."]},
   {"h": "With sum, min, max and sorted", "p": [
     "sum([a for a in amounts if a >= 100]) adds only the large amounts.",
     "sorted({c for c in customers}) gives the unique customers in order."]},
   {"h": "When not to use one", "p": [
     "Use a loop when the body is long or has several steps.",
     "Use a loop when you need side effects, such as printing or writing a file.",
     "One for and one if are easy to read. More than that is not."]},
   {"h": "Common mistakes", "p": [
     "The if goes at the end of the comprehension. It is easy to put it in the wrong place.",
     "A comprehension builds a new list. It does not change the old one."]}],
  "example": {"title": "Five comprehensions on one list of orders", "code": (
      "orders = [\n    {\"id\": 1, \"customer\": \"Acme\", \"amount\": 120},\n    {\"id\": 2, \"customer\": \"Birch\", \"amount\": 40},\n    {\"id\": 3, \"customer\": \"Acme\", \"amount\": 80},\n"
      "    {\"id\": 4, \"customer\": \"Cobalt\", \"amount\": 200},\n    {\"id\": 5, \"customer\": \"Birch\", \"amount\": 60},\n    {\"id\": 6, \"customer\": \"Acme\", \"amount\": 50},\n]\n"
      "amounts = [o[\"amount\"] for o in orders]\nlarge = [o[\"id\"] for o in orders if o[\"amount\"] >= 100]\nwith_vat = [round(a * 1.2, 2) for a in amounts]\n"
      "labels = [\"large\" if a >= 100 else \"small\" for a in amounts]\nby_id = {o[\"id\"]: o[\"amount\"] for o in orders}\ncustomers = sorted({o[\"customer\"] for o in orders})\n"
      "print(amounts)\nprint(large)\nprint(with_vat)\nprint(labels)\nprint(by_id)\nprint(customers)\nprint(sum([a for a in amounts if a >= 100]))")},
  "qa": {"q": "What does [n * n for n in range(1, 6) if n % 2 == 1] return? Why?",
         "a": "[1, 9, 25]. The loop visits 1 to 5. The if keeps the odd numbers 1, 3 and 5. The expression squares each one."},
  "build": {"task": "Use the list orders from the example. In two lines, with no for statement, build: a sorted list of the unique customers who have an order of 100 or more, and a dict that maps each order id to its amount for orders under 100.",
            "hint": "A set comprehension inside sorted(). A dict comprehension with an if at the end.",
            "check": "You should see ['Acme', 'Cobalt'] and {2: 40, 3: 80, 5: 60, 6: 50}."},
  "teach": "Explain in 4 sentences how you turn a for loop with append into a list comprehension.",
  "mistakes": [],
  "selfCheck": [{"q": "Where does the if go in a list comprehension?", "a": "At the end, after the for part."}, {"q": "Which brackets make a set comprehension?", "a": "Braces with no colon."}]},

 {"id": "py-files", "track": "Python", "title": "Files: text, CSV and JSON", "minutes": 45,
  "summary": "Open a file with with. Read CSV rows as dictionaries. Remember that CSV values arrive as text.",
  "teaches": ["file-open", "csv", "json", "stringio", "import"],
  "uses": ["dict", "dict-get", "tally", "loop-for", "list", "float", "convert-types", "str", "type-fn", "list-comp", "f-string", "print", "def", "return", "if"],
  "picture": {"svg": d_files(), "caption": "A CSV file is text. Convert the values before you do sums."},
  "predict": {"q": "row = {'id': '1', 'amount': '120'}. What does print(type(row['amount'])) show?", "reveal": "<class 'str'>. The amount is the text '120', not the number 120."},
  "explain": [
   {"h": "Text files", "p": [
     "open(path) gives a file object. Use it with with, so Python closes the file for you.",
     "Mode 'r' reads. Mode 'w' writes and replaces the file. Mode 'a' adds to the end.",
     "Add encoding='utf-8' so special characters read correctly.",
     "A loop over a file gives one line at a time. Each line ends with a newline. Use line.strip()."]},
   {"h": "Import", "p": [
     "import csv loads a module. A module is code that someone else wrote.",
     "Put imports at the top of the file. Use the module name: csv.DictReader.",
     "A later lesson explains imports in full."]},
   {"h": "CSV", "p": [
     "csv.DictReader gives each row as a dictionary. The first row of the file gives the keys.",
     "Open a CSV file with newline=''. This is a rule of the csv module.",
     "Every value from a CSV file is a str. Convert it: float(row['amount']).",
     "csv.DictWriter writes dictionaries. Call writeheader() first, then writerow() for each row."]},
   {"h": "JSON", "p": [
     "JSON stores nested data as text. Python lists and dicts match JSON arrays and objects.",
     "json.dumps(obj) makes text. json.loads(text) makes objects. json.dump and json.load work with files.",
     "JSON keys are always text. The int key 1 becomes '1'.",
     "JSON has no tuple. A tuple becomes a list."]},
   {"h": "Practice without a real file", "p": [
     "io.StringIO(text) makes a fake file from a string. Use it to test code before you have a file.",
     "For a real file, replace io.StringIO(raw) with open('orders.csv', newline='')."]},
   {"h": "Common mistakes", "p": [
     "Adding an int to a str raises TypeError. Convert CSV values first.",
     "Mode 'w' erases the old file. Check the file name first.",
     "On Windows, a path with backslashes needs a raw string, such as r'C:\\data\\x.csv', or forward slashes."]}],
  "example": {"title": "Read a CSV, total it, write CSV and JSON", "code": (
      "import csv\nimport io\nimport json\n\nraw = \"id,customer,amount\\n1,Acme,120\\n2,Birch,40\\n3,Acme,80\\n\"\nrows = list(csv.DictReader(io.StringIO(raw)))\nprint(rows[0])\nprint(type(rows[0][\"amount\"]))\n\n"
      "totals = {}\nfor row in rows:\n    customer = row[\"customer\"]\n    totals[customer] = totals.get(customer, 0) + float(row[\"amount\"])\nprint(totals)\n\n"
      "out = io.StringIO()\nwriter = csv.DictWriter(out, fieldnames=[\"customer\", \"total\"])\nwriter.writeheader()\nfor customer, total in totals.items():\n    writer.writerow({\"customer\": customer, \"total\": total})\nprint(out.getvalue().splitlines())\n\n"
      "text = json.dumps({\"totals\": totals}, indent=2)\nprint(text)\nprint(json.loads(text)[\"totals\"][\"Acme\"])")},
  "qa": {"q": "A row from DictReader is {'id': '1', 'amount': '120'}. You run total = 0 and then total = total + row['amount']. What happens? How do you fix it?",
         "a": "It raises TypeError: unsupported operand type(s) for +: 'int' and 'str'. The CSV value is text. Fix it: total = total + float(row['amount'])."},
  "build": {"task": "From a blank page: make a file orders.csv with the columns id, customer, amount and 4 rows. Write a script that reads it, totals the amount for each customer, and writes the totals to totals.json. Open totals.json and check it.",
            "hint": "Use open('orders.csv', newline='') with csv.DictReader. Use the tally pattern with float(). Use json.dump with indent=2.",
            "check": "totals.json shows each customer once, with the correct total."},
  "teach": "Explain in 5 sentences why a CSV amount of 120 is not the number 120 when you first read it.",
  "mistakes": [],
  "selfCheck": [{"q": "What type is every value from csv.DictReader?", "a": "str."}, {"q": "What does mode 'w' do to an old file?", "a": "It erases it and starts a new file."}]},

 {"id": "py-scripts", "track": "Python", "title": "Scripts, imports and virtual environments", "minutes": 40,
  "summary": "A script has a clear shape. Imports bring code in. A virtual environment keeps each project's packages apart.",
  "teaches": ["main-guard", "import-module", "argparse", "venv"],
  "uses": ["def", "return", "list-comp", "csv", "f-string", "if", "import", "try-except", "file-open", "float", "dict", "loop-for", "print"],
  "picture": {"svg": d_scripts(), "caption": "Each word on the command line has a job. Running a file is not the same as importing it."},
  "predict": {"q": "int('abc') runs. Which error does Python raise?", "reveal": "ValueError. The text 'abc' is not a valid whole number."},
  "explain": [
   {"h": "Script shape", "p": [
     "Put imports at the top, then functions, then a main() function.",
     "End the file with: if __name__ == '__main__': main().",
     "When you run python tool.py, __name__ is '__main__'. The code under the if runs.",
     "When another file imports tool, __name__ is 'tool'. The code under the if does not run.",
     "This lets you reuse the functions without running the whole script."]},
   {"h": "Imports", "p": [
     "import csv loads a module. Use csv.DictReader.",
     "from csv import DictReader loads one name. Use DictReader directly.",
     "Your own file helpers.py is a module. Keep it in the same folder and write import helpers.",
     "Do not name your file csv.py or json.py. It hides the standard module of the same name."]},
   {"h": "Command line arguments", "p": [
     "argparse reads the words you type after the script name.",
     "A positional argument is required: parser.add_argument('filename').",
     "An option starts with two dashes: --threshold. Give it a type and a default.",
     "parser.parse_args() returns an object. Read args.filename and args.threshold.",
     "To test, pass a list: parser.parse_args(['orders.csv', '--threshold', '100'])."]},
   {"h": "Virtual environments", "p": [
     "A virtual environment is a private folder of packages for one project.",
     "Create it: python -m venv .venv.",
     "Activate it on Windows: .venv\\Scripts\\activate. On Mac or Linux: source .venv/bin/activate.",
     "Install a package: pip install pandas. Save the list: pip freeze > requirements.txt.",
     "Rebuild it later: pip install -r requirements.txt."]},
   {"h": "Common mistakes", "p": [
     "Run the script from the folder that holds your data file, or give the full path.",
     "A package installed outside the virtual environment is not visible inside it."]}],
  "example": {"title": "A small command line tool", "code": (
      "import argparse\nimport csv\n\n\ndef load_rows(path):\n    with open(path, newline=\"\") as f:\n        return list(csv.DictReader(f))\n\n\ndef large_orders(rows, threshold):\n    return [r for r in rows if float(r[\"amount\"]) >= threshold]\n\n\n"
      "def main():\n    parser = argparse.ArgumentParser(description=\"List large orders\")\n    parser.add_argument(\"filename\")\n    parser.add_argument(\"--threshold\", type=float, default=100.0)\n    args = parser.parse_args()\n"
      "    rows = load_rows(args.filename)\n    for row in large_orders(rows, args.threshold):\n        print(f\"{row['id']:<4}{row['customer']:<8}{float(row['amount']):>8.2f}\")\n\n\nif __name__ == \"__main__\":\n    main()"),
              "script": {"name": "tool.py", "files": {"orders.csv": "id,customer,amount\n1,Acme,120\n2,Birch,40\n3,Acme,80\n4,Cobalt,200\n"},
                        "cmd": ["tool.py", "orders.csv", "--threshold", "100"], "show": "python tool.py orders.csv --threshold 100"}},
  "qa": {"q": "What is __name__ when you run python tool.py? What is it when another file runs import tool?",
         "a": "It is '__main__' when you run the file. It is 'tool' when another file imports it."},
  "build": {"task": "From a blank page: make a project folder and a virtual environment. Write tool.py so it reads orders.csv and prints the top N orders by amount. Add an option --top with the default 3. Run it with --top 2.",
            "hint": "Use sorted with key=lambda r: float(r['amount']) and reverse=True. Slice the result with [:args.top].",
            "check": "With the sample file from the example, --top 2 prints the 200 order and the 120 order."},
  "teach": "Explain in 5 sentences why the if __name__ line is useful.",
  "mistakes": [],
  "selfCheck": [{"q": "How do you create a virtual environment?", "a": "python -m venv .venv"}, {"q": "How do you read the --threshold option in code?", "a": "args.threshold, after args = parser.parse_args()."}]},
]


# ---------------------------------------------------------------- mixed tasks
ORDERS = '''orders = [
    {"id": 1, "customer": "Acme", "amount": 120.0},
    {"id": 2, "customer": "Birch", "amount": 40.0},
    {"id": 3, "customer": "Acme", "amount": 80.0},
    {"id": 4, "customer": "Cobalt", "amount": 200.0},
    {"id": 5, "customer": "Birch", "amount": 60.0},
    {"id": 6, "customer": "Acme", "amount": 50.0},
]'''

MIXED = {
 "py-types": [
  {"title": "A. Price a parcel", "setup": "",
   "task": "A parcel weighs 2.75 kg. The rate is 3.2 pounds for each kg. Print the cost. Then print the cost rounded to 2 decimal places.",
   "hint": "Store the weight and the rate in variables. Multiply them. Use round(value, 2).",
   "answer": "weight = 2.75\nrate = 3.2\ncost = weight * rate\nprint(cost)\nprint(round(cost, 2))"},
  {"title": "B. Boxes and leftovers", "setup": "",
   "task": "There are 47 items. A box holds 12 items. Print the number of full boxes. Then print the number of items left over.",
   "hint": "Use // for whole boxes. Use % for the remainder.",
   "answer": "items = 47\nper_box = 12\nprint(items // per_box)\nprint(items % per_box)"},
  {"title": "C. Fix a type error", "setup": "",
   "broken": 'qty = "3"\nprice = 2.5\nprint(qty * price)',
   "task": "This code fails. Say what the error is and why. Then fix it so it prints 7.5.",
   "hint": "qty holds text. Convert it with int() before you multiply.",
   "answer": 'qty = "3"\nprice = 2.5\nprint(int(qty) * price)'},
 ],
 "py-strings": [
  {"title": "A. A message with formats", "setup": "",
   "task": "customer is 'Acme', amount is 1234.5 and rate is 0.2. Print: Acme owes 1,234.50 (VAT 20.0%). Use one f-string.",
   "hint": "Format codes: :,.2f for money with commas and 2 decimal places, :.1% for a percentage.",
   "answer": 'customer = "Acme"\namount = 1234.5\nrate = 0.2\nprint(f"{customer} owes {amount:,.2f} (VAT {rate:.1%})")'},
  {"title": "B. Take an id apart", "setup": "",
   "task": "The id is 'ORD-1042-UK'. Print the prefix, the number as an int, and the country in lowercase.",
   "hint": "split('-') gives three parts. Use int() on the middle part and lower() on the last part.",
   "answer": 'order_id = "ORD-1042-UK"\nprefix, number, country = order_id.split("-")\nprint(prefix)\nprint(int(number))\nprint(country.lower())'},
  {"title": "C. Clean a name", "setup": "",
   "task": "The raw name is '  Birch & Co  '. Print it cleaned and in capitals. Then print True or False: does it contain the sign &?",
   "hint": "strip() then upper(). Use the word in for the test.",
   "answer": 'raw = "  Birch & Co  "\nclean = raw.strip().upper()\nprint(clean)\nprint("&" in clean)'},
 ],
 "py-lists-tuples": [
  {"title": "A. Remove and report", "setup": "orders = [120, 40, 80, 200]",
   "task": "Remove the last order from the list. Print the removed amount. Print the total of the orders that are left.",
   "hint": "pop() removes the last value and returns it.",
   "answer": "removed = orders.pop()\nprint(removed)\nprint(sum(orders))"},
  {"title": "B. Unpack a record", "setup": 'record = ("Acme", 3, 12.5)',
   "task": "Unpack the tuple into three names. Print one line in this form: Acme: 3 x 12.50 = 37.50.",
   "hint": "name, qty, price = record. Use an f-string with :.2f.",
   "answer": 'name, qty, price = record\nprint(f"{name}: {qty} x {price:.2f} = {qty * price:.2f}")'},
  {"title": "C. A backup that changes", "setup": "",
   "broken": "orders = [1, 2, 3]\nbackup = orders\norders.append(4)\nprint(backup)",
   "task": "The backup should still be [1, 2, 3]. Say what the code prints and why. Then fix it.",
   "hint": "b = a does not copy. Use .copy().",
   "answer": "orders = [1, 2, 3]\nbackup = orders.copy()\norders.append(4)\nprint(backup)\nprint(orders)"},
 ],
 "py-control": [
  {"title": "A. Count the bands", "setup": "amounts = [120, 40, 80, 200, 60, 50]",
   "task": "Count how many amounts are large (100 or more), medium (50 to 99) and small (under 50). Print the three counts on one line.",
   "hint": "Use three counters that start at 0. Use if, elif and else in one loop.",
   "answer": "large = 0\nmedium = 0\nsmall = 0\nfor amount in amounts:\n    if amount >= 100:\n        large += 1\n    elif amount >= 50:\n        medium += 1\n    else:\n        small += 1\nprint(large, medium, small)"},
  {"title": "B. Find the first match", "setup": "amounts = [120, 40, 80, 200, 60, 50]",
   "task": "Find the first amount over 150. Print its position (index) and its value. Stop the loop as soon as you find it.",
   "hint": "Use enumerate. Use break after the print.",
   "answer": "for i, amount in enumerate(amounts):\n    if amount > 150:\n        print(i, amount)\n        break"},
  {"title": "C. Walk two lists", "setup": 'customers = ["Acme", "Birch", "Cobalt"]\namounts = [120, 40, 200]',
   "task": "Print one line for each customer in this form: Acme owes 120.00. Use zip.",
   "hint": "for name, amount in zip(customers, amounts). Use an f-string with :.2f.",
   "answer": 'for name, amount in zip(customers, amounts):\n    print(f"{name} owes {amount:.2f}")'},
 ],
 "py-functions": [
  {"title": "A. Add VAT to a list", "setup": "",
   "task": "Write apply_vat(prices, rate). It returns a new list with each price multiplied by (1 + rate). Test it with [10, 20] and 0.2.",
   "hint": "Start with an empty list. Loop. Append. Return the list after the loop.",
   "answer": "def apply_vat(prices, rate):\n    result = []\n    for price in prices:\n        result.append(price * (1 + rate))\n    return result\n\nprint(apply_vat([10, 20], 0.2))"},
  {"title": "B. Shipping with defaults", "setup": "",
   "task": "Write shipping(weight, rate_per_kg=2.5, minimum=5.0). It returns the cost: weight times rate, but never less than the minimum. Test with weights 1 and 4, and then 4 with rate_per_kg=3.",
   "hint": "Use max(weight * rate_per_kg, minimum).",
   "answer": "def shipping(weight, rate_per_kg=2.5, minimum=5.0):\n    return max(weight * rate_per_kg, minimum)\n\nprint(shipping(1))\nprint(shipping(4))\nprint(shipping(4, rate_per_kg=3))"},
  {"title": "C. The two biggest orders", "setup": 'orders = [("Acme", 120), ("Birch", 40), ("Cobalt", 200), ("Delta", 80)]',
   "task": "Print the names of the two biggest orders, biggest first. Use sorted with a key.",
   "hint": "Sort by o[1] with reverse=True. Slice the first 2. Take o[0] from each.",
   "answer": "top = sorted(orders, key=lambda o: o[1], reverse=True)[:2]\nfor name, amount in top:\n    print(name)"},
  {"title": "D. A name that does not exist", "setup": "",
   "broken": "def total(price):\n    net = price * 2\n    return net\n\ntotal(5)\nprint(net)",
   "task": "This code stops with an error on the last line. Say what the error is and why. Then fix it so it prints 10.",
   "hint": "net only exists inside the function. Save the returned value in a variable.",
   "answer": "def total(price):\n    net = price * 2\n    return net\n\nresult = total(5)\nprint(result)"},
 ],
 "py-comprehensions": [
  {"title": "A. Filter a tally", "setup": ORDERS,
   "task": "Build the count of orders for each customer with a loop. Then make a new dict with a comprehension. It keeps only the customers with 2 or more orders.",
   "hint": "Loop first. Then {c: n for c, n in counts.items() if n >= 2}.",
   "answer": "counts = {}\nfor order in orders:\n    customer = order[\"customer\"]\n    counts[customer] = counts.get(customer, 0) + 1\nrepeat = {c: n for c, n in counts.items() if n >= 2}\nprint(repeat)"},
  {"title": "B. Loop to comprehension", "setup": ORDERS + "\n\nlabels = []\nfor order in orders:\n    if order[\"amount\"] >= 100:\n        labels.append(order[\"customer\"].upper())",
   "task": "The loop above builds a list of upper case customer names for the large orders. Print that list. Then rewrite the loop as one list comprehension and print it. The two lists must match.",
   "hint": "[expression for order in orders if test].",
   "answer": "print(labels)\nlabels2 = [o[\"customer\"].upper() for o in orders if o[\"amount\"] >= 100]\nprint(labels2)\nprint(labels == labels2)"},
  {"title": "C. Swap keys and values", "setup": 'prices = {"pen": 2.5, "ink": 10.0}',
   "task": "Make a new dict where the prices are the keys and the item names are the values.",
   "hint": "Use prices.items() and a dict comprehension.",
   "answer": "swapped = {v: k for k, v in prices.items()}\nprint(swapped)"},
 ],
 "py-files": [
  {"title": "A. Read, convert, filter", "setup": 'import csv\nimport io\n\nraw = "id,customer,amount\\n1,Acme,120\\n2,Birch,40\\n3,Acme,80\\n4,Cobalt,200\\n"',
   "task": "Read raw as a CSV. Make the amount a float in every row. Print the ids of the rows with an amount of 100 or more.",
   "hint": "Use csv.DictReader(io.StringIO(raw)). A list comprehension can build the new rows.",
   "answer": "rows = list(csv.DictReader(io.StringIO(raw)))\nrows = [{\"id\": r[\"id\"], \"amount\": float(r[\"amount\"])} for r in rows]\nprint([r[\"id\"] for r in rows if r[\"amount\"] >= 100])"},
  {"title": "B. Write a CSV", "setup": "import csv\nimport io\n\ntotals = {\"Acme\": 200.0, \"Birch\": 40.0}",
   "task": "Write totals as a CSV with the columns customer and total. Use a StringIO as the file. Print the lines.",
   "hint": "DictWriter, writeheader, then writerow for each pair. Use out.getvalue().splitlines().",
   "answer": "out = io.StringIO()\nwriter = csv.DictWriter(out, fieldnames=[\"customer\", \"total\"])\nwriter.writeheader()\nfor customer, total in totals.items():\n    writer.writerow({\"customer\": customer, \"total\": total})\nprint(out.getvalue().splitlines())"},
  {"title": "C. A JSON round trip", "setup": "import json\n\ndata = {1: \"a\", \"pair\": (1, 2)}",
   "task": "Turn data into JSON text. Print it. Turn the text back into Python and print the result. Say what changed.",
   "hint": "json.dumps then json.loads. Look at the key 1 and the tuple.",
   "answer": "text = json.dumps(data)\nprint(text)\nback = json.loads(text)\nprint(back)"},
 ],
 "py-scripts": [
  {"title": "A. Add an option", "setup": "import argparse",
   "task": "Build a parser with a positional filename and an option --vat (float, default 0.2). Test it with parse_args on the list ['orders.csv', '--vat', '0.1']. Print args.filename and args.vat.",
   "hint": "parser.add_argument('--vat', type=float, default=0.2). Pass the list to parse_args.",
   "answer": "parser = argparse.ArgumentParser()\nparser.add_argument(\"filename\")\nparser.add_argument(\"--vat\", type=float, default=0.2)\nargs = parser.parse_args([\"orders.csv\", \"--vat\", \"0.1\"])\nprint(args.filename, args.vat)"},
  {"title": "B. A yes or no flag", "setup": "import argparse",
   "task": "Add the flag --verbose that is False when you leave it out and True when you give it. Test both cases. Print each result.",
   "hint": "action='store_true'. Call parse_args twice, once with [] and once with ['--verbose'].",
   "answer": "parser = argparse.ArgumentParser()\nparser.add_argument(\"--verbose\", action=\"store_true\")\nprint(parser.parse_args([]).verbose)\nprint(parser.parse_args([\"--verbose\"]).verbose)"},
 ],
}

# Python tasks for the old lessons that stay in the course (changed to fit the new order)
LEGACY_MIXED = {
 "py-dict-count": [
  {"title": "A. Count, then sort", "setup": ORDERS,
   "task": "Count the orders for each customer. Print one line for each customer: the name and the count. Show the highest count first. If two counts are equal, sort by name.",
   "hint": "Build the tally first. Then sort counts.items() with a key. A key can return a tuple. Use a minus sign to sort a number from high to low.",
   "answer": "counts = {}\nfor order in orders:\n    customer = order[\"customer\"]\n    if customer in counts:\n        counts[customer] = counts[customer] + 1\n    else:\n        counts[customer] = 1\nfor name, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):\n    print(name, n)"},
  {"title": "B. Add up, not count", "setup": ORDERS,
   "task": "Find the total amount for each customer. Print the dictionary.",
   "hint": "The pattern is the same. Add the amount instead of 1. The method dict.get(key, 0) gives 0 when the key is missing.",
   "answer": "totals = {}\nfor order in orders:\n    customer = order[\"customer\"]\n    totals[customer] = totals.get(customer, 0) + order[\"amount\"]\nprint(totals)"},
  {"title": "C. Show only repeat customers", "setup": ORDERS,
   "task": "Build the count for each customer. Then print the name and count of each customer who has 2 or more orders. Use a loop and an if.",
   "hint": "Loop over counts.items(). Print only when n >= 2.",
   "answer": "counts = {}\nfor order in orders:\n    customer = order[\"customer\"]\n    counts[customer] = counts.get(customer, 0) + 1\nfor name, n in counts.items():\n    if n >= 2:\n        print(name, n)"},
 ],
 "py-mutable-default": [
  {"title": "A. Fix a shared list", "setup": "",
   "broken": "def add_order(order, orders=[]):\n    orders.append(order)\n    return orders\n\nprint(add_order(\"A\"))\nprint(add_order(\"B\"))",
   "task": "The code below should print ['A'] and then ['B']. Run it in your head. Say what it prints. Then rewrite add_order so it prints ['A'] and then ['B'].",
   "hint": "Use None as the default. Make the new list inside the function.",
   "answer": "def add_order(order, orders=None):\n    if orders is None:\n        orders = []\n    orders.append(order)\n    return orders\n\nprint(add_order(\"A\"))\nprint(add_order(\"B\"))"},
  {"title": "B. Fix a shared dictionary", "setup": "",
   "broken": "def tally(word, counts={}):\n    counts[word] = counts.get(word, 0) + 1\n    return counts\n\nprint(tally(\"a\"))\nprint(tally(\"b\"))",
   "task": "Each call should start with an empty tally. It should print {'a': 1} and then {'b': 1}. Say what the code below prints. Then fix it.",
   "hint": "The same rule applies to dictionaries. Use None. Make the new dict inside the function.",
   "answer": "def tally(word, counts=None):\n    if counts is None:\n        counts = {}\n    counts[word] = counts.get(word, 0) + 1\n    return counts\n\nprint(tally(\"a\"))\nprint(tally(\"b\"))"},
 ],
 "py-except-order": [
  {"title": "A. A custom error that is also a ValueError", "setup": "",
   "broken": "class NegativeAmountError(ValueError):\n    pass\n\ndef parse_amount(text):\n    value = float(text)\n    if value < 0:\n        raise NegativeAmountError(text)\n    return value\n\nfor text in [\"12.5\", \"abc\", \"-3\"]:\n    try:\n        print(parse_amount(text))\n    except ValueError:\n        print(\"not a number\")\n    except NegativeAmountError:\n        print(\"negative\")",
   "task": "Say what the code below prints for the three inputs. One result is wrong for the job. Fix the code so '-3' prints negative and 'abc' prints not a number.",
   "hint": "NegativeAmountError is a kind of ValueError. Which block must come first?",
   "answer": "class NegativeAmountError(ValueError):\n    pass\n\ndef parse_amount(text):\n    value = float(text)\n    if value < 0:\n        raise NegativeAmountError(text)\n    return value\n\nfor text in [\"12.5\", \"abc\", \"-3\"]:\n    try:\n        print(parse_amount(text))\n    except NegativeAmountError:\n        print(\"negative\")\n    except ValueError:\n        print(\"not a number\")"},
  {"title": "B. Read a file and skip bad rows", "setup": 'import csv\nimport io\n\nraw = "id,customer,amount\\n1,Acme,120\\n2,Birch,abc\\n3,Acme,80\\n4,Cobalt,\\n5,Birch,60\\n"',
   "task": "The text raw is a small CSV file. Read it with csv.DictReader. Add up the amount for each customer. If an amount is not a number, do not stop. Save the id of that row in a list. Print the totals, then the list of bad ids.",
   "hint": "Use io.StringIO(raw) in place of a file. Put float() inside try. The error to catch is ValueError. The id is a string.",
   "answer": "totals = {}\nbad = []\nfor row in csv.DictReader(io.StringIO(raw)):\n    try:\n        amount = float(row[\"amount\"])\n    except ValueError:\n        bad.append(row[\"id\"])\n        continue\n    customer = row[\"customer\"]\n    totals[customer] = totals.get(customer, 0) + amount\nprint(totals)\nprint(bad)"},
 ],
 "py-generators": [
  {"title": "A. A generator function in use", "setup": ORDERS,
   "task": "Write a generator function large_orders(orders, threshold). It yields each order with an amount at or above the threshold. Then print the sum of the amounts of orders of 100 or more.",
   "hint": "Use for, if and yield. Pass a generator expression to sum(): sum(o['amount'] for o in large_orders(orders, 100)).",
   "answer": "def large_orders(orders, threshold):\n    for order in orders:\n        if order[\"amount\"] >= threshold:\n            yield order\n\nprint(sum(o[\"amount\"] for o in large_orders(orders, 100)))"},
  {"title": "B. Used up twice", "setup": ORDERS,
   "broken": "amounts = (o[\"amount\"] for o in orders)\nprint(sum(amounts))\nprint(sum(amounts))",
   "task": "A new analyst wants the total and the average amount. Say what the code below prints. Then rewrite it so it prints the total, and then the average (total divided by count).",
   "hint": "Make a list once with square brackets. Then use sum() and len() on the list.",
   "answer": "amounts = [o[\"amount\"] for o in orders]\nprint(sum(amounts))\nprint(sum(amounts) / len(amounts))"},
 ],
}

# Claims in the text above that must be true. (code, expected stdout)
CHECKS = [
 ("x = 7 / 2\nprint(x, type(x).__name__, 6 / 3)", "3.5 float 2.0"),
 ('try:\n    age = "30"\n    print(age + 5)\nexcept TypeError as e:\n    print(e)', 'can only concatenate str (not "int") to str'),
 ("print('3' + '4')", "34"),
 ("code = 'uk-2024-q3'\nprint(code[3:7], code.upper())", "2024 UK-2024-Q3"),
 (" raw = ' ord-1042 '\nclean = raw.strip().upper()\nprint(clean)\nprint(int(clean.split('-')[1]) + 1)".strip(), "ORD-1042\n1043"),
 ("qty = 4\nunit_price = 12.5\nvat_rate = 0.2\nnet = qty * unit_price\nvat = net * vat_rate\ngross = net + vat\nprint(net)\nprint(vat)\nprint(round(gross, 2))\nprint(type(gross))", "50.0\n10.0\n60.0\n<class 'float'>"),
 ("code = 'ORD-1042'\nprint(code[0:3])", "ORD"),
 ("scores = [3, 1, 2]\nresult = scores.sort()\nprint(result)", "None"),
 ("prices = [12.5, 8.0, 20.0, 5.5]\nprint(min(prices))\nprint(max(prices))\nprint(sum(prices))\nprint(sorted(prices, reverse=True)[:2])\nprint(prices)", "5.5\n20.0\n46.0\n[20.0, 12.5]\n[12.5, 8.0, 20.0, 5.5]"),
 ("items = [10, 20, 30]\nprint(items[-1])\nprint(len(items))", "30\n3"),
 ("count = 0\nfor n in [5, 12, 7, 20, 3]:\n    if n > 6:\n        count = count + 1\nprint(count)", "3"),
 ("amounts = [120, 40, 80, 200, 60]\ntotal = 0\nfor amount in amounts:\n    total = total + amount\naverage = total / len(amounts)\nabove = 0\nbest_index = 0\nfor i, amount in enumerate(amounts):\n    if amount > average:\n        above = above + 1\n    if amount > amounts[best_index]:\n        best_index = i\nprint(total, round(average, 1), above, best_index)", "500 100.0 2 3"),
 ("total = 0\nfor n in [1, 2, 3]:\n    total = total + n\nprint(total)", "6"),
 ("def add_vat(price):\n    price * 1.2\nprint(add_vat(10))", "None"),
 ("def band(amount):\n    if amount >= 100:\n        return 'large'\n    elif amount >= 50:\n        return 'medium'\n    else:\n        return 'small'\ndef summarise(amounts):\n    return len(amounts), sum(amounts)\nprint(band(120), band(60), band(10))\ncount, total = summarise([120, 40, 80])\nprint(count, total)", "large medium small\n3 240"),
 ("squares = []\nfor n in [1, 2, 3]:\n    squares.append(n * n)\nprint(squares)", "[1, 4, 9]"),
 ("print([n * n for n in range(1, 6) if n % 2 == 1])", "[1, 9, 25]"),
 ("row = {'id': '1', 'amount': '120'}\nprint(type(row['amount']))", "<class 'str'>"),
 ("row = {'id': '1', 'amount': '120'}\ntry:\n    total = 0\n    total = total + row['amount']\nexcept TypeError as e:\n    print(e)", "unsupported operand type(s) for +: 'int' and 'str'"),
 ("try:\n    int('abc')\nexcept Exception as e:\n    print(type(e).__name__)", "ValueError"),
 ("orders = [\n    {'id': 1, 'customer': 'Acme', 'amount': 120}, {'id': 2, 'customer': 'Birch', 'amount': 40},\n    {'id': 3, 'customer': 'Acme', 'amount': 80}, {'id': 4, 'customer': 'Cobalt', 'amount': 200},\n    {'id': 5, 'customer': 'Birch', 'amount': 60}, {'id': 6, 'customer': 'Acme', 'amount': 50}]\nprint(sorted({o['customer'] for o in orders if o['amount'] >= 100}))\nprint({o['id']: o['amount'] for o in orders if o['amount'] < 100})", "['Acme', 'Cobalt']\n{2: 40, 3: 80, 5: 60, 6: 50}"),
 ("print(__name__)", "__main__"),
]
