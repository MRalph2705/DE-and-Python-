"""Mixed practice tasks. Every answer query is RUN in DuckDB and its output is captured,
so the expected output on the site comes from a real run. Answers use portable SQL
(CASE, COALESCE, CAST) so they also work in T-SQL."""
import duckdb

TABLES = {
 "E": (["Yr", "Ward", "Triage", "Mins"], "Yr INT, Ward VARCHAR, Triage INT, Mins INT",
       [(2024,"A",1,10),(2024,"A",2,20),(2024,"B",1,30),(2024,"B",2,40),
        (2025,"A",1,50),(2025,"A",2,60),(2025,"B",1,70),(2025,None,2,80)]),
 "V2": (["VisitID","Ward","Triage","WaitMins"], "VisitID INT, Ward VARCHAR, Triage INT, WaitMins INT",
        [(1,"A",1,10),(2,"A",2,50),(3,"A",2,60),(4,"B",1,20),(5,"B",2,20),(6,"C",1,90),(7,"C",2,70),(8,"C",2,40)]),
 "F": (["VisitID","Ward","WaitMins"], "VisitID INT, Ward VARCHAR, WaitMins INT",
       [(1,"A",10),(2,"A",50),(3,"A",30),(4,"A",70),(5,"B",20),(6,"B",40),(7,"B",20)]),
}

LABELS = ("CASE WHEN GROUPING(Yr) = 1 THEN 'All years' ELSE CAST(Yr AS VARCHAR) END AS YearLabel,\n"
          "       CASE WHEN GROUPING(Ward) = 1 THEN 'All wards' ELSE COALESCE(Ward, 'Unknown') END AS WardLabel")
ORD = "ORDER BY GROUPING(Yr), Yr, GROUPING(Ward), COALESCE(Ward, 'Unknown')"

