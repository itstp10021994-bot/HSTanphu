"""
Kết nối app với SharePoint Online để LƯU TRỮ BỀN VỮNG thay vì chỉ nằm
tạm trong session_state (mất khi đóng trình duyệt / hết phiên).

CÁCH HOẠT ĐỘNG
--------------
Dùng thư viện `Office365-REST-Python-Client`, xác thực kiểu APP-ONLY qua
Azure AD App Registration (Tenant ID + Client ID + Client Secret) — không
cần ai đăng nhập tài khoản cá nhân, phù hợp cho 1 app chạy nền như
Streamlit.

CẦN CHUẨN BỊ TRƯỚC (xem hướng dẫn đầy đủ trong README.md):
1. Đăng ký 1 "App Registration" trên Azure AD (portal.azure.com), cấp
   quyền API "Sites.ReadWrite.All" (SharePoint) kiểu Application
   permission, admin duyệt (Grant admin consent).
2. Tạo 1 Client Secret cho app đó.
3. Trên site SharePoint, tạo các List với đúng tên cột NỘI BỘ (internal
   name) bằng tiếng Anh không dấu như liệt kê trong DANH_SACH_BANG bên
   dưới — SharePoint tự mã hoá lại tên cột có dấu tiếng Việt thành chuỗi
   khó đoán, nên bắt buộc đặt tên cột bằng tiếng Anh khi tạo, sau đó có
   thể đổi lại "tên hiển thị" (display name) tiếng Việt thoải mái mà
   không ảnh hưởng gì (tên nội bộ giữ nguyên).
4. Khai báo thông tin kết nối vào `.streamlit/secrets.toml`:

    [sharepoint]
    site_url = "https://<tenant>.sharepoint.com/sites/<TenSite>"
    tenant_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    client_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    client_secret = "..."

LƯU Ý: code này viết đúng theo API chuẩn của Office365-REST-Python-Client
nhưng CHƯA test được với 1 tenant SharePoint thật (môi trường viết code
không có mạng ra ngoài) — cần bạn tự kiểm tra kỹ khi dùng lần đầu, có lỗi
gửi lại thông báo đầy đủ để chỉnh tiếp.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------
# Khai báo ánh xạ: mỗi bảng dữ liệu trong app <-> 1 SharePoint List.
# "columns" ánh xạ: {tên cột tiếng Việt trong app -> tên cột NỘI BỘ
# (internal name) tiếng Anh trên SharePoint, KHÔNG DẤU, không khoảng
# trắng} — tự tạo List với đúng các tên cột nội bộ này.
# ---------------------------------------------------------------------
DANH_SACH_BANG = {
    "departments": {
        "list_name": "ToChuyenMon",
        "columns": {"Tên tổ": "TenTo"},
    },
    "teachers": {
        "list_name": "GiaoVien",
        "columns": {"Tên giáo viên": "TenGV", "Tổ chuyên môn": "ToChuyenMon"},
    },
    "classes": {
        "list_name": "LopHoc",
        "columns": {"Tên lớp": "TenLop", "Khối": "Khoi", "Nhóm thứ tự": "NhomThuTu"},
    },
    "rooms": {
        "list_name": "PhongDacBiet",
        "columns": {
            "Tên phòng": "TenPhong", "Loại phòng": "LoaiPhong",
            "Số phòng cùng loại": "SoPhongCungLoai",
        },
    },
    "activities": {
        "list_name": "MonHocPhanCong",
        "columns": {
            "Tên hoạt động": "TenHoatDong", "Môn": "Mon", "Số tiết/tuần": "SoTietTuan",
            "Lớp": "Lop", "GV chính": "GVChinh", "GV phụ (đồng giảng)": "GVPhu",
            "Loại phòng cần": "LoaiPhongCan", "Mã đồng bộ (CLB/tự chọn)": "MaDongBo",
            "Cố định trước (Thứ:Tiết,...)": "CoDinhTruoc",
        },
    },
    "grade_times": {
        "list_name": "GioHocTheoKhoi",
        "columns": {
            "Khối": "Khoi", "Tiết": "Tiet",
            "Giờ bắt đầu": "GioBatDau", "Giờ kết thúc": "GioKetThuc",
        },
    },
    "grade_day_periods": {
        "list_name": "SoTietTheoKhoiNgay",
        "columns": {"Khối": "Khoi", "Thứ": "Thu", "Số tiết": "SoTiet"},
    },
    "exam_students": {
        "list_name": "DanhSachHocSinhThi",
        "columns": {
            "Mã HS (không bắt buộc)": "MaHS", "Họ và tên": "HoTen", "Lớp": "Lop",
        },
    },
    "exam_rooms": {
        "list_name": "DanhSachPhongThi",
        "columns": {
            "Tên phòng": "TenPhong", "Sức chứa": "SucChua", "Số cột bàn": "SoCotBan",
        },
    },
    "exam_subjects": {
        "list_name": "MonThi",
        "columns": {
            "Môn thi": "MonThi", "Lớp áp dụng": "LopApDung", "Ngày thi": "NgayThi",
            "Ca thi": "CaThi", "Chế độ xếp": "CheDoXep",
        },
    },
}


def da_cau_hinh() -> bool:
    """True nếu đã khai báo đủ thông tin kết nối SharePoint trong secrets."""
    try:
        cfg = st.secrets.get("sharepoint")
    except Exception:
        return False
    if not cfg:
        return False
    return all(k in cfg for k in ("site_url", "tenant_id", "client_id", "client_secret"))


@st.cache_resource(show_spinner=False)
def _lay_context():
    from office365.sharepoint.client_context import ClientContext
    from office365.runtime.auth.client_credential import ClientCredential

    cfg = st.secrets["sharepoint"]
    creds = ClientCredential(cfg["client_id"], cfg["client_secret"])
    ctx = ClientContext(cfg["site_url"]).with_credentials(creds)
    return ctx


def tai_bang(state_key: str) -> pd.DataFrame:
    """Đọc 1 SharePoint List, trả về DataFrame với TÊN CỘT TIẾNG VIỆT
    đúng như app đang dùng (tự map ngược từ tên cột nội bộ)."""
    thong_tin = DANH_SACH_BANG[state_key]
    ten_list = thong_tin["list_name"]
    cot_map = thong_tin["columns"]  # việt -> nội bộ
    cot_map_nguoc = {v: k for k, v in cot_map.items()}  # nội bộ -> việt

    ctx = _lay_context()
    list_obj = ctx.web.lists.get_by_title(ten_list)
    items = list_obj.items.get_all().execute_query()

    hang = []
    for item in items:
        dong = {}
        for cot_noi_bo, cot_viet in cot_map_nguoc.items():
            dong[cot_viet] = item.properties.get(cot_noi_bo, "")
        hang.append(dong)

    if not hang:
        return pd.DataFrame(columns=list(cot_map.keys()))
    return pd.DataFrame(hang)


def luu_bang(state_key: str, df: pd.DataFrame) -> int:
    """Ghi đè toàn bộ 1 SharePoint List bằng nội dung DataFrame hiện tại
    (xoá hết item cũ rồi thêm lại) — đơn giản, phù hợp quy mô dữ liệu
    trường học (vài trăm dòng/bảng). Trả về số dòng đã ghi."""
    thong_tin = DANH_SACH_BANG[state_key]
    ten_list = thong_tin["list_name"]
    cot_map = thong_tin["columns"]  # việt -> nội bộ

    ctx = _lay_context()
    list_obj = ctx.web.lists.get_by_title(ten_list)

    items_cu = list_obj.items.get_all().execute_query()
    for item in items_cu:
        item.delete_object()
    if items_cu:
        ctx.execute_batch()

    so_dong = 0
    for _, row in df.iterrows():
        du_lieu_noi_bo = {}
        for cot_viet, cot_noi_bo in cot_map.items():
            gia_tri = row.get(cot_viet, "")
            if pd.isna(gia_tri):
                gia_tri = ""
            du_lieu_noi_bo[cot_noi_bo] = gia_tri
        list_obj.add_item(du_lieu_noi_bo)
        so_dong += 1
    if so_dong:
        ctx.execute_batch()

    return so_dong


def sharepoint_io_row(state_key: str, nhan_hien_thi: str) -> None:
    """Vẽ 1 hàng 2 nút '📥 Tải từ SharePoint' / '📤 Lưu lên SharePoint'
    cho 1 bảng dữ liệu. Nếu chưa cấu hình secrets thì chỉ hiện ghi chú
    ngắn, không hiện nút (tránh lỗi khi bấm vào)."""
    if not da_cau_hinh():
        st.caption(
            "☁️ Chưa cấu hình kết nối SharePoint cho phần này — xem hướng dẫn "
            "trong README.md (mục Tích hợp SharePoint)."
        )
        return

    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            f"📥 Tải từ SharePoint",
            key=f"sp_load_{state_key}", use_container_width=True,
        ):
            try:
                with st.spinner(f"Đang tải '{nhan_hien_thi}' từ SharePoint..."):
                    df_moi = tai_bang(state_key)
                if df_moi.empty:
                    st.warning("List trên SharePoint đang trống hoặc chưa có dữ liệu.")
                else:
                    st.session_state[state_key] = df_moi
                    st.success(f"✅ Đã tải {len(df_moi)} dòng từ SharePoint.")
                    st.rerun()
            except Exception as e:
                st.error(f"Lỗi tải từ SharePoint: {e}")
    with c2:
        if st.button(
            f"📤 Lưu lên SharePoint",
            key=f"sp_save_{state_key}", use_container_width=True,
        ):
            try:
                with st.spinner(f"Đang lưu '{nhan_hien_thi}' lên SharePoint..."):
                    so_dong = luu_bang(state_key, st.session_state[state_key])
                st.success(f"✅ Đã lưu {so_dong} dòng lên SharePoint.")
            except Exception as e:
                st.error(f"Lỗi lưu lên SharePoint: {e}")
