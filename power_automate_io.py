"""
Kết nối app với SharePoint QUA POWER AUTOMATE — không cần đăng ký Azure AD
App, không cần admin duyệt gì cả.

CÁCH HOẠT ĐỘNG
--------------
Power Automate dùng connector SharePoint có sẵn của Microsoft (chạy bằng
CHÍNH quyền tài khoản của bạn, giống hệt khi bạn tự tay sửa list trên
SharePoint) — nên không cần "Application permission" hay "Grant admin
consent" như cách dùng thẳng Graph API.

Mỗi bảng dữ liệu (Tổ chuyên môn, Giáo viên, Lớp học...) cần 1 Flow trên
Power Automate với trigger "When a HTTP request is received". App chỉ
cần gọi đúng URL webhook mà Flow đó cung cấp — y hệt gọi 1 API bình
thường bằng `requests`, không cần thư viện Microsoft Graph/Azure AD gì.

CẦN CHUẨN BỊ TRƯỚC: xem hướng dẫn dựng Flow chi tiết trong README.md
(mục "Tích hợp qua Power Automate").

Khai báo URL webhook của từng bảng vào `.streamlit/secrets.toml`:

    [power_automate]
    departments = "https://prod-xx.westus.logic.azure.com:443/workflows/.../invoke?..."
    teachers = "..."
    classes = "..."
    rooms = "..."
    activities = "..."
    grade_times = "..."
    grade_day_periods = "..."
    exam_students = "..."
    exam_rooms = "..."
    exam_subjects = "..."

Bảng nào chưa có URL thì chỉ đơn giản là chưa dùng được nút đồng bộ cho
bảng đó — không ảnh hưởng các bảng khác hay phần còn lại của app.
"""

from __future__ import annotations

import pandas as pd
import requests
import streamlit as st

BANG_KEYS = [
    "departments", "teachers", "classes", "rooms", "activities",
    "grade_times", "grade_day_periods",
    "exam_students", "exam_rooms", "exam_subjects",
]

# Cột hệ thống SharePoint hay tự thêm vào khi trả về nguyên item — bỏ đi
# cho gọn, không phải cột dữ liệu thật của app.
_COT_HE_THONG = {
    "@odata.etag", "ItemInternalId", "ID", "Id", "Modified", "Created",
    "AuthorId", "EditorId", "OData__UIVersionString", "Attachments",
    "GUID", "ContentTypeId", "ComplianceAssetId", "Author", "Editor",
    "_UIVersionString", "Title",
}


def da_cau_hinh(state_key: str) -> bool:
    try:
        cfg = st.secrets.get("power_automate")
    except Exception:
        return False
    return bool(cfg) and state_key in cfg and bool(str(cfg[state_key]).strip())


def _url(state_key: str) -> str:
    return st.secrets["power_automate"][state_key]


def tai_bang(state_key: str) -> pd.DataFrame:
    """Gọi Flow với action='load', trả về DataFrame từ danh sách item
    Flow đọc được trên SharePoint."""
    resp = requests.post(_url(state_key), json={"action": "load"}, timeout=30)
    resp.raise_for_status()
    ket_qua = resp.json()
    items = ket_qua.get("items", [])
    if not items:
        return pd.DataFrame()
    df = pd.DataFrame(items)
    return df.drop(columns=[c for c in df.columns if c in _COT_HE_THONG], errors="ignore")


def luu_bang(state_key: str, df: pd.DataFrame) -> int:
    """Gọi Flow với action='save' kèm toàn bộ dữ liệu — Flow sẽ tự xoá
    hết item cũ và thêm lại theo dữ liệu này (xem thiết kế Flow trong
    README.md)."""
    hang = df.fillna("").to_dict(orient="records")
    resp = requests.post(
        _url(state_key), json={"action": "save", "data": hang}, timeout=60,
    )
    resp.raise_for_status()
    ket_qua = resp.json()
    return int(ket_qua.get("count", len(hang)))


def power_automate_io_row(state_key: str, nhan_hien_thi: str) -> None:
    """Vẽ 1 hàng 2 nút Tải/Lưu qua Power Automate cho 1 bảng dữ liệu."""
    if not da_cau_hinh(state_key):
        st.caption(
            "🔗 Chưa khai báo URL Power Automate cho bảng này trong secrets.toml "
            "— xem hướng dẫn trong README.md."
        )
        return

    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            "📥 Tải qua Power Automate",
            key=f"pa_load_{state_key}", use_container_width=True,
        ):
            try:
                with st.spinner(f"Đang tải '{nhan_hien_thi}' qua Power Automate..."):
                    df_moi = tai_bang(state_key)
                if df_moi.empty:
                    st.warning("Chưa có dữ liệu trên SharePoint (hoặc list đang trống).")
                else:
                    st.session_state[state_key] = df_moi
                    st.success(f"✅ Đã tải {len(df_moi)} dòng.")
                    st.rerun()
            except Exception as e:
                st.error(f"Lỗi gọi Power Automate: {e}")
    with c2:
        if st.button(
            "📤 Lưu qua Power Automate",
            key=f"pa_save_{state_key}", use_container_width=True,
        ):
            try:
                with st.spinner(f"Đang lưu '{nhan_hien_thi}' qua Power Automate..."):
                    so_dong = luu_bang(state_key, st.session_state[state_key])
                st.success(f"✅ Đã lưu {so_dong} dòng.")
            except Exception as e:
                st.error(f"Lỗi gọi Power Automate: {e}")
