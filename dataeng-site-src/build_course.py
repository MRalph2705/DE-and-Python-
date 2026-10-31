"""Assemble the course: syllabus, lessons, run-checked examples, concept check.

Usage: python3 build_course.py <site_dir>
Writes <site_dir>/data/topics.js  (window.SITE, window.SYLLABUS, window.TOPICS)

Rules enforced here:
  1. Every lesson lists the ideas it TEACHES and USES.
  2. A built lesson may only use ideas taught earlier (or the declared SQL baseline).
     Otherwise the lesson is held back (status 'waiting') and the build says why.
  3. Every code example and mixed task is executed. Outputs on the site are real outputs.
  4. Every claim in CHECKS is executed and compared.
"""
import copy, json, os, subprocess, sys, tempfile
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_topics as bt          # noqa: E402  legacy lessons + diagram helpers
import lessons_m1 as m1            # noqa: E402
import lessons_m2 as m2a           # noqa: E402
import lessons_m2b as m2b          # noqa: E402
import examples_pro as ep          # noqa: E402  senior-style worked examples
import mixed_tasks as mt           # noqa: E402  SQL mixed tasks
import py_mixed as pm              # noqa: E402  python task runner

import re

_plain_run = pm.run
HARNESS = (
    "import sys, io, contextlib\n"
    "code = open(sys.argv[1]).read()\n"
    "buf = io.StringIO()\n"
    "try:\n"
    "    exec(compile(code, '<lesson>', 'exec'), {'__name__': '__main__'})\n"
    "except Exception as e:\n"
    "    print(f'{type(e).__name__}: {e}')\n"
)


def run_isolated(code):
    """Run in a fresh Python, stdout and stderr together. Used for logging code (global state)."""
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "h.py"), "w").write(HARNESS)
        open(os.path.join(d, "c.py"), "w").write(code)
        r = subprocess.run([sys.executable, "-I", "h.py", "c.py"], cwd=d, capture_output=True, text=True)
        return (r.stdout + r.stderr).rstrip("\n")


def smart_run(code):
    return run_isolated(code) if re.search(r"\blogging\b", code) else _plain_run(code)


pm.run = smart_run

SOURCES = {
    "B": "Data with Baraa (SQL Server). Read: his 12-chapter SQL roadmap and the project READMEs. Not watched.",
    "Z": "DataTalks.Club Data Engineering Zoomcamp (Alexey Grigorev). Read: the course page and module list.",
    "D": "Microsoft DP-700 Fabric Data Engineer. Read: the official skills-measured list.",
    "O": "Claude's own knowledge. Lessons are written here. They are not copies of any course.",
}

# SQL ideas assumed from your earlier SQL days. Shown on each SQL lesson. Tell Claude if any is new.
ASSUMED = {
    "sql-select": ("SELECT, WHERE, ORDER BY", "sql-select"),
    "sql-groupby": ("GROUP BY with aggregates such as SUM and AVG", "sql-aggregates"),
    "sql-join": ("JOINs", "sql-joins"),
    "sql-cte": ("CTEs (WITH ... AS)", "sql-ctes"),
    "sql-window-basic": ("OVER, PARTITION BY and ranking functions such as RANK and LAG", "sql-window-ranking"),
    "sql-case": ("CASE WHEN", "sql-row-functions"),
    "sql-coalesce-cast": ("COALESCE, ISNULL and CAST", "sql-row-functions"),
    "sql-scalar-subquery": ("a subquery inside SELECT or WHERE", "sql-subqueries"),
}


def L(id, title, src, tags=None):
    return {"id": id, "title": title, "src": src}


