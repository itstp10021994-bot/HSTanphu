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

## Thông tin thị trường (lương/nhu cầu) — tự động kiểm tra định kỳ

`market_data.json` chứa thông tin lương/nhu cầu tuyển dụng tham khảo cho
một số ngành, kèm trích dẫn nguồn. File này **tách riêng khỏi `data.py`**
để có thể cập nhật độc lập, không cần sửa code.

- **Tự động (GitHub Actions)**: workflow `.github/workflows/update-market-data.yml`
  chạy vào ngày 1 mỗi tháng, gọi `scripts/update_market_data.py` để kiểm
  tra xem các con số đã trích dẫn có còn xuất hiện trên trang nguồn không.
  - Nếu vẫn khớp → chỉ cập nhật ngày kiểm tra gần nhất (`last_checked`).
  - Nếu không còn khớp con số nào → đánh dấu `status: "needs_review"` và
    trang web sẽ tự hiển thị cảnh báo ⚠️ cho đến khi ai đó xem lại và viết
    lại câu mô tả cho đúng.
  - **Script KHÔNG tự viết lại câu mô tả** — chỉ phát hiện thay đổi và báo
    hiệu, để tránh rủi ro tự động hiển thị thông tin sai/bịa cho học sinh.
  - Có thể chạy tay bất cứ lúc nào: tab **Actions** trên GitHub > chọn
    workflow "Kiểm tra định kỳ dữ liệu thị trường lương" > **Run workflow**.
- **Thủ công**: khi thấy cảnh báo "cần xem lại", mở file `market_data.json`
  trên GitHub, sửa lại `text` cho đúng số liệu mới, đổi `status` về `"ok"`,
  commit — Render sẽ tự deploy lại.
- Thêm ngành mới vào hệ thống này: thêm 1 mục vào `market_data.json` với
  key là `career_id`, gồm `text`, `source_name`, `source_url`.

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