TASKS = {
 "sql-rollup-grouping": [
  {"table": "E", "title": "A. Subtotals with clear labels",
   "task": "Show the total Mins for each year and ward. Add a subtotal for each year and one grand total. Label subtotal rows 'All wards' and 'All years'. Label a real NULL ward 'Unknown'. Sort so each subtotal sits under its year and the grand total is last.",
   "hint": "Use ROLLUP (Yr, Ward). Use GROUPING(Ward) and GROUPING(Yr) inside CASE. Sort with GROUPING() first.",
   "sql": f"SELECT {LABELS},\n       SUM(Mins) AS Total\nFROM E\nGROUP BY ROLLUP (Yr, Ward)\n{ORD};"},
  {"table": "E", "title": "B. Keep only big totals",
   "task": "Use the query from task A. Keep only the rows where the total is more than 100.",
   "hint": "A filter on SUM() goes in HAVING. HAVING runs after GROUP BY and ROLLUP.",
   "sql": f"SELECT {LABELS},\n       SUM(Mins) AS Total\nFROM E\nGROUP BY ROLLUP (Yr, Ward)\nHAVING SUM(Mins) > 100\n{ORD};"},
  {"table": "E", "title": "C. Subtotals only",
   "task": "Show only the subtotal rows and the grand total. Do not show the detail rows.",
   "hint": "A detail row has GROUPING(Ward) = 0. A subtotal and the grand total have GROUPING(Ward) = 1.",
   "sql": f"SELECT {LABELS},\n       SUM(Mins) AS Total\nFROM E\nGROUP BY ROLLUP (Yr, Ward)\nHAVING GROUPING(Ward) = 1\n{ORD};"},
  {"table": "E", "title": "D. Percent of the grand total",
   "task": "Show each row of task A with a column PctOfAll. PctOfAll is the row total divided by the grand total, times 100, rounded to 1 decimal place.",
   "hint": "Put the ROLLUP query in a CTE and keep GROUPING(Yr) and GROUPING(Ward) as columns. The grand total row has both equal to 1. Read it with a subquery.",
   "sql": ("WITH r AS (\n    SELECT GROUPING(Yr) AS gy, GROUPING(Ward) AS gw, Yr, Ward, SUM(Mins) AS Total\n"
           "    FROM E\n    GROUP BY ROLLUP (Yr, Ward)\n)\n"
           "SELECT CASE WHEN gy = 1 THEN 'All years' ELSE CAST(Yr AS VARCHAR) END AS YearLabel,\n"
           "       CASE WHEN gw = 1 THEN 'All wards' ELSE COALESCE(Ward, 'Unknown') END AS WardLabel,\n"
           "       Total,\n       ROUND(Total * 100.0 / (SELECT Total FROM r WHERE gy = 1 AND gw = 1), 1) AS PctOfAll\n"
           "FROM r\nORDER BY gy, Yr, gw, COALESCE(Ward, 'Unknown');")},
 ],
 "sql-where-having": [
  {"table": "V2", "title": "A. Filter rows and groups together",
   "task": "Ignore visits of 10 minutes or less. For each ward show the number of visits and the average wait, rounded to 1 decimal place. Keep wards with at least 2 visits and an average above 30. Show the highest average first.",
   "hint": "Row filter in WHERE. Both group filters in HAVING. Multiply by 1.0 so the average keeps its decimals.",
   "sql": "SELECT Ward, COUNT(*) AS Visits, ROUND(AVG(WaitMins * 1.0), 1) AS AvgWait\nFROM V2\nWHERE WaitMins > 10\nGROUP BY Ward\nHAVING COUNT(*) >= 2 AND AVG(WaitMins * 1.0) > 30\nORDER BY AvgWait DESC;"},
  {"table": "V2", "title": "B. Compare each group to the whole table",
   "task": "Show the wards whose average wait is above the average wait of all visits. Show the ward and its average, rounded to 1 decimal place.",
   "hint": "A CTE gives one row per ward. A subquery in WHERE gives the overall average.",
   "sql": "WITH w AS (\n    SELECT Ward, AVG(WaitMins * 1.0) AS AvgWait\n    FROM V2\n    GROUP BY Ward\n)\nSELECT Ward, ROUND(AvgWait, 1) AS AvgWait\nFROM w\nWHERE AvgWait > (SELECT AVG(WaitMins * 1.0) FROM V2)\nORDER BY Ward;"},
 ],
 "sql-window-frames": [
  {"table": "F", "title": "A. Running total and change",
   "task": "For each visit show the running total of waits in its ward, and the change from the previous visit in the same ward. The first visit in a ward has no change.",
   "hint": "SUM() with a frame that ends at CURRENT ROW. LAG() for the previous row. Both use PARTITION BY Ward ORDER BY VisitID.",
   "sql": "SELECT VisitID, Ward, WaitMins,\n       SUM(WaitMins) OVER (PARTITION BY Ward ORDER BY VisitID\n           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS RunningTotal,\n       WaitMins - LAG(WaitMins) OVER (PARTITION BY Ward ORDER BY VisitID) AS ChangeFromPrev\nFROM F\nORDER BY VisitID;"},
  {"table": "F", "title": "B. Filter on a window result",
   "task": "Show only the visits whose wait is above the average of the visit itself and the 2 visits before it, in the same ward. Show the moving average, rounded to 1 decimal place.",
   "hint": "WHERE cannot see a window alias. Put the window query in a CTE, then filter in the outer query.",
   "sql": "WITH m AS (\n    SELECT VisitID, Ward, WaitMins,\n           AVG(WaitMins * 1.0) OVER (PARTITION BY Ward ORDER BY VisitID\n               ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS Moving3\n    FROM F\n)\nSELECT VisitID, Ward, WaitMins, ROUND(Moving3, 1) AS Moving3\nFROM m\nWHERE WaitMins > Moving3\nORDER BY VisitID;"},
 ],
}

def fmt(v):
    if v is None: return "NULL"
    if isinstance(v, float): return f"{v:.1f}"
    return str(v)

def table_text(name):
    cols, _, rows = TABLES[name]
    return " | ".join(cols) + "\n" + "\n".join(" | ".join(fmt(c) for c in r) for r in rows)

def run_all():
    con = duckdb.connect()
    for name, (cols, ddl, rows) in TABLES.items():
        con.execute(f"CREATE TABLE {name}({ddl})")
        con.executemany(f"INSERT INTO {name} VALUES ({','.join('?'*len(cols))})", rows)
    out = {}
    for tid, tasks in TASKS.items():
        res = []
        for t in tasks:
            cur = con.execute(t["sql"]); head = [d[0] for d in cur.description]; rows = cur.fetchall()
            text = " | ".join(head) + "\n" + "\n".join(" | ".join(fmt(c) for c in r) for r in rows)
            res.append({"title": t["title"], "task": t["task"], "hint": t["hint"], "table": t["table"],
                        "tableData": table_text(t["table"]), "sql": t["sql"], "output": text, "rowCount": len(rows)})
        out[tid] = res
    return out

if __name__ == "__main__":
    for tid, ts in run_all().items():
        for t in ts:
            print("=====", tid, t["title"], t["rowCount"], "rows"); print(t["output"])