MODULES = [
    {"id": "M1", "title": "Python core for data work", "basis": "O. Meets the Zoomcamp prerequisite 'basic coding'. Every lesson is written to be typed from a blank page.",
     "lessons": ["py-types", "py-strings", "py-lists-tuples", "py-control", "py-functions", "py-dict-count", "py-comprehensions", "py-mutable-default", "py-files", "py-except-order", "py-scripts"]},
    {"id": "M2", "title": "Python for engineers", "basis": "O.",
     "lessons": ["py-generators", L("py-classes", "Classes: objects, attributes and methods", "O"), "py-class-property", L("py-dataclasses", "Dataclasses", "O"),
                 L("py-decorators", "Decorators and closures", "O"), L("py-typing", "Type hints", "O"), L("py-logging", "Logging", "O"),
                 L("py-pytest", "Testing with pytest", "O"), L("py-datetime", "Dates, times and time zones", "O")]},
    {"id": "M3", "title": "T-SQL queries on SQL Server", "basis": "B (roadmap chapters 1 to 8) plus O.",
     "lessons": [L("sql-setup", "Set up SQL Server Express and SSMS", "B ch.1"), L("sql-select", "SELECT, WHERE, ORDER BY and TOP", "B ch.2, 5"),
                 L("sql-ddl-dml", "CREATE, ALTER, DROP, INSERT, UPDATE and DELETE", "B ch.3, 4"), L("sql-joins", "Joins", "B ch.6"),
                 L("sql-set-ops", "UNION, EXCEPT and INTERSECT", "B ch.6"), L("sql-row-functions", "String, date, NULL, CASE and CAST functions", "B ch.7"),
                 L("sql-aggregates", "Aggregates and GROUP BY", "B ch.8"), "sql-where-having",
                 L("sql-window-ranking", "Ranking and value window functions", "B ch.8"), "sql-window-frames", "sql-percentile", "sql-rollup-grouping"]},
    {"id": "M4", "title": "Advanced T-SQL and performance", "basis": "B (roadmap chapters 9 and 10) plus O.",
     "lessons": [L("sql-subqueries", "Subqueries", "B ch.9"), L("sql-ctes", "CTEs and recursive CTEs", "B ch.9"), L("sql-views-temp", "Views, temp tables and table variables", "B ch.9"),
                 "sql-correlated-vs-window", L("sql-stored-procs", "Stored procedures and triggers", "B ch.9"), L("sql-indexes", "Indexes: clustered, nonclustered, covering", "B ch.10"),
                 L("sql-exec-plans", "Execution plans and STATISTICS IO and TIME", "B ch.10, O"), L("sql-sargable", "Writing queries an index can use", "O"),
                 L("sql-partitions", "Partitioning", "B ch.10"), L("sql-transactions", "Transactions, locks and isolation", "O"), L("sql-plan-cache", "Parameter sniffing and the plan cache", "O")]},
    {"id": "M5", "title": "Build a data warehouse in SQL Server", "basis": "B (the SQL Data Warehouse project: bronze, silver, gold; and the analytics project) plus O, D (loading patterns).",
     "lessons": [L("dw-architecture", "OLTP and OLAP, layers and the medallion design", "B"), L("dw-setup", "Project setup, naming rules and Git", "B"),
                 L("dw-bronze", "Bronze: load raw files with BULK INSERT", "B"), L("dw-silver", "Silver: clean and standardise", "B"), L("dw-gold", "Gold: dimensions, facts and a star schema", "B"),
                 L("dw-quality", "Data quality checks", "B, D"), L("dw-docs", "Data model docs and a data catalogue", "B"),
                 L("dw-analysis", "Explore and analyse: the six stages", "B"), L("dw-incremental", "Full and incremental loads, late data", "D, O")]},
    {"id": "M6", "title": "Python and SQL Server together", "basis": "O. No course found covers this. Portfolio project 2.",
     "lessons": [L("pysql-connect", "Connect with pyodbc", "O"), L("pysql-params", "Parameterised queries", "O"), L("pysql-sqlalchemy", "SQLAlchemy Core", "O"),
                 L("pysql-pandas", "pandas read_sql and to_sql", "O"), L("pysql-bulk", "Bulk loads and fast_executemany", "O"), L("pysql-secrets", "Config and secrets", "O"),
                 L("pysql-upsert", "Repeatable loads: MERGE and upserts", "O"), L("pysql-test-log", "Logging and testing an ETL job", "O"), L("pysql-capstone", "Capstone 1: Python ETL into your warehouse", "O")]},
    {"id": "M7", "title": "pandas and data quality", "basis": "O, D (duplicates, missing and late data).",
     "lessons": [L("pd-basics", "DataFrames and Series", "O"), L("pd-select", "Select and filter", "O"), L("pd-groupby", "groupby and aggregates", "O"), L("pd-merge", "merge and join", "O"),
                 L("pd-window", "rolling, shift and rank", "O"), L("pd-dtypes", "dtypes and missing values", "O"), L("pd-dedupe", "Duplicates and late-arriving data", "D, O"), L("pd-parquet", "Parquet files", "O")]},
    {"id": "M8", "title": "Engineering toolbox", "basis": "Z (module 1) plus O.",
     "lessons": [L("eng-cli", "The command line", "Z, O"), L("eng-git", "Git and GitHub", "Z, O"), L("eng-docker", "Docker basics", "Z"), L("eng-compose", "Docker Compose and Postgres in Docker", "Z"),
                 L("eng-terraform", "Infrastructure as code with Terraform", "Z"), L("eng-gcp", "GCP basics", "Z")]},
    {"id": "M9", "title": "Orchestration and ingestion", "basis": "Z (module 2), D (orchestrate processes).",
     "lessons": [L("orch-concepts", "Schedules, idempotence and backfills", "Z, D"), L("orch-kestra", "Kestra flows", "Z"), L("orch-params", "Parameters and triggers", "Z, D"),
                 L("orch-lake", "Ingest to a data lake", "Z"), L("orch-incremental", "Incremental patterns", "D"), L("orch-reliability", "Retries, alerts and monitoring", "D")]},
    {"id": "M10", "title": "Cloud warehouse and analytics engineering", "basis": "Z (modules 3 to 5).",
     "lessons": [L("bq-basics", "BigQuery basics", "Z"), L("bq-partition", "Partitioning and clustering", "Z"), L("dbt-models", "dbt models", "Z"), L("dbt-tests", "dbt tests and docs", "Z"),
                 L("dbt-incremental", "dbt incremental models", "Z, O"), L("plat-bruin", "Data platforms with Bruin", "Z"), L("bi-dash", "Dashboards", "Z")]},
    {"id": "M11", "title": "Microsoft Fabric track", "basis": "D (all three skill areas). Needs a Fabric account. Access not checked.",
     "lessons": [L("fab-workspace", "Workspaces, OneLake and settings", "D"), L("fab-stores", "Lakehouse or warehouse: choose a data store", "D"), L("fab-pipelines", "Pipelines, Dataflow Gen2 and notebooks", "D"),
                 L("fab-pyspark", "Transform with PySpark and T-SQL", "D"), L("fab-kql", "KQL and Eventstream", "D"), L("fab-security", "Security and governance", "D"),
                 L("fab-lifecycle", "Version control and deployment pipelines", "D"), L("fab-monitor", "Monitor and optimise", "D"), L("fab-practice", "DP-700 practice review", "D")]},
    {"id": "M12", "title": "Spark and Kafka", "basis": "Z (modules 6 and 7).",
     "lessons": [L("spark-basics", "Spark and DataFrames", "Z"), L("spark-sql", "Spark SQL, GroupBy and joins", "Z"), L("spark-tuning", "Spark performance", "Z, D"),
                 L("kafka-basics", "Kafka basics", "Z"), L("kafka-streams", "Kafka Streams and KSQL", "Z"), L("kafka-schemas", "Schemas with Avro", "Z")]},
    {"id": "M13", "title": "Capstone and job readiness", "basis": "Z (capstone) plus O.",
     "lessons": [L("cap-design", "Design the capstone", "Z"), L("cap-build", "Build the pipeline", "Z"), L("cap-docs", "Documents, dashboard and presentation", "Z"),
                 L("interview", "SQL and Python interview practice", "O"), L("portfolio", "Portfolio and CV", "O")]},
]

