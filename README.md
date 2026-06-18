# chaoxing-homework-assistant

A Kimi skill for extracting, integrating, and analyzing homework assignments from the Chaoxing (超星) online learning platform.

## What It Does

This skill helps you:

1. **Extract** homework questions, options, your answers, and correct answers from Chaoxing course pages via Kimi WebBridge.
2. **Integrate** multiple assignments into a single Markdown document.
3. **Analyze** the combined questions to identify high-frequency exam topics and knowledge gaps.
4. **Improve** your review/study outline based on what the homework actually tests.

## Repository Structure

```
chaoxing-homework-assistant/
├── SKILL.md                     # Instructions for Kimi
├── README.md                    # This file
├── scripts/
│   ├── fetch_homeworks.py       # Fetch homework HTML via WebBridge
│   ├── extract_homework.py      # Parse HTML into structured JSON
│   ├── combine_homeworks.py     # Combine JSON files into Markdown
│   └── reextract_all.py         # Batch re-extract existing HTML files
└── references/
    └── webbridge-notes.md       # WebBridge tips for Chaoxing
```

## Quick Start

1. Install and start [Kimi WebBridge](https://kimi.com/features/webbridge).
2. Log into Chaoxing in your browser.
3. Prepare a `urls.json` file:

```json
[
  {"name": "第6讲 天文学革命 作业", "url": "https://mooc1.chaoxing.com/mooc-ans/mooc2/work/task?..."}
]
```

4. Run the scripts:

```powershell
python scripts/fetch_homeworks.py --urls urls.json --out-dir ./homework
python scripts/reextract_all.py --html-dir ./homework --json-dir ./homework
python scripts/combine_homeworks.py --inputs ./homework/hw*.json --output 作业题目整合.md
```

5. Ask Kimi to analyze `作业题目整合.md` and improve your review outline.

## Requirements

- Python 3
- `requests` library
- Kimi WebBridge installed and running
- Chaoxing login session in your browser

## License

MIT
