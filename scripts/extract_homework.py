"""Parse a Chaoxing homework HTML file into structured JSON.

Usage:
    python extract_homework.py --html hw1-page.html --json hw1.json [--title "..."]
"""
import argparse
import html as ihtml
import json
import re


def clean_html(raw):
    """Remove HTML tags and decode entities, preserving text structure."""
    if not raw:
        return ""
    raw = re.sub(r"<script[^>]*>.*?</script>", "", raw, flags=re.S)
    raw = re.sub(r"<style[^>]*>.*?</style>", "", raw, flags=re.S)
    raw = re.sub(r"<br\s*/?>", "\n", raw, flags=re.I)
    raw = re.sub(r"</p>", "\n", raw, flags=re.I)
    raw = re.sub(r"<p[^>]*>", "", raw, flags=re.I)
    raw = re.sub(r"</span>", "", raw, flags=re.I)
    raw = re.sub(r"<span[^>]*>", "", raw, flags=re.I)
    raw = re.sub(r"<[^>]+>", "", raw)
    raw = ihtml.unescape(raw)
    raw = raw.replace("\xa0", " ")
    raw = re.sub(r"[ \t]+", " ", raw)
    raw = re.sub(r"\n\s*\n+", "\n", raw)
    return raw.strip()


def extract_title(html):
    m = re.search(r'<h2 class="mark_title"[^>]*>(.*?)</h2>', html, re.S)
    if m:
        return clean_html(m.group(1))
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if m:
        return clean_html(m.group(1))
    return ""


def extract_questions(html):
    """Extract questions from Chaoxing homework HTML using regex."""
    questions = []
    pattern = r'<div[^>]*class="[^"]*questionLi[^"]*"[^>]*id="(question\d+)"[^>]*data="(\d+)"[^>]*>'
    matches = list(re.finditer(pattern, html))

    for i, m in enumerate(matches):
        qdata = m.group(2)
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(html)
        block = html[start:end]

        # Question text
        qtext = ""
        qtext_match = re.search(
            r'<h3 class="mark_name[^"]*"[^>]*>.*?</span>\s*<span class="qtContent workTextWrap">(.*?)</span>\s*</h3>',
            block, re.S,
        )
        if qtext_match:
            qtext = clean_html(qtext_match.group(1))
        if not qtext.strip():
            qtext_match2 = re.search(r'<h3 class="mark_name[^"]*"[^>]*>(.*?)</h3>', block, re.S)
            if qtext_match2:
                qtext = clean_html(qtext_match2.group(1))
                qtext = re.sub(r"^\d+\.\s*\([^)]*\)", "", qtext).strip()

        # Options
        options = []
        opt_matches = re.findall(
            r'<li[^>]*class="workTextWrap"[^>]*>\s*[A-D]\.\s*(.*?)\s*</li>', block, re.S
        )
        if opt_matches:
            options = [clean_html(o) for o in opt_matches]
        else:
            opt_matches = re.findall(r'<li[^>]*class="workTextWrap"[^>]*>(.*?)</li>', block, re.S)
            for opt in opt_matches:
                opt = clean_html(opt)
                opt = re.sub(r"^[A-D]\.\s*", "", opt).strip()
                if opt:
                    options.append(opt)

        right_match = re.search(r'<span class="rightAnswerContent[^"]*">(.*?)</span>', block, re.S)
        right_answer = clean_html(right_match.group(1)) if right_match else ""

        stu_match = re.search(r'<span class="stuAnswerContent">(.*?)</span>', block, re.S)
        stu_answer = clean_html(stu_match.group(1)) if stu_match else ""

        type_match = re.search(r'<span class="colorShallow">\((.*?)\)</span>', block, re.S)
        qtype = clean_html(type_match.group(1)) if type_match else ""

        questions.append({
            "id": qdata,
            "type": qtype,
            "question": qtext,
            "options": options,
            "student_answer": stu_answer,
            "correct_answer": right_answer,
        })

    return questions


def main():
    parser = argparse.ArgumentParser(description="Extract questions from a Chaoxing homework HTML file")
    parser.add_argument("--html", required=True, help="Input HTML file path")
    parser.add_argument("--json", required=True, help="Output JSON file path")
    parser.add_argument("--title", default=None, help="Override homework title")
    args = parser.parse_args()

    with open(args.html, "r", encoding="utf-8") as f:
        html = f.read()

    title = args.title or extract_title(html)
    questions = extract_questions(html)

    result = {
        "title": title,
        "question_count": len(questions),
        "questions": questions,
    }

    with open(args.json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Extracted {len(questions)} questions from '{title}' -> {args.json}")


if __name__ == "__main__":
    main()