# Ideas taught by planned lessons that built lessons may need (this is what holds a lesson back)
PLANNED_TEACHES = {"py-classes": ["class", "init", "self", "methods"]}


def tag_legacy(legacy):
    """Add teaches/uses and small content fixes to the older lessons."""
    t = legacy
    t["py-dict-count"].update(
        teaches=["dict", "dict-get", "dict-items", "tally"],
        uses=["loop-for", "if", "in-operator", "def", "return", "lambda", "sort-key", "sorted", "list", "str", "f-string", "print", "list-methods"])
    t["py-mutable-default"].update(
        teaches=["mutable-default"],
        uses=["def", "return", "params-defaults", "list", "dict", "dict-get", "if", "none", "print", "list-methods"])
    t["py-except-order"]["explain"].insert(0, {"h": "Your own error types", "p": [
        "You can make your own error type. It is a class that inherits from Exception.",
        "For now, copy this class. The text in triple quotes is a docstring. Lesson 1.5 explained it.",
        "class InsufficientFundsError(Exception):  then, on the next line, indented: a docstring.",
        "Classes have their own lesson later. You only need the one line here."]})
    t["py-except-order"].update(
        teaches=["try-except", "except-order", "custom-exception-line"],
        uses=["def", "return", "if", "loop-for", "dict", "dict-get", "tally", "csv", "stringio", "break", "convert-types", "float", "print", "list-methods", "str"])
    t["py-generators"].update(
        teaches=["generator", "yield", "generator-expr"],
        uses=["list-comp", "def", "return", "loop-for", "if", "sum-min-max", "list", "dict", "print", "round"])
    t["sql-where-having"].update(teaches=["where-having", "logical-order"], uses=["sql-select", "sql-groupby", "sql-cte", "sql-scalar-subquery"])
    t["sql-window-frames"].update(teaches=["frames", "last-value"], uses=["sql-window-basic", "sql-cte"])
    t["sql-percentile"].update(teaches=["percentile"], uses=["sql-window-basic", "sql-groupby"])
    t["sql-rollup-grouping"].update(teaches=["rollup", "grouping"], uses=["sql-groupby", "sql-case", "sql-coalesce-cast", "sql-cte"])
    t["sql-correlated-vs-window"].update(teaches=["correlated-subquery"], uses=["sql-scalar-subquery", "frames", "sql-window-basic", "sql-groupby"])
    t["py-class-property"].update(teaches=["property", "repr"], uses=["class", "init", "self", "methods", "def", "return", "f-string", "list", "lambda", "sort-key", "sorted"])
    for k in ("py-dict-count", "py-mutable-default", "py-except-order", "py-generators"):
        t[k]["videos"] = []          # your videos replace the outside links
        t[k].pop("compared", None)
    return t


