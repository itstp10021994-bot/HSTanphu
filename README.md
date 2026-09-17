# Khám Phá Nghề — Ứng dụng mô phỏng trải nghiệm nghề nghiệp

Web app giúp học sinh thử "làm thật" một nhiệm vụ đặc trưng của từng ngành
nghề (kéo-thả sắp xếp quy trình đúng), qua đó đo năng lực (tư duy logic,
khéo léo, sáng tạo, kiên nhẫn, giao tiếp) và gợi ý ngành phù hợp.

100% Python ở phần backend & logic. 100% miễn phí — không thư viện trả phí,
không dịch vụ bên thứ ba, không cần tài khoản/đăng nhập.

## Chạy thử trên máy

```bash
cd career-sim
pip install -r requirements.txt
python app.py
```

Mở trình duyệt tại `http://127.0.0.1:5000`.

## Cấu trúc thư mục

```
career-sim/
├── app.py              # Flask backend: route, chấm điểm, gợi ý ngành
├── data.py             # Dữ liệu ngành nghề / nhiệm vụ — CHỈ SỬA FILE NÀY để thêm nội dung
├── requirements.txt
├── templates/           # Giao diện (Jinja2)
│   ├── base.html
│   ├── index.html       # Trang chọn ngành nghề
│   ├── career.html      # Giới thiệu ngành + danh sách nhiệm vụ
│   ├── task.html         # Mini-game kéo-thả
│   └── result.html       # Hồ sơ năng lực + gợi ý ngành
└── static/
    ├── css/style.css
    └── js/dragdrop.js    # Kéo-thả bằng Pointer Events (không dùng thư viện ngoài, không cần CDN)
```

## Cách hoạt động

- Mỗi nhiệm vụ là một quy trình gồm nhiều bước (mỗi bước có 1 icon minh
  hoạ + mô tả ngắn) bị xáo trộn; học sinh kéo-thả các thẻ để sắp lại đúng
  thứ tự — không cần đọc nhiều chữ, nhìn icon là đoán được hành động.
- Độ chính xác (số bước đúng vị trí / tổng số bước) được quy đổi thành điểm
  cho từng năng lực theo trọng số khai báo trong `data.py`.
- Tiến trình lưu trong **session cookie của trình duyệt** — không cần đăng
  nhập, không cần cơ sở dữ liệu. Vào lại từ trình duyệt khác sẽ là hồ sơ mới.
- Trang "Hồ sơ năng lực" so khớp vector năng lực của học sinh với hồ sơ yêu
  cầu năng lực của từng ngành (`CAREER_SKILL_PROFILE`) để xếp hạng độ phù hợp
  — kể cả những ngành học sinh **chưa** thử.
- Toàn bộ giao diện chạy bằng HTML/CSS/JS thuần, không gọi CDN ngoài nào —
  nên không bao giờ bị lỗi do mạng chặn tài nguyên bên thứ ba (đã từng gặp
  vấn đề này ở bản dùng nhân vật 3D Three.js trước đây).

## Dữ liệu động (lương, lộ trình học, xu hướng AI) — tự động kiểm tra hàng tuần

3 file JSON tách riêng khỏi `data.py`, mỗi file có thể cập nhật độc lập
không cần sửa code:

- `market_data.json` — lương & nhu cầu thị trường
- `study_data.json` — khối thi & lộ trình học tập
- `automation_data.json` — mức độ rủi ro tự động hoá (theo WEF Future of Jobs)

**Tự động (GitHub Actions, chạy 02:00 UTC thứ Hai hàng tuần)**:
`.github/workflows/update-dynamic-data.yml` gọi
`scripts/update_dynamic_data.py`, kiểm tra CẢ 3 file bằng cách tải lại
đúng trang nguồn và so khớp với dữ liệu đang lưu:

| File | Cách kiểm tra |
|---|---|
| `market_data.json` | Mỗi ngành có 1 trang nguồn riêng — so khớp trực tiếp các con số lương |
| `study_data.json` | Tất cả dùng chung 1 trang (Tuyển Sinh 247 – tổ hợp môn) — kiểm tra mã khối thi (A00, B00...) có còn trong danh sách chính thức |
| `automation_data.json` | Tất cả dùng chung 1 nguồn (báo cáo PDF của WEF) — kiểm tra từ khoá liên quan đến ngành có còn xuất hiện trong báo cáo |

- Còn khớp → chỉ cập nhật `last_checked` (ngày kiểm tra gần nhất).
- Không còn khớp → đánh dấu `status: "needs_review"`, trang web tự hiển
  thị cảnh báo ⚠️ "Cần xem lại" thay cho tiêu đề thẻ.
