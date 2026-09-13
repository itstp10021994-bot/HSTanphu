# -*- coding: utf-8 -*-
"""
Dữ liệu mẫu (seed data) cho ứng dụng mô phỏng trải nghiệm nghề nghiệp.
Đây là nơi DUY NHẤT bạn cần chỉnh sửa để thêm ngành nghề / nhiệm vụ mới.

Cấu trúc mở rộng:
- Thêm 1 dict vào CAREERS (nhớ gán "cluster" đúng 1 trong các id ở CLUSTERS)
- Thêm 1 dict vào TASKS (career_id trỏ tới id ngành vừa thêm)
- (tuỳ chọn) chỉnh CAREER_SKILL_PROFILE để việc gợi ý nghề chính xác hơn
- (tuỳ chọn) thêm cụm ngành mới vào CLUSTERS nếu ngành mới không thuộc
  cụm nào có sẵn
"""

# Cụm ngành nghề — hiển thị dạng tab bên trái trang chủ. Thứ tự trong danh
# sách này quyết định thứ tự tab hiển thị.
CLUSTERS = [
    {"id": "cntt", "name": "Công nghệ thông tin", "icon": "💻"},
    {"id": "yte", "name": "Y tế", "icon": "🏥"},
    {"id": "giaoduc", "name": "Giáo dục", "icon": "📚"},
    {"id": "kythuat", "name": "Kỹ thuật & Xây dựng", "icon": "🏗️"},
    {"id": "phapluat", "name": "Pháp luật & Công quyền", "icon": "⚖️"},
    {"id": "nghethuat", "name": "Nghệ thuật & Sáng tạo", "icon": "🎨"},
    {"id": "dichvu", "name": "Dịch vụ & Ẩm thực", "icon": "🍳"},
    {"id": "vantai", "name": "Giao thông & Vận tải", "icon": "✈️"},
    {"id": "kinhdoanh", "name": "Kinh doanh & Tài chính", "icon": "💰"},
    {"id": "khoahoc", "name": "Khoa học & Nghiên cứu", "icon": "🔬"},
    {"id": "nongnghiep", "name": "Nông nghiệp & Môi trường", "icon": "🌱"},
]

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
        "cluster": "cntt",
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
        "cluster": "yte",
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
        "cluster": "dichvu",
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
        "cluster": "giaoduc",
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
        "cluster": "kythuat",
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
        "cluster": "phapluat",
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
        "cluster": "vantai",
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
        "cluster": "nghethuat",
        "name": "Nhiếp ảnh gia",
        "icon": "📷",
        "color": "#F472B6",
        "tagline": "Lưu giữ khoảnh khắc bằng con mắt sáng tạo",
        "description": (
            "Nhiếp ảnh gia kết hợp con mắt thẩm mỹ, sự khéo léo khi thao tác "
            "thiết bị, và kỹ năng giao tiếp để hướng dẫn người được chụp."
        ),
    },
    {
        "id": "uxui",
        "cluster": "cntt",
        "name": "Nhà thiết kế UX/UI",
        "icon": "🖌️",
        "color": "#A78BFA",
        "tagline": "Biến ý tưởng thành giao diện dễ dùng, đẹp mắt",
        "description": (
            "Nhà thiết kế UX/UI nghiên cứu người dùng và tạo ra giao diện "
            "vừa đẹp vừa dễ sử dụng cho ứng dụng, website."
        ),
    },
    {
        "id": "nurse",
        "cluster": "yte",
        "name": "Điều dưỡng viên",
        "icon": "💉",
        "color": "#FDA4AF",
        "tagline": "Chăm sóc bệnh nhân từng giờ, đồng hành cùng bác sĩ",
        "description": (
            "Điều dưỡng viên theo dõi sát tình trạng bệnh nhân, thực hiện y "
            "lệnh của bác sĩ và là người chăm sóc bệnh nhân nhiều nhất mỗi ngày."
        ),
    },
    {
        "id": "preschool",
        "cluster": "giaoduc",
        "name": "Giáo viên mầm non",
        "icon": "🧸",
        "color": "#FCD34D",
        "tagline": "Gieo những viên gạch đầu tiên cho hành trình học tập",
        "description": (
            "Giáo viên mầm non chăm sóc và dạy dỗ trẻ nhỏ thông qua vui "
            "chơi, cần sự kiên nhẫn, yêu trẻ và khả năng sáng tạo."
        ),
    },
    {
        "id": "architect",
        "cluster": "kythuat",
        "name": "Kiến trúc sư",
        "icon": "📐",
        "color": "#FB923C",
        "tagline": "Vẽ nên không gian sống bằng cả kỹ thuật lẫn thẩm mỹ",
        "description": (
            "Kiến trúc sư thiết kế công trình vừa đẹp vừa đảm bảo công "
            "năng, làm việc chặt chẽ với khách hàng và kỹ sư xây dựng."
        ),
    },
    {
        "id": "police",
        "cluster": "phapluat",
        "name": "Cảnh sát điều tra",
        "icon": "🚓",
        "color": "#60A5FA",
        "tagline": "Tìm ra sự thật đằng sau mỗi vụ án",
        "description": (
            "Cảnh sát điều tra thu thập chứng cứ, phân tích tình tiết để "
            "tìm ra sự thật và đưa người phạm tội ra trước pháp luật."
        ),
    },
    {
        "id": "musician",
        "cluster": "nghethuat",
        "name": "Nhạc sĩ",
        "icon": "🎵",
        "color": "#F0ABFC",
        "tagline": "Kể chuyện bằng giai điệu và âm thanh",
        "description": (
            "Nhạc sĩ sáng tác giai điệu, lời ca để truyền tải cảm xúc và "
            "câu chuyện đến người nghe."
        ),
    },
    {
        "id": "tourguide",
        "cluster": "dichvu",
        "name": "Hướng dẫn viên du lịch",
        "icon": "🧳",
        "color": "#6EE7B7",
        "tagline": "Đưa du khách khám phá những vùng đất mới",
        "description": (
            "Hướng dẫn viên du lịch dẫn dắt và chăm sóc đoàn khách suốt "
            "hành trình, cần vốn hiểu biết rộng và kỹ năng giao tiếp tốt."
        ),
    },
    {
        "id": "cybersecurity",
        "cluster": "cntt",
        "name": "Chuyên viên an ninh mạng",
        "icon": "🔐",
        "color": "#38BDF8",
        "tagline": "Bảo vệ hệ thống khỏi những cuộc tấn công vô hình",
        "description": (
            "Chuyên viên an ninh mạng phát hiện lỗ hổng và bảo vệ hệ "
            "thống, dữ liệu của tổ chức khỏi các cuộc tấn công mạng."
        ),
    },
    {
        "id": "pharmacist",
        "cluster": "yte",
        "name": "Dược sĩ",
        "icon": "💊",
        "color": "#4ADE80",
        "tagline": "Đảm bảo mỗi viên thuốc đến đúng người, đúng liều",
        "description": (
            "Dược sĩ tư vấn và cấp phát thuốc đúng chỉ định, giúp người "
            "bệnh sử dụng thuốc an toàn và hiệu quả."
        ),
    },
    {
        "id": "electrical",
        "cluster": "kythuat",
        "name": "Kỹ sư điện",
        "icon": "🔌",
        "color": "#FACC15",
        "tagline": "Đưa dòng điện an toàn đến từng công trình",
        "description": (
            "Kỹ sư điện thiết kế và lắp đặt hệ thống điện cho công trình, "
            "đảm bảo an toàn và đúng tiêu chuẩn kỹ thuật."
        ),
    },
    {
        "id": "actor",
        "cluster": "nghethuat",
        "name": "Diễn viên",
        "icon": "🎭",
        "color": "#FB7185",
        "tagline": "Hoá thân vào nhân vật để kể chuyện bằng cảm xúc",
        "description": (
            "Diễn viên truyền tải câu chuyện và cảm xúc nhân vật đến khán "
            "giả thông qua biểu cảm, giọng nói và hành động."
        ),
    },
    {
        "id": "hotelmanager",
        "cluster": "dichvu",
        "name": "Quản lý khách sạn",
        "icon": "🏨",
        "color": "#2DD4BF",
        "tagline": "Mang lại trải nghiệm lưu trú hoàn hảo cho từng vị khách",
        "description": (
            "Quản lý khách sạn điều phối toàn bộ hoạt động để đảm bảo "
            "khách hàng có trải nghiệm lưu trú tốt nhất."
        ),
    },
    {
        "id": "captain",
        "cluster": "vantai",
        "name": "Thuyền trưởng",
        "icon": "🚢",
        "color": "#0EA5E9",
        "tagline": "Chỉ huy con tàu vượt qua mọi vùng biển",
        "description": (
            "Thuyền trưởng chịu trách nhiệm điều khiển tàu và đảm bảo an "
            "toàn cho toàn bộ thuyền viên, hàng hoá trên tàu."
        ),
    },
    {
        "id": "marketing",
        "cluster": "kinhdoanh",
        "name": "Chuyên viên Marketing",
        "icon": "📣",
        "color": "#F97316",
        "tagline": "Đưa sản phẩm đến đúng người, đúng thời điểm",
        "description": (
            "Chuyên viên marketing xây dựng chiến lược quảng bá để sản "
            "phẩm hoặc thương hiệu tiếp cận đúng khách hàng mục tiêu."
        ),
    },
    {
        "id": "accountant",
        "cluster": "kinhdoanh",
        "name": "Kế toán viên",
        "icon": "🧾",
        "color": "#A3E635",
        "tagline": "Giữ cho từng con số của doanh nghiệp luôn chính xác",
        "description": (
            "Kế toán viên ghi chép, kiểm soát và báo cáo tình hình tài "
            "chính, giúp doanh nghiệp hoạt động minh bạch, đúng quy định."
        ),
    },
    {
        "id": "scientist",
        "cluster": "khoahoc",
        "name": "Nhà nghiên cứu khoa học",
        "icon": "🔬",
        "color": "#818CF8",
        "tagline": "Đi tìm câu trả lời cho những câu hỏi chưa ai giải được",
        "description": (
            "Nhà nghiên cứu khoa học thực hiện thí nghiệm, phân tích dữ "
            "liệu để tìm ra tri thức mới, đóng góp cho khoa học."
        ),
    },
    {
        "id": "agriculture",
        "cluster": "nongnghiep",
        "name": "Kỹ sư nông nghiệp",
        "icon": "🌾",
        "color": "#65A30D",
        "tagline": "Ứng dụng khoa học để cây trồng cho năng suất tốt hơn",
        "description": (
            "Kỹ sư nông nghiệp nghiên cứu và áp dụng kỹ thuật canh tác để "
            "nâng cao năng suất, chất lượng cây trồng bền vững."
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
    "uxui":       {"logic": 1, "hand": 0, "creative": 3, "patience": 1, "comms": 2},
    "nurse":      {"logic": 1, "hand": 2, "creative": 0, "patience": 3, "comms": 2},
    "preschool":  {"logic": 0, "hand": 1, "creative": 2, "patience": 3, "comms": 2},
    "architect":  {"logic": 2, "hand": 0, "creative": 3, "patience": 1, "comms": 2},
    "police":     {"logic": 3, "hand": 0, "creative": 1, "patience": 2, "comms": 2},
    "musician":   {"logic": 0, "hand": 1, "creative": 3, "patience": 2, "comms": 1},
    "tourguide":  {"logic": 0, "hand": 0, "creative": 1, "patience": 2, "comms": 3},
    "cybersecurity": {"logic": 3, "hand": 0, "creative": 1, "patience": 2, "comms": 1},
    "pharmacist":    {"logic": 2, "hand": 1, "creative": 0, "patience": 3, "comms": 2},
    "electrical":    {"logic": 3, "hand": 2, "creative": 0, "patience": 2, "comms": 0},
    "actor":         {"logic": 0, "hand": 0, "creative": 3, "patience": 2, "comms": 2},
    "hotelmanager":  {"logic": 1, "hand": 0, "creative": 1, "patience": 2, "comms": 3},
    "captain":       {"logic": 2, "hand": 0, "creative": 0, "patience": 3, "comms": 2},
    "marketing":     {"logic": 1, "hand": 0, "creative": 3, "patience": 1, "comms": 2},
    "accountant":    {"logic": 3, "hand": 0, "creative": 0, "patience": 3, "comms": 1},
    "scientist":     {"logic": 3, "hand": 1, "creative": 2, "patience": 3, "comms": 1},
    "agriculture":   {"logic": 2, "hand": 2, "creative": 1, "patience": 3, "comms": 1},
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
    {
        "id": "uxui-app",
        "career_id": "uxui",
        "title": "Thiết kế lại giao diện app đặt đồ ăn",
        "story": (
            "Một startup nhờ bạn thiết kế lại giao diện app đặt đồ ăn vì "
            "người dùng phàn nàn khó thao tác. Hãy sắp xếp đúng quy trình "
            "thiết kế UX/UI chuẩn."
        ),
        "steps": [
            {"icon": "🔎", "text": "Nghiên cứu và phỏng vấn người dùng để hiểu vấn đề họ gặp phải"},
            {"icon": "🗺️", "text": "Vẽ sơ đồ luồng thao tác (user flow) tổng thể"},
            {"icon": "✏️", "text": "Phác thảo wireframe các màn hình chính"},
            {"icon": "🎨", "text": "Thiết kế giao diện chi tiết (màu sắc, font, bố cục)"},
            {"icon": "🧪", "text": "Kiểm thử với người dùng thật trên bản mẫu (prototype)"},
            {"icon": "🔄", "text": "Chỉnh sửa theo phản hồi trước khi bàn giao cho lập trình viên"},
        ],
        "skill_weight": {"creative": 3, "comms": 2, "patience": 1},
    },
    {
        "id": "nurse-postop",
        "career_id": "nurse",
        "title": "Chăm sóc bệnh nhân sau phẫu thuật",
        "story": (
            "Một bệnh nhân vừa mổ xong được chuyển về phòng hồi sức. Hãy "
            "sắp xếp đúng quy trình chăm sóc ban đầu của điều dưỡng."
        ),
        "steps": [
            {"icon": "📋", "text": "Đọc hồ sơ bệnh án và y lệnh của bác sĩ"},
            {"icon": "🌡️", "text": "Đo các chỉ số sinh tồn (nhiệt độ, huyết áp, mạch)"},
            {"icon": "💊", "text": "Cho bệnh nhân uống/tiêm thuốc theo đúng y lệnh"},
            {"icon": "🛏️", "text": "Hỗ trợ bệnh nhân thay đổi tư thế để tránh loét"},
            {"icon": "📝", "text": "Ghi chép lại tình trạng bệnh nhân vào hồ sơ theo dõi"},
            {"icon": "🔔", "text": "Báo ngay cho bác sĩ nếu phát hiện dấu hiệu bất thường"},
        ],
        "skill_weight": {"patience": 3, "comms": 2, "hand": 1},
    },
    {
        "id": "preschool-activity",
        "career_id": "preschool",
        "title": "Tổ chức hoạt động vui chơi cho lớp mầm non",
        "story": (
            "Hôm nay lớp bạn có 20 bé 4 tuổi. Hãy sắp xếp đúng trình tự tổ "
            "chức một hoạt động vui chơi kết hợp học tập."
        ),
        "steps": [
            {"icon": "🧩", "text": "Lên kế hoạch hoạt động phù hợp độ tuổi"},
            {"icon": "🎈", "text": "Chuẩn bị đồ chơi, dụng cụ học tập"},
            {"icon": "🙋", "text": "Tập hợp và ổn định các bé trước khi bắt đầu"},
            {"icon": "🎭", "text": "Hướng dẫn và cùng bé tham gia hoạt động"},
            {"icon": "👀", "text": "Quan sát, hỗ trợ từng bé trong lúc chơi"},
            {"icon": "🧹", "text": "Cùng bé dọn dẹp và tổng kết sau hoạt động"},
        ],
        "skill_weight": {"patience": 3, "creative": 2, "comms": 1},
    },
    {
        "id": "architect-house",
        "career_id": "architect",
        "title": "Thiết kế một ngôi nhà phố cho khách hàng",
        "story": (
            "Một gia đình nhờ bạn thiết kế ngôi nhà phố 4 tầng. Hãy sắp "
            "xếp đúng quy trình thiết kế kiến trúc."
        ),
        "steps": [
            {"icon": "🗣️", "text": "Trao đổi với khách hàng về nhu cầu và ngân sách"},
            {"icon": "📏", "text": "Khảo sát hiện trạng khu đất"},
            {"icon": "✏️", "text": "Phác thảo ý tưởng mặt bằng công năng"},
            {"icon": "🖥️", "text": "Dựng bản vẽ 3D và phối cảnh"},
            {"icon": "🔧", "text": "Điều chỉnh thiết kế theo yêu cầu kỹ thuật kết cấu"},
            {"icon": "📁", "text": "Hoàn thiện hồ sơ bản vẽ để xin giấy phép xây dựng"},
        ],
        "skill_weight": {"creative": 3, "comms": 1, "logic": 1},
    },
    {
        "id": "police-investigation",
        "career_id": "police",
        "title": "Điều tra một vụ trộm đột nhập",
        "story": (
            "Một cửa hàng báo mất trộm vào ban đêm. Hãy sắp xếp đúng trình "
            "tự điều tra hiện trường ban đầu."
        ),
        "steps": [
            {"icon": "🚧", "text": "Phong toả và bảo vệ hiện trường"},
            {"icon": "📸", "text": "Chụp ảnh, ghi nhận hiện trạng hiện trường"},
            {"icon": "🔍", "text": "Thu thập dấu vết, vật chứng tại chỗ"},
            {"icon": "🗣️", "text": "Lấy lời khai nhân chứng, chủ cửa hàng"},
            {"icon": "🧠", "text": "Phân tích, đối chiếu các manh mối thu được"},
            {"icon": "📄", "text": "Lập báo cáo và đề xuất hướng điều tra tiếp theo"},
        ],
        "skill_weight": {"logic": 3, "patience": 2, "comms": 1},
    },
    {
        "id": "musician-song",
        "career_id": "musician",
        "title": "Sáng tác một bài hát mới",
        "story": (
            "Một ca sĩ trẻ nhờ bạn sáng tác một bài hát cho album đầu tay. "
            "Hãy sắp xếp đúng trình tự sáng tác."
        ),
        "steps": [
            {"icon": "💡", "text": "Tìm cảm hứng và chủ đề cho bài hát"},
            {"icon": "🎼", "text": "Viết giai điệu chính (melody)"},
            {"icon": "✍️", "text": "Viết lời bài hát khớp với giai điệu"},
            {"icon": "🎹", "text": "Phối khí (hoà âm) cho bài hát"},
            {"icon": "🎤", "text": "Thu âm thử và điều chỉnh"},
            {"icon": "🎧", "text": "Mix, master hoàn thiện bản thu"},
        ],
        "skill_weight": {"creative": 3, "patience": 2, "hand": 1},
    },
    {
        "id": "tourguide-tour",
        "career_id": "tourguide",
        "title": "Dẫn một tour du lịch trong ngày",
        "story": (
            "Bạn phụ trách dẫn một đoàn 20 khách tham quan trong ngày. Hãy "
            "sắp xếp đúng trình tự công việc của hướng dẫn viên."
        ),
        "steps": [
            {"icon": "📋", "text": "Kiểm tra lịch trình và chuẩn bị thông tin điểm đến"},
            {"icon": "🙋", "text": "Đón và tập hợp đoàn khách tại điểm hẹn"},
            {"icon": "🗣️", "text": "Giới thiệu lịch trình và các lưu ý an toàn"},
            {"icon": "🏛️", "text": "Thuyết minh tại từng điểm tham quan"},
            {"icon": "🍽️", "text": "Sắp xếp giờ ăn uống, nghỉ ngơi hợp lý cho đoàn"},
            {"icon": "👋", "text": "Tổng kết chuyến đi và tiễn khách"},
        ],
        "skill_weight": {"comms": 3, "patience": 2, "creative": 1},
    },
    {
        "id": "cybersecurity-incident",
        "career_id": "cybersecurity",
        "title": "Xử lý một cuộc tấn công mạng vào hệ thống công ty",
        "story": (
            "Hệ thống công ty bạn vừa bị phát hiện có dấu hiệu bị xâm "
            "nhập. Hãy sắp xếp đúng quy trình xử lý sự cố an ninh mạng."
        ),
        "steps": [
            {"icon": "🚨", "text": "Xác nhận và phân loại mức độ nghiêm trọng của sự cố"},
            {"icon": "🔌", "text": "Cô lập hệ thống bị ảnh hưởng để ngăn lây lan"},
            {"icon": "🔍", "text": "Điều tra nguồn gốc và cách thức tấn công"},
            {"icon": "🛡️", "text": "Vá lỗ hổng bảo mật đã bị khai thác"},
            {"icon": "💾", "text": "Khôi phục dữ liệu và hệ thống từ bản sao lưu"},
            {"icon": "📄", "text": "Viết báo cáo sự cố và đề xuất biện pháp phòng ngừa"},
        ],
        "skill_weight": {"logic": 3, "patience": 2, "comms": 1},
    },
    {
        "id": "pharmacist-dispense",
        "career_id": "pharmacist",
        "title": "Cấp phát thuốc theo đơn tại nhà thuốc",
        "story": (
            "Một khách hàng mang đơn thuốc của bác sĩ đến nhà thuốc. Hãy "
            "sắp xếp đúng quy trình cấp phát thuốc an toàn."
        ),
        "steps": [
            {"icon": "📋", "text": "Kiểm tra tính hợp lệ của đơn thuốc"},
            {"icon": "🔎", "text": "Đối chiếu thuốc với tiền sử dị ứng của khách hàng"},
            {"icon": "📦", "text": "Lấy đúng thuốc, đúng hàm lượng theo đơn"},
            {"icon": "🧮", "text": "Tính đúng liều lượng và số lượng cần cấp"},
            {"icon": "🗣️", "text": "Hướng dẫn khách hàng cách dùng thuốc"},
            {"icon": "🧾", "text": "Ghi chép lại vào hệ thống quản lý nhà thuốc"},
        ],
        "skill_weight": {"patience": 3, "logic": 2, "comms": 2},
    },
    {
        "id": "electrical-install",
        "career_id": "electrical",
        "title": "Lắp đặt hệ thống điện cho một căn hộ mới",
        "story": (
            "Một căn hộ mới xây cần lắp đặt toàn bộ hệ thống điện. Hãy "
            "sắp xếp đúng quy trình thi công."
        ),
        "steps": [
            {"icon": "📐", "text": "Đọc bản vẽ thiết kế hệ thống điện"},
            {"icon": "🧯", "text": "Ngắt nguồn điện tổng để đảm bảo an toàn thi công"},
            {"icon": "🔧", "text": "Đi dây điện âm tường theo đúng sơ đồ"},
            {"icon": "💡", "text": "Lắp đặt ổ cắm, công tắc và đèn"},
            {"icon": "⚡", "text": "Đấu nối vào tủ điện tổng và bật thử nguồn"},
            {"icon": "✅", "text": "Kiểm tra an toàn toàn bộ hệ thống trước khi bàn giao"},
        ],
        "skill_weight": {"logic": 3, "hand": 2, "patience": 1},
    },
    {
        "id": "actor-scene",
        "career_id": "actor",
        "title": "Chuẩn bị cho một cảnh quay phim",
        "story": (
            "Bạn được giao một cảnh quay quan trọng trong phim. Hãy sắp "
            "xếp đúng quy trình chuẩn bị của diễn viên."
        ),
        "steps": [
            {"icon": "📖", "text": "Đọc và phân tích kịch bản, hiểu tâm lý nhân vật"},
            {"icon": "🗣️", "text": "Học thuộc lời thoại của cảnh quay"},
            {"icon": "💇", "text": "Hoá trang và mặc trang phục nhân vật"},
            {"icon": "🎬", "text": "Tập diễn cùng đạo diễn trước khi quay chính thức"},
            {"icon": "🎥", "text": "Diễn xuất cảnh quay theo chỉ đạo của đạo diễn"},
            {"icon": "🔁", "text": "Diễn lại nếu đạo diễn yêu cầu quay thêm (retake)"},
        ],
        "skill_weight": {"creative": 3, "comms": 2, "patience": 1},
    },
    {
        "id": "hotelmanager-complaint",
        "career_id": "hotelmanager",
        "title": "Xử lý tình huống khách hàng phàn nàn về phòng",
        "story": (
            "Một khách hàng phàn nàn phòng của họ chưa được dọn sạch khi "
            "nhận phòng. Hãy sắp xếp đúng quy trình xử lý."
        ),
        "steps": [
            {"icon": "👂", "text": "Lắng nghe và ghi nhận phàn nàn của khách hàng"},
            {"icon": "🙏", "text": "Xin lỗi khách hàng vì trải nghiệm không tốt"},
            {"icon": "🧹", "text": "Điều phối nhân viên dọn phòng xử lý ngay lập tức"},
            {"icon": "🛎️", "text": "Sắp xếp phòng tạm thời hoặc ưu đãi cho khách trong lúc chờ"},
            {"icon": "✅", "text": "Xác nhận lại với khách khi vấn đề đã được giải quyết"},
            {"icon": "📝", "text": "Ghi nhận sự việc để cải thiện quy trình dọn phòng"},
        ],
        "skill_weight": {"comms": 3, "patience": 2, "creative": 1},
    },
    {
        "id": "captain-departure",
        "career_id": "captain",
        "title": "Chuẩn bị cho tàu rời cảng",
        "story": (
            "Con tàu của bạn chuẩn bị rời cảng cho một chuyến hải trình "
            "dài. Hãy sắp xếp đúng quy trình chuẩn bị."
        ),
        "steps": [
            {"icon": "🌦️", "text": "Kiểm tra dự báo thời tiết và hải trình"},
            {"icon": "🔧", "text": "Kiểm tra tình trạng kỹ thuật của tàu"},
            {"icon": "📦", "text": "Giám sát việc xếp hàng hoá lên tàu"},
            {"icon": "👥", "text": "Họp phổ biến nhiệm vụ cho thuyền viên"},
            {"icon": "📡", "text": "Xin phép cảng vụ cho tàu rời cảng"},
            {"icon": "⚓", "text": "Chỉ huy tàu rời cảng theo đúng luồng lạch"},
        ],
        "skill_weight": {"patience": 3, "logic": 2, "comms": 1},
    },
    {
        "id": "marketing-campaign",
        "career_id": "marketing",
        "title": "Lên chiến dịch quảng bá sản phẩm mới",
        "story": (
            "Công ty bạn chuẩn bị ra mắt một sản phẩm mới. Hãy sắp xếp "
            "đúng quy trình lên chiến dịch marketing."
        ),
        "steps": [
            {"icon": "🎯", "text": "Xác định khách hàng mục tiêu của sản phẩm"},
            {"icon": "📊", "text": "Phân tích đối thủ cạnh tranh trên thị trường"},
            {"icon": "💡", "text": "Lên ý tưởng thông điệp và nội dung truyền thông"},
            {"icon": "📅", "text": "Lập kế hoạch triển khai trên các kênh truyền thông"},
            {"icon": "🚀", "text": "Triển khai chiến dịch và theo dõi hiệu quả"},
            {"icon": "📈", "text": "Đánh giá kết quả và điều chỉnh chiến lược"},
        ],
        "skill_weight": {"creative": 3, "comms": 2, "logic": 1},
    },
    {
        "id": "accountant-report",
        "career_id": "accountant",
        "title": "Lập báo cáo tài chính cuối tháng",
        "story": (
            "Cuối tháng, bạn cần tổng hợp và lập báo cáo tài chính cho "
            "công ty. Hãy sắp xếp đúng quy trình thực hiện."
        ),
        "steps": [
            {"icon": "🧾", "text": "Thu thập toàn bộ hoá đơn, chứng từ trong tháng"},
            {"icon": "🗂️", "text": "Phân loại chứng từ theo từng khoản mục"},
            {"icon": "⌨️", "text": "Nhập liệu vào sổ sách kế toán"},
            {"icon": "🔍", "text": "Đối chiếu số liệu với ngân hàng và kho"},
            {"icon": "📊", "text": "Lập báo cáo tài chính tổng hợp"},
            {"icon": "📤", "text": "Trình báo cáo cho ban giám đốc phê duyệt"},
        ],
        "skill_weight": {"logic": 3, "patience": 3, "comms": 1},
    },
    {
        "id": "scientist-experiment",
        "career_id": "scientist",
        "title": "Thực hiện một thí nghiệm khoa học",
        "story": (
            "Bạn đang nghiên cứu hiệu quả của một loại phân bón mới đối "
            "với cây trồng. Hãy sắp xếp đúng quy trình thí nghiệm."
        ),
        "steps": [
            {"icon": "❓", "text": "Đặt câu hỏi nghiên cứu và giả thuyết"},
            {"icon": "📝", "text": "Thiết kế quy trình thí nghiệm đối chứng"},
            {"icon": "🧪", "text": "Chuẩn bị mẫu vật và dụng cụ thí nghiệm"},
            {"icon": "🔬", "text": "Tiến hành thí nghiệm và ghi nhận dữ liệu"},
            {"icon": "📊", "text": "Phân tích số liệu thu được"},
            {"icon": "📄", "text": "Viết báo cáo kết luận nghiên cứu"},
        ],
        "skill_weight": {"logic": 3, "patience": 3, "creative": 1},
    },
    {
        "id": "agriculture-pest",
        "career_id": "agriculture",
        "title": "Xử lý một vườn cây bị sâu bệnh",
        "story": (
            "Một vườn cây ăn quả đang bị sâu bệnh tấn công. Hãy sắp xếp "
            "đúng quy trình xử lý của kỹ sư nông nghiệp."
        ),
        "steps": [
            {"icon": "🔍", "text": "Khảo sát vườn để xác định loại sâu bệnh"},
            {"icon": "🧪", "text": "Lấy mẫu phân tích trong phòng thí nghiệm"},
            {"icon": "📋", "text": "Lập phác đồ xử lý phù hợp"},
            {"icon": "🌿", "text": "Hướng dẫn nông dân phun thuốc/xử lý đúng cách"},
            {"icon": "👀", "text": "Theo dõi tình trạng cây sau xử lý"},
            {"icon": "📈", "text": "Đánh giá hiệu quả và đề xuất phòng ngừa lâu dài"},
        ],
        "skill_weight": {"patience": 3, "logic": 2, "hand": 1},
    },
]
