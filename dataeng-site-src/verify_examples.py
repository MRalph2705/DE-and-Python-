"""Run every worked example used on the topic pages and assert the stated outputs."""
import duckdb

# ---------- Python examples ----------
# P1 dict counting
def count_by_status(orders):
    counts = {}
    for order in orders:
        status = order["status"]
        if status in counts:
            counts[status] = counts[status] + 1
        else:
            counts[status] = 1
    return counts

orders = [{"id": 1, "status": "shipped"}, {"id": 2, "status": "pending"}, {"id": 3, "status": "shipped"}]
assert count_by_status(orders) == {"shipped": 2, "pending": 1}
# the wrong version: checks the row instead of the tally
def wrong_count(orders):
    counts = {}
    for order in orders:
        s = order["status"]
        if s in order:
            counts[s] = counts[s] + 1
        else:
            counts[s] = 1
    return counts
assert wrong_count(orders) == {"shipped": 1, "pending": 1}

# P2 mutable default
def add_item(item, cart=[]):
    cart.append(item)
    return cart
a = add_item("Laptop")
b = add_item("Mouse")
assert b == ["Laptop", "Mouse"] and a is b
def add_item_fixed(item, cart=None):
    if cart is None:
        cart = []
    cart.append(item)
    return cart
assert add_item_fixed("Laptop") == ["Laptop"] and add_item_fixed("Mouse") == ["Mouse"]

# P3 generators
prices = [10, 25, 8, 40]
gen = (p * 0.9 for p in prices)
assert str(gen).startswith("<generator object")
assert list(gen) == [9.0, 22.5, 7.2, 36.0]
assert list(gen) == []
lst = [p * 0.9 for p in prices]
assert list(lst) == [9.0, 22.5, 7.2, 36.0] and list(lst) == [9.0, 22.5, 7.2, 36.0]

# P4 except order
class InsufficientFundsError(Exception):
    pass
out = None
try:
    raise InsufficientFundsError("low")
except Exception:
    out = "general"
except InsufficientFundsError:
    out = "specific"
assert out == "general"
out = None
try:
    raise InsufficientFundsError("low")
except InsufficientFundsError:
    out = "specific"
except Exception:
    out = "general"
assert out == "specific"

# P5 property / repr
class Order:
    def __init__(self, customer, qty, unit_price):
        self.customer = customer
        self.qty = qty
        self.unit_price = unit_price
    @property
    def total(self):
        return self.qty * self.unit_price
    def __repr__(self):
        return f"Order({self.customer!r}, total={self.total})"
o = Order("Acme", 3, 10)
assert o.total == 30
assert repr(o) == "Order('Acme', total=30)"
try:
    o.total()
    raise SystemExit("expected TypeError")
except TypeError as e:
    assert "'int' object is not callable" in str(e)
class BadRepr:
    def __repr__(self):
        f"x"
try:
    repr(BadRepr())
    raise SystemExit("expected TypeError")
except TypeError as e:
    assert "__repr__ returned non-string" in str(e)

# ---------- SQL examples (DuckDB used only to check the numbers; syntax noted per page) ----------
con = duckdb.connect()

# S1 WHERE vs HAVING
con.execute("CREATE TABLE Visits(VisitID INT, Ward VARCHAR, WaitMins INT)")
con.execute("INSERT INTO Visits VALUES (1,'A',10),(2,'A',50),(3,'B',20),(4,'B',20),(5,'C',90),(6,'C',70)")
r = con.execute("""SELECT Ward, AVG(WaitMins) AS AvgWait FROM Visits WHERE WaitMins > 15
                   GROUP BY Ward HAVING AVG(WaitMins) > 30 ORDER BY Ward""").fetchall()
assert r == [("A", 50.0), ("C", 80.0)], r

# S2 frames, ward A waits 10,50,30,70
con.execute("CREATE TABLE W(VisitID INT, Ward VARCHAR, WaitMins INT)")
con.execute("INSERT INTO W VALUES (1,'A',10),(2,'A',50),(3,'A',30),(4,'A',70)")
r = con.execute("""SELECT VisitID,
        AVG(WaitMins) OVER (PARTITION BY Ward ORDER BY VisitID ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS Moving3,
        LAST_VALUE(WaitMins) OVER (PARTITION BY Ward ORDER BY VisitID) AS LastDefault,
        LAST_VALUE(WaitMins) OVER (PARTITION BY Ward ORDER BY VisitID
             ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS LastFull
      FROM W ORDER BY VisitID""").fetchall()
assert r == [(1, 10.0, 10, 70), (2, 30.0, 50, 70), (3, 30.0, 30, 70), (4, 50.0, 70, 70)], r

# S3 percentiles on 10,20,30,40
con.execute("CREATE TABLE P(x INT)")
con.execute("INSERT INTO P VALUES (10),(20),(30),(40)")
r = con.execute("""SELECT quantile_cont(x,0.5), quantile_disc(x,0.5), quantile_cont(x,0.75), quantile_disc(x,0.75),
                   quantile_cont(x,0.25), quantile_disc(x,0.25) FROM P""").fetchall()[0]
assert r == (25.0, 20, 32.5, 30, 17.5, 10), r

