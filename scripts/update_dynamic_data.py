#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tự động kiểm tra định kỳ (hàng tuần) CẢ 3 file dữ liệu "động":
  - market_data.json      (lương & thị trường)
  - study_data.json       (khối thi & lộ trình học tập)
  - automation_data.json  (xu hướng AI/tự động hoá — theo WEF)

TRIẾT LÝ CHUNG (an toàn, không tự "bịa" số liệu mới):
Với mỗi mục, script tải lại đúng trang nguồn và kiểm tra xem nội dung đã
lưu có còn khớp với những gì trang nguồn đang hiển thị không.
  - Còn khớp    -> chỉ cập nhật "last_checked" (ngày kiểm tra gần nhất).
  - Không khớp  -> đánh dấu status = "needs_review" để người kiểm duyệt
                   xem lại và tự viết lại nội dung cho đúng. Script KHÔNG
                   tự viết lại câu mô tả, tránh rủi ro hiển thị thông tin
                   sai/bịa cho học sinh.
  - Không tải được trang (lỗi mạng...) -> bỏ qua, giữ nguyên trạng thái cũ.

Ba loại dữ liệu có mức độ kiểm chứng khác nhau vì bản chất nguồn khác nhau:
  - market_data: kiểm tra CHÍNH XÁC theo từng ngành — mỗi ngành có 1 trang
    nguồn riêng, so khớp trực tiếp các con số lương đã trích dẫn.
  - study_data: tất cả các ngành dùng CHUNG 1 trang nguồn (trang liệt kê
    tổ hợp môn xét tuyển của Tuyển Sinh 247) — kiểm tra xem các mã khối
    thi đã lưu (VD: A00, B00) có còn xuất hiện trong danh sách tổ hợp
    môn chính thức hay không.
  - automation_data: tất cả các ngành cùng dùng 1 nguồn duy nhất (báo cáo
    PDF của WEF) — kiểm tra xem từ khoá tiếng Anh liên quan đến ngành đó
    có còn xuất hiện trong nội dung báo cáo hay không. Bản thân báo cáo
    này chỉ ra bản mới sau mỗi 1-2 năm nên phần lớn các tuần sẽ không có
    gì thay đổi để báo — đây là điều bình thường, không phải lỗi.

