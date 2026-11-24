# Data Engineering Study Site

A static website (no build step, no server). Six tabs: Today (your hour, the minimum day, the 15-minute rule, daily tick and wins), Recall (a daily 15-minute closed-book quiz on your lessons, spaced so old lessons come back), Course (every lesson), Genomics project (project pages and milestones), Progress (lesson ticks and schedule, with Export) and Help.

## Put it on GitHub (no git needed)
1. Sign in to github.com. Click New repository. Name it `dataeng-study`. Choose Public. Click Create.
2. Click "uploading an existing file". Drag in everything from this folder: `index.html`, `style.css`, `app.js`, the `data` folder (`topics.js`, `genomics.js` and `recall.js`) and `.nojekyll`.
   If the `.nojekyll` file does not upload, skip it. The site works without it.
3. Click Commit changes.
4. Go to Settings, then Pages. Under Source choose "Deploy from a branch". Choose branch `main` and folder `/ (root)`. Click Save.
5. Wait one or two minutes. GitHub shows the address: `https://YOUR-NAME.github.io/dataeng-study/`.

## Use it
- Open a topic. Do the eight steps. Tick the five boxes at the bottom.
- Progress, then Lesson ticks: shows all ticks. "Copy summary for Claude" copies a text summary. Paste it in the chat to get a mini test.
- Progress, then Schedule: compares topics done with topics the plan expects by today. Change the start and finish dates to match your real time.
- Export your progress from Progress, Lesson ticks now and then. The export includes your streak, wins, project ticks and Recall progress. Ticks are saved in the browser only.

## Add a topic
Lessons live in `lessons_m1.py`, `lessons_m2.py`, `lessons_m2b.py`, `lessons_m3.py`, `lessons_m3b.py` (groupby, merge, rolling), `lessons_m3c.py` (forecasting) and `build_topics.py` (older lessons). Senior-style worked examples are in `examples_pro.py` in the `dataeng-site-src` folder. The course order is in `build_course.py`. Run `python3 build_course.py <site folder>`. It runs every example, checks that no lesson uses an idea taught later, and rewrites `data/topics.js` and `data/recall.js` (the Recall cards come from each lesson's self-check, prediction, question and build task). Upload those two files again.
Run every code example before you write its output into a topic.


## About the worked examples
Each worked example is written in the style a senior engineer would use, with a box that says why. The Python style follows PEP 8 (layout and names), PEP 20 (the Zen of Python) and PEP 257 (docstrings). The SQL follows common T-SQL style. The Python output is made by running the code. The SQL results were checked in DuckDB, not on SQL Server.


## Genomics project tab

The `Genomics project` tab shows the day pages and guides of the guided project. They are written as markdown in the project folder and converted by `python3 dataeng-site-src/build_genomics.py <site folder> <project folder>`, which writes `data/genomics.js`. Run it again whenever a project page changes, then upload `data/genomics.js`. The tab itself lives in `app.js`, `index.html` and `style.css`.


## Recall tab

Recall cards are made from the built lessons when you run `build_course.py` (self-check, prediction and code questions), plus 12 core SQL and project cards in `build_course.py` (`CORE_CARDS`). Writing practice is not on the site: it is `python drill.py` in the project folder. Your progress (which cards, which box, when due) is saved in this browser under the same key as your ticks, so Export covers it. Boxes: a right answer moves a card up (due after 1, 2, 4, 8, 16, 32 days), a miss sends it back to box 1 (due tomorrow). New cards are capped at 6 a day, a session is up to 6 cards, and reviews come first.
