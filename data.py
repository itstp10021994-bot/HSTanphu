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
    {
        "id": "teacher",
        "name": "Giáo viên",
        "icon": "📚",
        "color": "#93C5FD",
        "tagline": "Truyền đạt kiến thức và truyền cảm hứng học tập",
        "description": (
            "Giáo viên cần khả năng giao tiếp tốt để truyền đạt kiến thức dễ "
            "hiểu, sự kiên nhẫn khi học sinh chưa nắm bài, và một chút sáng "
            "tạo để tiết học không nhàm chán."
        ),
    },
    {
        "id": "civil",
        "name": "Kỹ sư xây dựng",
        "icon": "🏗️",
        "color": "#FDBA74",
        "tagline": "Biến bản vẽ thành công trình vững chắc",
        "description": (
            "Kỹ sư xây dựng phải tuân thủ nghiêm ngặt quy trình kỹ thuật — "
            "sai một bước trong thi công móng có thể ảnh hưởng đến cả công "
            "trình về sau."
        ),
    },
    {
        "id": "lawyer",
        "name": "Luật sư",
        "icon": "⚖️",
        "color": "#C4B5FD",
        "tagline": "Bảo vệ lẽ phải bằng lập luận chặt chẽ",
        "description": (
            "Luật sư cần tư duy logic để xây dựng lập luận, và khả năng "
            "giao tiếp thuyết phục để trình bày trước toà và trao đổi với "
            "thân chủ."
        ),
    },
    {
        "id": "pilot",
        "name": "Phi công",
        "icon": "✈️",
        "color": "#7DD3FC",
        "tagline": "Đưa hàng trăm sinh mạng đến nơi an toàn",
        "description": (
            "Phi công phải tuân thủ tuyệt đối quy trình kiểm tra trước khi "
            "bay — không được bỏ sót hay đảo bước, vì an toàn luôn được đặt "
            "lên hàng đầu."
        ),
    },
    {
        "id": "photographer",
        "name": "Nhiếp ảnh gia",
        "icon": "📷",
        "color": "#F472B6",
        "tagline": "Lưu giữ khoảnh khắc bằng con mắt sáng tạo",
        "description": (
            "Nhiếp ảnh gia kết hợp con mắt thẩm mỹ, sự khéo léo khi thao tác "
            "thiết bị, và kỹ năng giao tiếp để hướng dẫn người được chụp."
        ),
    },
]

# Trọng số năng lực yêu cầu của mỗi ngành (dùng để gợi ý mức độ phù hợp)
CAREER_SKILL_PROFILE = {
    "dev":    {"logic": 3, "hand": 0, "creative": 1, "patience": 2, "comms": 1},
    "doctor": {"logic": 2, "hand": 1, "creative": 0, "patience": 3, "comms": 2},
    "chef":   {"logic": 0, "hand": 2, "creative": 3, "patience": 2, "comms": 1},
    "teacher":      {"logic": 1, "hand": 0, "creative": 1, "patience": 2, "comms": 3},
    "civil":        {"logic": 3, "hand": 1, "creative": 0, "patience": 2, "comms": 0},
    "lawyer":       {"logic": 3, "hand": 0, "creative": 1, "patience": 1, "comms": 3},
    "pilot":        {"logic": 3, "hand": 0, "creative": 0, "patience": 3, "comms": 1},
    "photographer": {"logic": 0, "hand": 1, "creative": 3, "patience": 1, "comms": 1},
}