def run_task(task, lang_py=True):
    setup = task.get("setup", "")
    item = {"title": task["title"], "task": task["task"], "hint": task["hint"], "setup": setup, "sql": task["answer"],
            "output": pm.run(setup + "\n" + task["answer"]), "lang": "python"}
    if task.get("broken"):
        item["broken"] = task["broken"]
        item["brokenOutput"] = pm.run(setup + "\n" + task["broken"])
    return item


def run_script_example(ex):
    sc = ex["script"]
    with tempfile.TemporaryDirectory() as d:
        if not sc.get("display_only"):
            open(os.path.join(d, sc["name"]), "w").write(ex["code"])
        for n, c in sc["files"].items():
            open(os.path.join(d, n), "w").write(c)
        r = subprocess.run([sys.executable, "-I", *sc["cmd"]], cwd=d, capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr
        out = r.stdout.rstrip("\n")
        if sc.get("tidy"):   # drop the run time and long runs of spaces (they change from run to run)
            out = re.sub(r" in \d+\.\d+s", "", out)
            out = re.sub(r" {3,}", "   ", out)
        ex["output"] = "$ " + sc["show"] + "\n" + out
    del ex["script"]


def verify_extra():
    """Reference answers for build tasks that need files. Run in a temp folder."""
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "orders.csv"), "w").write("id,customer,amount\n1,Acme,120\n2,Birch,40\n3,Acme,80\n4,Cobalt,200\n")
        code = ("import csv, json\ntotals = {}\nwith open('orders.csv', newline='') as f:\n    for row in csv.DictReader(f):\n"
                "        totals[row['customer']] = totals.get(row['customer'], 0) + float(row['amount'])\nwith open('totals.json', 'w') as f:\n    json.dump(totals, f, indent=2)\n")
        open(os.path.join(d, "t.py"), "w").write(code)
        assert subprocess.run([sys.executable, "-I", "t.py"], cwd=d).returncode == 0
        assert json.load(open(os.path.join(d, "totals.json"))) == {"Acme": 200.0, "Birch": 40.0, "Cobalt": 200.0}
        tool = ("import argparse, csv\nparser = argparse.ArgumentParser()\nparser.add_argument('filename')\nparser.add_argument('--top', type=int, default=3)\nargs = parser.parse_args()\n"
                "with open(args.filename, newline='') as f:\n    rows = list(csv.DictReader(f))\nfor r in sorted(rows, key=lambda r: float(r['amount']), reverse=True)[:args.top]:\n    print(r['id'], r['customer'], r['amount'])\n")
        open(os.path.join(d, "tool.py"), "w").write(tool)
        out = subprocess.run([sys.executable, "-I", "tool.py", "orders.csv", "--top", "2"], cwd=d, capture_output=True, text=True).stdout.split("\n")
        assert out[0].startswith("4 Cobalt 200") and out[1].startswith("1 Acme 120"), out
        # __name__ claim for the scripts lesson
        open(os.path.join(d, "tool2.py"), "w").write("print(__name__)\n")
        assert subprocess.run([sys.executable, "-I", "tool2.py"], cwd=d, capture_output=True, text=True).stdout.strip() == "__main__"
        assert subprocess.run([sys.executable, "-c", "import tool2"], cwd=d, capture_output=True, text=True).stdout.strip() == "tool2"