- **Script KHÔNG tự viết lại nội dung** — chỉ phát hiện và báo hiệu, để
  tránh rủi ro tự động hiển thị thông tin sai/bịa cho học sinh.
- Không tải được trang (lỗi mạng...) → bỏ qua, giữ nguyên trạng thái cũ,
  KHÔNG coi đó là dấu hiệu cần xem lại.
- Có thể chạy tay bất cứ lúc nào: tab **Actions** trên GitHub > chọn
  workflow "Kiểm tra định kỳ dữ liệu động..." > **Run workflow**.

**Lưu ý về độ chính xác của việc kiểm tra**: `market_data.json` được kiểm
chứng chính xác theo từng ngành (mỗi ngành 1 nguồn riêng). `study_data.json`
và `automation_data.json` dùng chung 1 nguồn cho tất cả các ngành nên chỉ
phát hiện được khi nguồn đó có thay đổi lớn (VD: khối thi bị bỏ hoàn toàn
khỏi hệ thống, hoặc WEF ra báo cáo bản mới) — không phát hiện được các thay
đổi nhỏ, cụ thể theo từng trường/ngành riêng lẻ.

**Thủ công**: khi thấy cảnh báo "cần xem lại", mở đúng file JSON trên
GitHub, sửa lại nội dung cho đúng, đổi `status` về `"ok"`, commit — Render
sẽ tự deploy lại.

## Thêm ngành nghề / nhiệm vụ mới

Chỉ cần sửa `data.py`:
1. Thêm một mục vào `CAREERS`.
2. Thêm trọng số năng lực yêu cầu vào `CAREER_SKILL_PROFILE`.
3. Thêm một hoặc nhiều nhiệm vụ vào `TASKS`, với `career_id` trỏ đúng ngành
   vừa thêm, danh sách `steps` (mỗi bước là `{"icon": "...", "text": "..."}`)
   theo **đúng thứ tự chuẩn**, và `skill_weight` là năng lực nhiệm vụ đó
   rèn luyện. Icon chỉ cần là 1 emoji phù hợp với nội dung bước đó.

Không cần sửa gì ở `app.py` hay giao diện — mọi thứ tự động hiển thị.

## ⚠️ Lưu ý khi chọn nơi deploy

Đây là **ứng dụng Flask thông thường**, KHÔNG phải ứng dụng Streamlit.
**Không deploy lên Streamlit Community Cloud** — nền tảng đó chỉ chạy được
app viết bằng thư viện `streamlit`, chạy Flask trên đó sẽ báo lỗi
`signal.signal` do cách Streamlit Cloud khởi chạy script không tương thích
với reloader của Flask. Hãy dùng một trong các nền tảng ở mục bên dưới.

## Triển khai miễn phí (để học sinh truy cập qua internet)

Vài lựa chọn hosting có gói **free tier vĩnh viễn** (không cần thẻ tín dụng,
hoặc có nhưng không tính phí ở mức sử dụng nhỏ):

- **Render.com** (Free Web Service): kết nối repo GitHub, chọn
  `Build Command: pip install -r requirements.txt`,
  `Start Command: gunicorn app:app`. Cần thêm `gunicorn` vào
  `requirements.txt` khi deploy thật (dev server của Flask chỉ dùng để test).
- **PythonAnywhere** (Free account): upload code, cấu hình WSGI trỏ vào
  `app.py`, không cần thẻ tín dụng.
- **Railway** / **Fly.io**: có free tier giới hạn giờ chạy/tháng, phù hợp
  demo cho lớp học hoặc nhóm nhỏ.

Trước khi deploy thật:
1. Đổi `app.secret_key` trong `app.py` thành một chuỗi ngẫu nhiên bí mật.
2. Tắt `debug=True` trong `app.run(...)`.
3. Thêm `gunicorn` vào `requirements.txt` và dùng nó làm production server
   thay vì `flask run`.

## Hướng phát triển tiếp theo (gợi ý, chưa làm)

- Thêm loại nhiệm vụ khác ngoài "sắp xếp thứ tự" (VD: kéo đúng vật dụng vào
  đúng vị trí, ra quyết định theo tình huống có nhiều nhánh).
- Mở rộng từ 3 lên 10-15 ngành theo đúng dự tính ban đầu.
- Lưu kết quả vào SQLite nếu muốn học sinh xem lại lịch sử trên nhiều thiết bị.
- Bảng điều khiển cho giáo viên tổng hợp kết quả cả lớp.
