"""Re-run extraction on all saved homework HTML files in a directory.

Usage:
    python reextract_all.py --html-dir ./homework --json-dir ./homework
"""
import argparse
import glob
import os
from extract_homework import extract_questions, extract_title


def main():
    parser = argparse.ArgumentParser(description="Re-extract all homework HTML files in a directory")
    parser.add_argument("--html-dir", default=".", help="Directory containing hw*-page.html files")
    parser.add_argument("--json-dir", default=None, help="Directory to write JSON files (defaults to html-dir)")
    args = parser.parse_args()

    json_dir = args.json_dir or args.html_dir
    os.makedirs(json_dir, exist_ok=True)

    html_files = sorted(glob.glob(os.path.join(args.html_dir, "hw*-page.html")))
    for html_path in html_files:
        basename = os.path.basename(html_path)
        idx = basename.rfind("-page.html")
        name = basename[:idx]
        json_path = os.path.join(json_dir, f"{name}.json")

        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()

        title = extract_title(html)
        questions = extract_questions(html)
        result = {
            "title": title,
            "question_count": len(questions),
            "questions": questions,
        }

        with open(json_path, "w", encoding="utf-8") as f:
            import json
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"{title}: {len(questions)} questions -> {json_path}")


if __name__ == "__main__":
    main()