def verify_mypy():
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "report.py"), "w").write(m2b.TYPING_CODE + "\n")
        r = subprocess.run([sys.executable, "-m", "mypy", "report.py"], cwd=d, capture_output=True, text=True)
        out = r.stdout
        assert 'report.py:18: error: Argument 1 to "add_vat" has incompatible type "str"; expected "float"' in out, out
        assert 'report.py:20: error: Value of type "dict[Any, Any] | None" is not indexable' in out, out
        fixed = m2b.TYPING_CODE.replace('print(add_vat("10", 2))\n', 'print(add_vat(10, 2))\n').replace('print(found["amount"])', 'if found is not None:\n    print(found["amount"])')
        open(os.path.join(d, "ok.py"), "w").write(fixed + "\n")
        r = subprocess.run([sys.executable, "-m", "mypy", "ok.py"], cwd=d, capture_output=True, text=True)
        assert "Success: no issues found in 1 source file" in r.stdout, r.stdout


def main(out_dir):
    legacy = {t["id"]: copy.deepcopy(t) for t in bt.TOPICS}
    tag_legacy(legacy)
    lessons = {x["id"]: copy.deepcopy(x) for x in m1.LESSONS + m2a.LESSONS + m2b.LESSONS}
    for k, v in legacy.items():
        lessons.setdefault(k, v)

    # --- senior-style worked examples replace the old ones
    ep.sql_checks()
    for lid, ex in ep.EXAMPLES.items():
        t = lessons[lid]
        code = m2b.TYPING_CODE if ex["code"] == "TYPING_CODE" else ex["code"]
        new_ex = {"title": ex["title"], "code": code, "notes": ex["notes"]}
        if "output" in ex:
            new_ex["output"] = ex["output"]
        if "script" in ex:
            new_ex["script"] = ex["script"]
        t["example"] = new_ex
        extra = list(ex.get("uses_add", []))
        if '\"\"\"'.replace("\\", "") in code and lid != "py-functions" and "docstring" not in extra:
            extra.append("docstring")
        if "__main__" in code and lid != "py-scripts" and "main-guard" not in extra:
            extra.append("main-guard")
        t["uses"] = list(dict.fromkeys(t.get("uses", []) + extra))

    # --- run every claim
    for code, expect in m1.CHECKS + m2a.CHECKS + m2b.CHECKS:
        got = pm.run(code)
        assert got.strip() == expect.strip(), f"CHECK FAILED\n{code}\nexpected {expect!r}\n got {got!r}"
    for code, parts in m2b.CHECKS_HAS:
        got = pm.run(code)
        for part in parts:
            assert part in got, f"CHECK FAILED\n{code}\nmissing {part!r}\n got {got!r}"
    verify_extra()
    verify_mypy()

    # --- order and number
    order, plan = [], []
    for mi, m in enumerate(MODULES, 1):
        for li, entry in enumerate(m["lessons"], 1):
            lid = entry if isinstance(entry, str) else entry["id"]
            title = lessons[lid]["title"] if lid in lessons else entry["title"]
            src = "O" if lid in lessons and lid.startswith("py-") else (entry["src"] if not isinstance(entry, str) else "")
            order.append(lid)
            plan.append({"id": lid, "module": m["id"], "no": f"{mi}.{li}", "title": title, "src": src, "entry": entry})

    # --- concept check
    known, taught_by = set(), {}
    status = {}
    for p in plan:
        lid = p["id"]
        if lid not in lessons:
            status[lid] = "planned"
            continue
        t = lessons[lid]
        unmet = [u for u in t.get("uses", []) if u not in known and u not in ASSUMED]
        if unmet:
            waiting = [pl for pl, tags in PLANNED_TEACHES.items() if any(u in tags for u in unmet)]
            if not waiting or any(u not in sum(PLANNED_TEACHES.values(), []) for u in unmet):
                raise SystemExit(f"COVERAGE ERROR: lesson {lid} uses ideas that nothing teaches earlier: {unmet}")
            status[lid] = "waiting"
            t["waitsFor"] = waiting
            continue
        status[lid] = "built"
        for tag in t.get("teaches", []):
            known.add(tag)
            taught_by.setdefault(tag, lid)

    # --- fill outputs
    for lid, t in lessons.items():
        if status.get(lid) != "built":
            continue
        if t["track"] == "Python":
            if "script" in t["example"]:
                run_script_example(t["example"])
            elif "output" not in t["example"]:
                t["example"]["output"] = pm.run(t["example"]["code"])
            tasks = (m1.MIXED.get(lid) or m1.LEGACY_MIXED.get(lid) or m2a.MIXED.get(lid) or m2b.MIXED.get(lid) or [])
            t["mixed"] = [run_task(x) for x in tasks]
        t.setdefault("videos", [])
    sqlmixed = mt.run_all()
    for lid, items in sqlmixed.items():
        if status.get(lid) == "built":
            lessons[lid]["mixed"] = items

    # --- prerequisites
    meta = {p["id"]: p for p in plan}
    topics = []
    for p in plan:
        lid = p["id"]
        if status[lid] != "built":
            continue
        t = lessons[lid]
        pre, seen = [], set()
        for u in t.get("uses", []):
            src = taught_by.get(u)
            if src and src != lid and src not in seen:
                seen.add(src)
                pre.append({"id": src, "title": lessons[src]["title"], "no": meta[src]["no"]})
        pre.sort(key=lambda x: order.index(x["id"]))
        t["prereqs"] = pre
        t["assumed"] = [{"label": ASSUMED[u][0], "lesson": ASSUMED[u][1]} for u in dict.fromkeys(t.get("uses", [])) if u in ASSUMED]
        t["module"] = p["module"]
        t["lessonNo"] = p["no"]
        t["num"] = len(topics) + 1
        t.pop("waitsFor", None)
        topics.append(t)

    # --- syllabus for the site
    syl = []
    for mi, m in enumerate(MODULES, 1):
        items = []
        for p in plan:
            if p["module"] != m["id"]:
                continue
            e = {"id": p["id"], "no": p["no"], "title": p["title"], "status": status[p["id"]], "src": p["src"]}
            if status[p["id"]] == "waiting":
                e["waitsFor"] = [{"id": w, "title": meta[w]["title"], "no": meta[w]["no"]} for w in lessons[p["id"]].get("waitsFor", PLANNED_TEACHES and ["py-classes"])]
            items.append(e)
        syl.append({"id": m["id"], "no": mi, "title": m["title"], "basis": m["basis"], "lessons": items})

    site = {
        "title": "Data Engineering Study Site", "generated": date.today().isoformat(),
        "defaultStart": "2026-10-27", "defaultPace": 4, "totalLessons": len(plan), "builtLessons": len(topics),
        "sources": SOURCES, "assumedNote": "SQL lessons assume these ideas from your earlier SQL days. They are planned as refresher lessons in module 3 and 4. Tell Claude if any is new.",
        "milestones": [
            {"date": "2027-06-21", "label": "Summer 2027: your target for first Data Engineer applications (from your roadmap)"}],
        "notes": ["The Zoomcamp page says cohorts start 'around January each year'. It gives no exact 2027 date. Check the DataTalks.Club site before you plan around it."],
    }
    os.makedirs(os.path.join(out_dir, "data"), exist_ok=True)
    for t in topics:
        for k in ("teaches", "uses", "videos", "videoPending", "reading", "compared", "ownVideo"):
            t.pop(k, None)
    js = ("window.SITE = " + json.dumps(site, ensure_ascii=False, indent=1) + ";\n"
          "window.SYLLABUS = " + json.dumps(syl, ensure_ascii=False, indent=1) + ";\n"
          "window.TOPICS = " + json.dumps(topics, ensure_ascii=False, indent=1) + ";\n")
    open(os.path.join(out_dir, "data", "topics.js"), "w", encoding="utf-8").write(js)
    waiting = [k for k, v in status.items() if v == "waiting"]
    print(f"Lessons in plan: {len(plan)} | built: {len(topics)} | waiting: {waiting} | planned: {sum(1 for v in status.values() if v == 'planned')}")
    return topics


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
