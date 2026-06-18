"""Fetch Chaoxing homework pages via Kimi WebBridge.

Usage:
    python fetch_homeworks.py --urls urls.json --out-dir ./homework

urls.json format:
    [
      {"name": "第6讲 天文学革命 作业", "url": "https://mooc1.chaoxing.com/mooc-ans/mooc2/work/task?..."},
      ...
    ]
"""
import argparse
import base64
import json
import os
import time
import requests

FETCH_CODE = """
(async () => {
  const resp = await fetch(location.href);
  const buf = await resp.arrayBuffer();
  const bytes = new Uint8Array(buf);
  let binary = '';
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
})()
"""

DEFAULT_BRIDGE = "http://127.0.0.1:10086/command"
DEFAULT_SESSION = "chaoxing-homework"


def wb_request(action, args, bridge, session):
    r = requests.post(bridge, json={"action": action, "args": args, "session": session}, timeout=60)
    r.raise_for_status()
    return r.json()


def navigate(url, bridge, session):
    return wb_request("navigate", {"url": url, "newTab": False}, bridge, session)


def fetch_page(bridge, session):
    resp = wb_request("evaluate", {"code": FETCH_CODE}, bridge, session)
    if not resp.get("ok"):
        raise RuntimeError(f"fetch failed: {resp}")
    raw = base64.b64decode(resp["data"]["value"])
    return raw.decode("utf-8", errors="replace")


def load_urls(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Fetch Chaoxing homework pages via WebBridge")
    parser.add_argument("--urls", required=True, help="Path to JSON file containing homework URL list")
    parser.add_argument("--out-dir", default=".", help="Directory to save HTML files")
    parser.add_argument("--bridge", default=DEFAULT_BRIDGE, help="WebBridge HTTP endpoint")
    parser.add_argument("--session", default=DEFAULT_SESSION, help="WebBridge session name")
    parser.add_argument("--delay", type=int, default=4, help="Seconds to wait after each navigation")
    args = parser.parse_args()

    homeworks = load_urls(args.urls)
    os.makedirs(args.out_dir, exist_ok=True)

    for i, hw in enumerate(homeworks, 1):
        name = hw.get("name", f"hw{i}")
        url = hw["url"]
        print(f"[{i}/{len(homeworks)}] Fetching: {name}")
        try:
            navigate(url, args.bridge, args.session)
            time.sleep(args.delay)
            html = fetch_page(args.bridge, args.session)
            out_path = os.path.join(args.out_dir, f"hw{i}-page.html")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"  Saved -> {out_path} ({len(html)} chars)")
        except Exception as e:
            print(f"  ERROR: {e}")


if __name__ == "__main__":
    main()