# Mỗi nhiệm vụ là dạng "sequence": học sinh kéo-thả các thẻ (có icon minh
# hoạ + mô tả) về đúng thứ tự. "steps" liệt kê theo ĐÚNG thứ tự chuẩn; hệ
# thống sẽ tự xáo trộn khi hiển thị cho học sinh.
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
            {"icon": "📋", "text": "Đọc thông báo lỗi (error log) để xác định vị trí xảy ra sự cố"},
            {"icon": "💻", "text": "Tái hiện lại lỗi trên máy của mình để chắc chắn hiểu đúng vấn đề"},
            {"icon": "🔍", "text": "Thu hẹp phạm vi bằng cách kiểm tra từng đoạn code liên quan"},
            {"icon": "⏸️", "text": "Đặt điểm dừng (breakpoint) để xem giá trị biến tại thời điểm lỗi"},
            {"icon": "🛠️", "text": "Sửa đoạn code gây lỗi"},
            {"icon": "✅", "text": "Chạy lại toàn bộ kiểm thử (test) để chắc chắn không phát sinh lỗi mới"},
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
            {"icon": "📞", "text": "Kiểm tra phản ứng và gọi hỗ trợ ngay lập tức"},
            {"icon": "🌬️", "text": "Kiểm tra đường thở, khai thông nếu bị tắc nghẽn"},
            {"icon": "⏱️", "text": "Kiểm tra nhịp thở trong 10 giây"},
            {"icon": "💓", "text": "Bắt đầu ép tim ngoài lồng ngực (30 lần ép)"},
            {"icon": "💨", "text": "Hà hơi thổi ngạt (2 lần) rồi tiếp tục chu kỳ ép tim"},
            {"icon": "⚡", "text": "Gắn máy khử rung tim (AED) ngay khi có sẵn"},
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
            {"icon": "🥘", "text": "Ninh xương bò lấy nước dùng trong nhiều giờ"},
            {"icon": "🧂", "text": "Nêm nếm nước dùng với gia vị và thảo mộc đặc trưng"},
            {"icon": "🍜", "text": "Trụng bánh phở qua nước sôi"},
            {"icon": "🥩", "text": "Xếp thịt bò tái thái mỏng lên trên bánh phở"},
            {"icon": "♨️", "text": "Chan nước dùng nóng để làm chín thịt"},
            {"icon": "🌿", "text": "Trang trí với hành lá, rau thơm trước khi phục vụ"},
        ],
        "skill_weight": {"creative": 3, "hand": 2, "patience": 1},
    },
    {
        "id": "teacher-lesson",
        "career_id": "teacher",
        "title": "Dạy một tiết Toán lớp 6",
        "story": (
            "Bạn có 45 phút để dạy học sinh lớp 6 về phân số. Hãy sắp xếp "
            "đúng trình tự một tiết dạy hiệu quả."
        ),
        "steps": [
            {"icon": "📝", "text": "Soạn giáo án và xác định mục tiêu bài học"},
            {"icon": "📐", "text": "Chuẩn bị đồ dùng dạy học trực quan"},
            {"icon": "🔔", "text": "Ổn định lớp và kiểm tra bài cũ"},
            {"icon": "🗣️", "text": "Giảng bài theo giáo án đã chuẩn bị"},
            {"icon": "❓", "text": "Đặt câu hỏi để kiểm tra học sinh có hiểu bài không"},
            {"icon": "📚", "text": "Giao bài tập về nhà và tổng kết tiết học"},
        ],
        "skill_weight": {"comms": 3, "patience": 2, "creative": 1},
    },
    {
        "id": "civil-foundation",
        "career_id": "civil",
        "title": "Giám sát thi công móng nhà",
        "story": (
            "Một công trình nhà ở chuẩn bị đổ móng. Hãy sắp xếp đúng trình "
            "tự thi công để đảm bảo móng nhà vững chắc."
        ),
        "steps": [
            {"icon": "🧭", "text": "Khảo sát địa chất khu đất"},
            {"icon": "📐", "text": "Thiết kế bản vẽ kết cấu móng"},
            {"icon": "⛏️", "text": "Đào đất theo đúng bản vẽ"},
            {"icon": "🏗️", "text": "Lắp đặt cốt thép móng"},
            {"icon": "🧱", "text": "Đổ bê tông móng"},
            {"icon": "💧", "text": "Bảo dưỡng bê tông trước khi thi công tiếp"},
        ],
        "skill_weight": {"logic": 3, "patience": 2, "hand": 1},
    },
    {
        "id": "lawyer-case",
        "career_id": "lawyer",
        "title": "Chuẩn bị bào chữa cho một vụ kiện",
        "story": (
            "Một thân chủ nhờ bạn bào chữa trong một vụ tranh chấp hợp đồng. "
            "Hãy sắp xếp đúng trình tự các bước chuẩn bị."
        ),
        "steps": [
            {"icon": "📁", "text": "Tiếp nhận hồ sơ và tình tiết vụ việc từ thân chủ"},
            {"icon": "📖", "text": "Nghiên cứu các điều luật liên quan"},
            {"icon": "🔎", "text": "Thu thập và rà soát chứng cứ"},
            {"icon": "✍️", "text": "Soạn thảo luận cứ bào chữa"},
            {"icon": "🗣️", "text": "Trao đổi với thân chủ về chiến lược bào chữa"},
            {"icon": "⚖️", "text": "Trình bày luận cứ bào chữa tại phiên toà"},
        ],
        "skill_weight": {"logic": 3, "comms": 3, "creative": 1},
    },
    {
        "id": "pilot-preflight",
        "career_id": "pilot",
        "title": "Quy trình trước khi cất cánh",
        "story": (
            "Chuyến bay của bạn chuẩn bị khởi hành. Hãy sắp xếp đúng trình "
            "tự các bước kiểm tra bắt buộc trước khi cất cánh."
        ),
        "steps": [
            {"icon": "🌦️", "text": "Kiểm tra thời tiết và lộ trình bay"},
            {"icon": "🔧", "text": "Kiểm tra tình trạng kỹ thuật máy bay"},
            {"icon": "📡", "text": "Xin phép đài kiểm soát không lưu"},
            {"icon": "🦺", "text": "Hướng dẫn an toàn cho hành khách"},
            {"icon": "⚙️", "text": "Khởi động động cơ theo checklist"},
            {"icon": "🛫", "text": "Cất cánh theo đường băng được chỉ định"},
        ],
        "skill_weight": {"patience": 3, "logic": 3, "comms": 1},
    },
    {
        "id": "photo-wedding",
        "career_id": "photographer",
        "title": "Chụp ảnh cưới ngoại cảnh",
        "story": (
            "Bạn nhận chụp bộ ảnh cưới ngoại cảnh cho một cặp đôi. Hãy sắp "
            "xếp đúng trình tự một buổi chụp chuyên nghiệp."
        ),
        "steps": [
            {"icon": "🌅", "text": "Khảo sát địa điểm và điều kiện ánh sáng"},
            {"icon": "💡", "text": "Lên ý tưởng concept cho bộ ảnh"},
            {"icon": "📷", "text": "Chuẩn bị và kiểm tra thiết bị chụp"},
            {"icon": "🤝", "text": "Hướng dẫn dáng chụp cho cô dâu chú rể"},
            {"icon": "📸", "text": "Chụp và kiểm tra ảnh ngay tại chỗ"},
            {"icon": "🖥️", "text": "Hậu kỳ chỉnh sửa ảnh trước khi bàn giao"},
        ],
        "skill_weight": {"creative": 3, "comms": 1, "patience": 1},
    },
]
