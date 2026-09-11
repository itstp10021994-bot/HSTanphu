# -*- coding: utf-8 -*-
"""
Dữ liệu mẫu (seed data) cho ứng dụng mô phỏng trải nghiệm nghề nghiệp.
Đây là nơi DUY NHẤT bạn cần chỉnh sửa để thêm ngành nghề / nhiệm vụ mới.

Cấu trúc mở rộng:
- Thêm 1 dict vào CAREERS
- Thêm 1 dict vào TASKS (career_id trỏ tới id ngành vừa thêm)
- (tuỳ chọn) chỉnh CAREER_SKILL_PROFILE để việc gợi ý nghề chính xác hơn
"""

SKILLS = [
    {"id": "logic", "name": "Tư duy logic"},
    {"id": "hand", "name": "Khéo léo tay chân"},
    {"id": "creative", "name": "Sáng tạo"},
    {"id": "patience", "name": "Kiên nhẫn & tỉ mỉ"},
    {"id": "comms", "name": "Giao tiếp"},
]

CAREERS = [
    {
        "id": "dev",
        "name": "Lập trình viên",
        "icon": "💻",
        "color": "#5EEAD4",
        "tagline": "Biến ý tưởng thành phần mềm chạy được",
        "description": (
            "Lập trình viên xây dựng và sửa lỗi phần mềm mỗi ngày. "
            "Công việc đòi hỏi tư duy logic chặt chẽ và sự kiên nhẫn khi "
            "một đoạn code không chạy đúng như mong đợi."
        ),
    },
    {
        "id": "doctor",
        "name": "Bác sĩ cấp cứu",
        "icon": "🩺",
        "color": "#F87171",
        "tagline": "Ra quyết định chính xác khi thời gian là sinh mạng",
        "description": (
            "Bác sĩ cấp cứu phải xử lý tình huống nguy cấp theo đúng quy "
            "trình, không được bỏ sót bước nào. Một sai sót nhỏ có thể "
            "ảnh hưởng đến tính mạng bệnh nhân."
        ),
    },
    {
        "id": "chef",
        "name": "Đầu bếp",
        "icon": "🍳",
        "color": "#FBBF24",
        "tagline": "Kết hợp nguyên liệu thành trải nghiệm vị giác",
        "description": (
            "Đầu bếp cần sự sáng tạo trong hương vị, sự khéo léo trong "
            "thao tác, và tính kỷ luật để giữ đúng quy trình chế biến."
        ),
    },
]

# Trọng số năng lực yêu cầu của mỗi ngành (dùng để gợi ý mức độ phù hợp)
CAREER_SKILL_PROFILE = {
    "dev":    {"logic": 3, "hand": 0, "creative": 1, "patience": 2, "comms": 1},
    "doctor": {"logic": 2, "hand": 1, "creative": 0, "patience": 3, "comms": 2},
    "chef":   {"logic": 0, "hand": 2, "creative": 3, "patience": 2, "comms": 1},
}

# Mỗi nhiệm vụ là dạng "sequence": học sinh kéo-thả các bước về đúng thứ tự.
# "steps" liệt kê theo ĐÚNG thứ tự chuẩn; hệ thống sẽ tự xáo trộn khi hiển thị.
TASKS = [
    {
        "id": "dev-debug",
        "career_id": "dev",
        "title": "Gỡ lỗi ứng dụng bị treo",
        "story": (
            "Ứng dụng đặt đồ ăn của công ty bạn báo lỗi và bị treo ngay khi "
            "người dùng bấm nút \"Thanh toán\". Hãy sắp xếp lại đúng quy trình "
            "gỡ lỗi (debug) mà một lập trình viên sẽ thực hiện."
        ),
        "steps": [
            "Đọc thông báo lỗi (error log) để xác định vị trí xảy ra sự cố",
            "Tái hiện lại lỗi trên máy của mình để chắc chắn hiểu đúng vấn đề",
            "Thu hẹp phạm vi bằng cách kiểm tra từng đoạn code liên quan",
            "Đặt điểm dừng (breakpoint) để xem giá trị biến tại thời điểm lỗi",
            "Sửa đoạn code gây lỗi",
            "Chạy lại toàn bộ kiểm thử (test) để chắc chắn không phát sinh lỗi mới",
        ],
        "skill_weight": {"logic": 3, "patience": 2, "creative": 1},
    },
    {
        "id": "doctor-cpr",
        "career_id": "doctor",
        "title": "Sơ cứu bệnh nhân ngưng thở",
        "story": (
            "Một bệnh nhân được đưa vào phòng cấp cứu trong tình trạng bất "
            "tỉnh, không thấy lồng ngực di chuyển. Hãy sắp xếp đúng thứ tự "
            "các bước sơ cứu ban đầu."
        ),
        "steps": [
            "Kiểm tra phản ứng và gọi hỗ trợ ngay lập tức",
            "Kiểm tra đường thở, khai thông nếu bị tắc nghẽn",
            "Kiểm tra nhịp thở trong 10 giây",
            "Bắt đầu ép tim ngoài lồng ngực (30 lần ép)",
            "Hà hơi thổi ngạt (2 lần) rồi tiếp tục chu kỳ ép tim",
            "Gắn máy khử rung tim (AED) ngay khi có sẵn",
        ],
        "skill_weight": {"patience": 3, "comms": 2, "logic": 2},
    },
    {
        "id": "chef-pho",
        "career_id": "chef",
        "title": "Chế biến một tô phở bò",
        "story": (
            "Khách hàng vừa gọi một tô phở bò tái. Hãy sắp xếp đúng trình tự "
            "các công đoạn để cho ra một tô phở chuẩn vị."
        ),
        "steps": [
            "Ninh xương bò lấy nước dùng trong nhiều giờ",
            "Nêm nếm nước dùng với gia vị và thảo mộc đặc trưng",
            "Trụng bánh phở qua nước sôi",
            "Xếp thịt bò tái thái mỏng lên trên bánh phở",
            "Chan nước dùng nóng để làm chín thịt",
            "Trang trí với hành lá, rau thơm trước khi phục vụ",
        ],
        "skill_weight": {"creative": 3, "hand": 2, "patience": 1},
    },
]