Chạy định kỳ qua GitHub Actions (xem .github/workflows/update-dynamic-data.yml).
"""
import json
import os
import re
import sys
from datetime import date
from functools import lru_cache

try:
    import requests
except ImportError:
    print("Thiếu thư viện 'requests'. Cài bằng: pip install -r scripts/requirements.txt")
    sys.exit(1)

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
USER_AGENT = "Mozilla/5.0 (compatible; CareerSimBot/1.0; +https://github.com/)"
TODAY = date.today().isoformat()


def load_json(filename):
    path = os.path.join(BASE_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(filename, data):
    path = os.path.join(BASE_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


@lru_cache(maxsize=None)
def fetch_text(url, timeout=20):
    """Tải 1 trang và trả về text thô (đã bỏ thẻ HTML). Cache theo URL để
    không tải lại nhiều lần cùng 1 trang (VD: study_data dùng chung 1 URL
    cho cả 25 ngành)."""
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    resp.raise_for_status()
    html = resp.text
    html = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<style[^>]*>.*?</style>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    return re.sub(r"<[^>]+>", " ", html)


@lru_cache(maxsize=None)
def fetch_pdf_text(url, timeout=60):
    """Tải 1 file PDF và trả về toàn bộ text trích xuất được. Cache theo
    URL vì automation_data dùng chung 1 file PDF cho cả 25 ngành."""
    import pypdf
    import io

    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    resp.raise_for_status()
    reader = pypdf.PdfReader(io.BytesIO(resp.content))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


# ---------------------------------------------------------------------
# 1. market_data.json — so khớp con số lương theo từng ngành
# ---------------------------------------------------------------------
NUMBER_TOKEN = r"\d{1,3}(?:[.,]\d{1,3})?"
RANGE_PATTERN = re.compile(
    rf"({NUMBER_TOKEN})\s*(?:[-–—]|đến|tới)?\s*({NUMBER_TOKEN})?\s*(?:triệu|tr\b)",
    re.IGNORECASE,
)
PERCENT_PATTERN = re.compile(rf"({NUMBER_TOKEN})\s*(?:[-–—]|đến|tới)?\s*({NUMBER_TOKEN})?\s*%")


def _parse_num(token):
    try:
        return int(float(token.replace(",", ".")))
    except ValueError:
        return None


def extract_numbers(text):
    numbers = set()
    for pattern in (RANGE_PATTERN, PERCENT_PATTERN):
        for m in pattern.finditer(text):
            for group in (m.group(1), m.group(2)):
                if group:
                    n = _parse_num(group)
                    if n is not None:
                        numbers.add(n)
    return numbers


def check_market_entry(entry):
    stored_numbers = extract_numbers(entry.get("text", ""))
    url = entry.get("source_url")
    if not url or not stored_numbers:
        return entry, "skip", "thiếu source_url hoặc không trích được số để so sánh"
    try:
        page_text = fetch_text(url)
    except requests.RequestException as err:
        return entry, "skip", f"không tải được trang ({err})"

    overlap = stored_numbers & extract_numbers(page_text)
    updated = {**entry, "last_checked": TODAY}
    if overlap:
        updated["status"] = "ok"
        return updated, "ok", f"khớp {sorted(overlap)}"
    updated["status"] = "needs_review"
    return updated, "needs_review", "không còn số liệu nào khớp — có thể trang đã đổi"


# ---------------------------------------------------------------------
# 2. study_data.json — so khớp mã khối thi với trang tổ hợp môn chung
# ---------------------------------------------------------------------
def check_study_entry(entry):
    url = entry.get("source_url")
    blocks = entry.get("exam_blocks", [])
    # Chỉ lấy các mã khối thi chuẩn (2 chữ + 2 số, VD A00, B08, V01) để so
    # khớp — bỏ qua các mô tả dài kèm chú thích trong ngoặc.
    codes = re.findall(r"\b[A-Z]\d{2}\b", " ".join(blocks))
    if not url or not codes:
        return entry, "skip", "không có mã khối thi chuẩn để so sánh"
    try:
        page_text = fetch_text(url)
    except requests.RequestException as err:
        return entry, "skip", f"không tải được trang ({err})"

    found = [c for c in codes if c in page_text]
    updated = {**entry, "last_checked": TODAY}
    if found:
        updated["status"] = "ok"
        return updated, "ok", f"còn thấy khối {found} trong danh sách tổ hợp môn"
    updated["status"] = "needs_review"
    return updated, "needs_review", f"không còn thấy khối {codes} trong danh sách tổ hợp môn hiện tại"


# ---------------------------------------------------------------------
# 3. automation_data.json — so khớp từ khoá với nội dung báo cáo WEF (PDF)
# ---------------------------------------------------------------------
def check_automation_entry(entry):
    url = entry.get("source_url")
    keyword = entry.get("keyword", "")
    if not url or not keyword:
        return entry, "skip", "thiếu source_url hoặc keyword"
    try:
        pdf_text = fetch_pdf_text(url).lower()
    except Exception as err:  # network, PDF lỗi, thiếu pypdf...
        return entry, "skip", f"không đọc được PDF nguồn ({err})"

    updated = {**entry, "last_checked": TODAY}
    if keyword.lower() in pdf_text:
        updated["status"] = "ok"
        return updated, "ok", f"vẫn thấy từ khoá '{keyword}' trong báo cáo"
    updated["status"] = "needs_review"
    return updated, "needs_review", f"không thấy từ khoá '{keyword}' — có thể báo cáo đã đổi bản mới"


CHECKERS = {
    "market_data.json": check_market_entry,
    "study_data.json": check_study_entry,
    "automation_data.json": check_automation_entry,
}


def main():
    any_changed = False
    for filename, checker in CHECKERS.items():
        print(f"\n=== {filename} ===")
        data = load_json(filename)
        changed = False
        for career_id, entry in data.items():
            updated_entry, status, detail = checker(entry)
            print(f"[{career_id}] {status}: {detail}")
            if updated_entry != entry:
                data[career_id] = updated_entry
                changed = True
        if changed:
            save_json(filename, data)
            any_changed = True
            print(f"-> Đã cập nhật {filename}")
        else:
            print(f"-> Không có thay đổi trong {filename}")

    if not any_changed:
        print("\nKhông có file nào cần ghi lại.")


if __name__ == "__main__":
    main()