# S4 ROLLUP + GROUPING, includes a real NULL ward
con.execute("CREATE TABLE R(Yr INT, Ward VARCHAR, Mins INT)")
con.execute("INSERT INTO R VALUES (2024,'A',100),(2024,'B',200),(2025,'A',300),(2025,NULL,50)")
r = con.execute("""SELECT Yr, Ward, SUM(Mins) AS Total, GROUPING(Ward) AS IsWardSubtotal
                   FROM R GROUP BY ROLLUP (Yr, Ward) ORDER BY Yr NULLS LAST, Ward NULLS LAST""").fetchall()
expected = [
    (2024, "A", 100, 0), (2024, "B", 200, 0), (2024, None, 300, 1),
    (2025, "A", 300, 0), (2025, None, 50, 0), (2025, None, 350, 1),
    (None, None, 650, 1),
]
assert sorted(r, key=lambda t: (t[0] is None, t[0] or 0, t[3], t[1] or "")) == sorted(
    expected, key=lambda t: (t[0] is None, t[0] or 0, t[3], t[1] or "")), r

# S5 correlated subquery vs window: average of all PRIOR visits in same ward
con.execute("CREATE TABLE V(VisitID INT, Ward VARCHAR, WaitMins INT)")
con.execute("INSERT INTO V VALUES (1,'A',10),(2,'B',40),(3,'A',30),(4,'A',50),(5,'B',20)")
a = con.execute("""SELECT VisitID, (SELECT AVG(v2.WaitMins) FROM V v2
                    WHERE v2.Ward = v.Ward AND v2.VisitID < v.VisitID) AS AvgPrior
                   FROM V v ORDER BY VisitID""").fetchall()
b = con.execute("""SELECT VisitID, AVG(WaitMins) OVER (PARTITION BY Ward ORDER BY VisitID
                    ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS AvgPrior
                   FROM V ORDER BY VisitID""").fetchall()
assert a == b == [(1, None), (2, None), (3, 10.0), (4, 20.0), (5, 40.0)], (a, b)

print("ALL EXAMPLES VERIFIED")

# ---------- extra checks for build tasks and exact error messages ----------
class BadRepr2:
    def __repr__(self):
        f"x"
try:
    print(BadRepr2())
    raise SystemExit("expected TypeError")
except TypeError as e:
    PRINT_MSG = str(e)
print("print(obj) with a return-less __repr__ gives:", PRINT_MSG)

try:
    int("abc")
except Exception:
    first = "A"
except ValueError:
    first = "B"
assert first == "A"

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
print("Invoice total:", inv.total, repr(inv))
assert inv.total == 300.0

def safe_ratio(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
    except TypeError:
        return "Numbers only"
    except Exception:
        return "Unexpected"
assert safe_ratio(1, 0) == "Cannot divide by zero"
assert safe_ratio("a", 2) == "Numbers only"
assert safe_ratio(1, 2) == 0.5

def prices_with_vat(prices, rate=0.2):
    for p in prices:
        yield p * (1 + rate)
g = prices_with_vat([10, 25])
assert list(g) == [12.0, 30.0] and list(g) == []

# S1 build task
r = con.execute("""SELECT Ward, COUNT(*) AS Visits, AVG(WaitMins) AS AvgWait FROM Visits
                   WHERE WaitMins > 10 GROUP BY Ward HAVING COUNT(*) >= 2 AND AVG(WaitMins) > 25""").fetchall()
assert r == [("C", 2, 80.0)], r

# S3 build task: per-ward median CONT vs DISC
r = con.execute("""SELECT Ward, quantile_disc(WaitMins,0.5), quantile_cont(WaitMins,0.5)
                   FROM Visits GROUP BY Ward ORDER BY Ward""").fetchall()
assert r == [("A", 10, 30.0), ("B", 20, 20.0), ("C", 70, 80.0)], r

# S4 labels
r = con.execute("""SELECT Yr,
        CASE WHEN GROUPING(Ward)=1 THEN 'All wards' ELSE COALESCE(Ward,'Unknown') END AS WardLabel,
        SUM(Mins) AS Total
      FROM R GROUP BY ROLLUP (Yr, Ward)""").fetchall()
got = sorted(r, key=lambda t: (t[0] is None, t[0] or 0, t[1], t[2]))
exp = sorted([(2024,'A',100),(2024,'B',200),(2024,'All wards',300),
              (2025,'A',300),(2025,'Unknown',50),(2025,'All wards',350),
              (None,'All wards',650)], key=lambda t: (t[0] is None, t[0] or 0, t[1], t[2]))
assert got == exp, got

# S5 qa + build
a = con.execute("""SELECT VisitID, (SELECT MAX(v2.WaitMins) FROM V v2 WHERE v2.Ward=v.Ward AND v2.VisitID<v.VisitID) FROM V v ORDER BY VisitID""").fetchall()
b = con.execute("""SELECT VisitID, MAX(WaitMins) OVER (PARTITION BY Ward ORDER BY VisitID ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) FROM V ORDER BY VisitID""").fetchall()
assert a == b == [(1,None),(2,None),(3,10),(4,30),(5,40)], (a, b)
c = con.execute("""SELECT VisitID, (SELECT COUNT(*) FROM V v2 WHERE v2.Ward=v.Ward AND v2.VisitID<v.VisitID) FROM V v ORDER BY VisitID""").fetchall()
d = con.execute("""SELECT VisitID, COUNT(*) OVER (PARTITION BY Ward ORDER BY VisitID ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) FROM V ORDER BY VisitID""").fetchall()
assert c == d == [(1,0),(2,0),(3,1),(4,2),(5,1)], (c, d)
print("EXTRA CHECKS VERIFIED")
