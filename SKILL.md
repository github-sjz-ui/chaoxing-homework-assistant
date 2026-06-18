---
name: chaoxing-homework-assistant
description: |
  Extract, integrate, and analyze homework assignments from the Chaoxing (超星) online learning platform, then improve study/review outlines based on the extracted questions. Use when the user asks to: (1) collect or integrate Chaoxing homework questions, (2) extract questions/answers from Chaoxing course pages, (3) analyze homework content to identify knowledge gaps, or (4) improve a review/study outline according to homework coverage.
---

# Chaoxing Homework Assistant

Help students extract homework questions from the Chaoxing (超星) platform and turn them into organized review materials.

## What This Skill Does

1. Navigates the user's real browser (via Kimi WebBridge) to Chaoxing homework pages.
2. Fetches the raw HTML of each homework assignment.
3. Parses questions, options, student answers, and correct answers into structured JSON.
4. Combines multiple assignments into a single Markdown file.
5. Analyzes the combined questions and updates a review outline to emphasize tested topics.

## Prerequisites

- Kimi WebBridge must be installed and running (`kimi-webbridge status` shows `running: true` and `extension_connected: true`).
- The user must already be logged into Chaoxing in the browser.
- Python 3 and `requests` must be available.

## Workflow

### 1. Confirm WebBridge health

```powershell
~/.kimi-webbridge/bin/kimi-webbridge status
```

If not healthy, follow the WebBridge skill instructions to install or restart it.

### 2. Collect homework URLs

Ask the user for:
- The course URL (or the list of individual homework/task URLs).
- The display names for each homework (e.g., "第6讲 天文学革命 作业").

If the user only provides the course URL, navigate to it, switch to the "作业" tab, enter the iframe, and read the homework list to discover URLs. See `references/webbridge-notes.md` for iframe handling.

### 3. Fetch and extract homework pages

Use the bundled scripts:

```powershell
python scripts/fetch_homeworks.py --urls urls.json --out-dir ./homework
python scripts/extract_homework.py --html ./homework/hw1-page.html --json ./homework/hw1.json
python scripts/combine_homeworks.py --inputs ./homework/hw*.json --output 作业题目整合.md
```

Or run `fetch_homeworks.py` followed by `reextract_all.py` and `combine_homeworks.py` as a pipeline.

### 4. Improve the review outline

Read the combined Markdown file and the existing review outline. Identify:
- Missing people, dates, concepts, or works that appear in homework.
- High-frequency topics.
- Common distractors or easy-to-confuse options.

Update the outline by adding content to the relevant lecture sections and appending a "作业高频考点速查" section.

## Bundled Scripts

| Script | Purpose |
|--------|---------|
| `scripts/fetch_homeworks.py` | Navigate to each homework URL via WebBridge, fetch raw HTML, and save it. |
| `scripts/extract_homework.py` | Parse a saved homework HTML file into JSON (questions, options, answers). |
| `scripts/combine_homeworks.py` | Combine multiple JSON homework files into one Markdown document. |
| `scripts/reextract_all.py` | Re-run extraction on all saved HTML files in a directory. |

## Important Notes

- Chaoxing homework pages are usually UTF-8; fetch raw bytes and decode as UTF-8.
- The course portal loads the homework list inside an iframe. Use `evaluate` to read the iframe `src`, then navigate to that URL directly.
- The HTML may be malformed; BeautifulSoup alone can miss questions. The extractor uses regex on top of HTML parsing to recover all question blocks.
- Fill-in-the-blank answers may not be exposed in the HTML; ask the user or infer from course content when missing.

## When Not to Use

- For non-Chaoxing platforms. This skill assumes Chaoxing's specific HTML structure.
- When the user is not already logged into Chaoxing in their browser.
