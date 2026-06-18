"""Combine multiple extracted homework JSON files into one Markdown document.

Usage:
    python combine_homeworks.py --inputs ./homework/hw*.json --output 作业题目整合.md
"""
import argparse
import glob
import json
import os


def main():
    parser = argparse.ArgumentParser(description="Combine homework JSON files into Markdown")
    parser.add_argument("--inputs", nargs="+", required=True, help="Input JSON files (supports glob patterns)")
    parser.add_argument("--output", default="作业题目整合.md", help="Output Markdown file path")
    args = parser.parse_args()

    # Expand globs
    files = []
    for pattern in args.inputs:
        files.extend(glob.glob(pattern))
    files = sorted(set(files))

    lines = []
    lines.append("# 作业题目整合")
    lines.append("")
    lines.append(f"> 共整合 {len(files)} 份作业")
    lines.append("")

    total = 0
    for i, path in enumerate(files, 1):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        lines.append("---")
        lines.append("")
        lines.append(f"## {data['title']} ({data['question_count']}题)")
        lines.append("")

        for q in data["questions"]:
            total += 1
            lines.append(f"### {total}. {q.get('type', '')}")
            lines.append("")
            lines.append(q["question"])
            lines.append("")
            if q["options"]:
                for opt in q["options"]:
                    lines.append(f"- {opt}")
                lines.append("")
            lines.append(f"**我的答案：** {q['student_answer']}")
            lines.append(f"**正确答案：** {q['correct_answer']}")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"**总计：{total} 道题目**")

    os.makedirs(os.path.dirname(os.path.abspath(args.output)) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Combined {total} questions from {len(files)} files -> {args.output}")


if __name__ == "__main__":
    main()
