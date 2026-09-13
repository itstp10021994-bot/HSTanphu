#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tự động kiểm tra định kỳ market_data.json xem các con số đã trích dẫn từ
mỗi nguồn có còn xuất hiện trên trang gốc hay không.

CÁCH HOẠT ĐỘNG (an toàn, không tự "bịa" số liệu mới):
1. Với mỗi ngành có market_note, tải lại đúng trang "source_url".
2. Trích các con số dạng "xx triệu" trong câu mô tả đang lưu (VD: "15-40").
3. So với các con số "xx triệu" tìm thấy trên trang gốc hiện tại.
4. Nếu KHÔNG còn con số nào trùng khớp -> rất có thể trang đã cập nhật số
   liệu mới -> đánh dấu status = "needs_review" để người kiểm duyệt xem
   lại và tự viết câu mô tả mới (script KHÔNG tự viết lại câu, tránh rủi
   ro đưa thông tin sai/bịa cho học sinh).
5. Nếu vẫn khớp -> chỉ cập nhật "last_checked" (ngày kiểm tra gần nhất).
6. Nếu không tải được trang (mạng lỗi, bị chặn...) -> bỏ qua, giữ nguyên
   trạng thái cũ, KHÔNG coi đó là dấu hiệu cần xem lại.

Chạy định kỳ qua GitHub Actions (xem .github/workflows/update-market-data.yml).
"""
import json
import os
import re
import sys
from datetime import date, timezone

try:
    import requests
except ImportError:
    print("Thiếu thư viện 'requests'. Cài bằng: pip install -r scripts/requirements.txt")
    sys.exit(1)

MARKET_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "market_data.json")
USER_AGENT = "Mozilla/5.0 (compatible; CareerSimBot/1.0; +https://github.com/)"
NUMBER_TOKEN = r"\d{1,3}(?:[.,]\d{1,3})?"
RANGE_PATTERN = re.compile(
    rf"({NUMBER_TOKEN})\s*(?:[-–—]|đến|tới)?\s*({NUMBER_TOKEN})?\s*(?:triệu|tr\b)",
    re.IGNORECASE,
)
PERCENT_PATTERN = re.compile(
    rf"({NUMBER_TOKEN})\s*(?:[-–—]|đến|tới)?\s*({NUMBER_TOKEN})?\s*%",
)


def _parse_num(token):
    """'16,5' hoặc '16.5' -> 16 (làm tròn xuống, đủ dùng để so sánh thô)."""
    try:
        return int(float(token.replace(",", ".")))
    except ValueError:
        return None


def extract_numbers(text):
    """Lấy tập hợp các con số xuất hiện trong văn bản, gồm cả dạng tiền
    ("13-20 triệu", "16,5 triệu") lẫn dạng phần trăm ("15-20%"). Số tiền và
    số phần trăm gộp chung một tập hợp — chỉ dùng để so sánh thô xem trang
    gốc có còn nhắc tới các con số đã trích dẫn hay không, không cần phân
    biệt đơn vị."""
    numbers = set()
    for pattern in (RANGE_PATTERN, PERCENT_PATTERN):
        for m in pattern.finditer(text):
            for group in (m.group(1), m.group(2)):
                if group:
                    n = _parse_num(group)
                    if n is not None:
                        numbers.add(n)
    return numbers


def strip_html(html):
    """Bỏ thẻ HTML một cách đơn giản để lấy văn bản thô (đủ dùng để dò số)."""
    html = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<style[^>]*>.*?</style>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<[^>]+>", " ", html)
    return html


def check_entry(career_id, entry):
    stored_numbers = extract_numbers(entry.get("text", ""))
    url = entry.get("source_url")
    if not url:
        return entry, "skip", "không có source_url"

    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as err:
        return entry, "skip", f"không tải được trang ({err})"

    page_numbers = extract_numbers(strip_html(resp.text))

    if not stored_numbers:
        # Không trích được số từ câu đang lưu — không đủ cơ sở so sánh, bỏ qua.
        return entry, "skip", "không trích được số liệu để so sánh"

    overlap = stored_numbers & page_numbers
    today = date.today().isoformat()
    updated = dict(entry)
    updated["last_checked"] = today

    if overlap:
        updated["status"] = "ok"
        return updated, "ok", f"khớp {sorted(overlap)}"
    else:
        updated["status"] = "needs_review"
        return updated, "needs_review", "không còn số liệu nào khớp — có thể trang đã đổi"


def main():
    with open(MARKET_DATA_PATH, encoding="utf-8") as f:
        market_data = json.load(f)

    changed = False
    for career_id, entry in market_data.items():
        updated_entry, status, detail = check_entry(career_id, entry)
        print(f"[{career_id}] {status}: {detail}")
        if updated_entry != entry:
            market_data[career_id] = updated_entry
            changed = True

    if changed:
        with open(MARKET_DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(market_data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("Đã cập nhật market_data.json")
    else:
        print("Không có thay đổi nào cần ghi lại")


if __name__ == "__main__":
    main()
