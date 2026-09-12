# -*- coding: utf-8 -*-
"""
Ứng dụng mô phỏng trải nghiệm nghề nghiệp cho học sinh.
Backend: Flask (Python) — 100% miễn phí, không cần dịch vụ trả phí nào.

Tiến trình của học sinh được lưu trong session (cookie phía trình duyệt),
nên KHÔNG cần đăng nhập, KHÔNG cần cơ sở dữ liệu cho bản MVP này.
"""
import os
import random
from flask import Flask, render_template, session, jsonify, request, redirect, url_for

from data import CAREERS, SKILLS, TASKS, CAREER_SKILL_PROFILE

app = Flask(__name__)
app.secret_key = "doi-chuoi-nay-truoc-khi-trien-khai-that"  # TODO: đổi khi deploy

# Tắt cache mặc định của Flask cho file tĩnh — quan trọng vì mỗi lần deploy
# bản mới, nếu không có dòng này, trình duyệt (hoặc CDN của nơi hosting) có
# thể tiếp tục phục vụ file .js/.css CŨ đã lưu trong cache, khiến người dùng
# thấy lỗi dù code trên server đã đúng.
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


def asset_url(filename):
    """url_for('static', ...) nhưng luôn kèm ?v=<thời gian sửa file cuối>
    để trình duyệt/CDN tự tải lại bản mới mỗi khi file thay đổi, thay vì
    dùng nhầm bản cache cũ."""
    path = os.path.join(app.static_folder, filename)
    try:
        version = int(os.path.getmtime(path))
    except OSError:
        version = 0
    return url_for("static", filename=filename, v=version)


app.jinja_env.globals["asset_url"] = asset_url


@app.after_request
def add_no_cache_headers(response):
    """Chặn cache cho MỌI response (kể cả các trang HTML động), không chỉ
    file CSS/JS tĩnh. Nếu không có dòng này, trình duyệt hoặc CDN của nơi
    hosting (Render, v.v.) có thể tiếp tục hiển thị bản HTML CŨ sau khi đã
    deploy code mới, khiến người dùng tưởng nhầm là code chưa cập nhật."""
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response


CAREERS_BY_ID = {c["id"]: c for c in CAREERS}
TASKS_BY_ID = {t["id"]: t for t in TASKS}
SKILLS_BY_ID = {s["id"]: s for s in SKILLS}


def get_progress():
    """Lấy tiến trình học sinh từ session, khởi tạo nếu chưa có."""
    if "skill_points" not in session:
        session["skill_points"] = {s["id"]: 0 for s in SKILLS}
    if "completed_tasks" not in session:
        session["completed_tasks"] = []
    return session["skill_points"], session["completed_tasks"]


def tasks_for_career(career_id):
    return [t for t in TASKS if t["career_id"] == career_id]


@app.route("/")
def index():
    skill_points, completed = get_progress()
    careers_view = []
    for c in CAREERS:
        c_tasks = tasks_for_career(c["id"])
        done = sum(1 for t in c_tasks if t["id"] in completed)
        careers_view.append({**c, "total_tasks": len(c_tasks), "done_tasks": done})
    return render_template(
        "index.html",
        careers=careers_view,
        has_progress=any(v > 0 for v in skill_points.values()),
    )


@app.route("/career/<career_id>")
def career_detail(career_id):
    career = CAREERS_BY_ID.get(career_id)
    if not career:
        return redirect(url_for("index"))
    _, completed = get_progress()
    c_tasks = [
        {**t, "done": t["id"] in completed} for t in tasks_for_career(career_id)
    ]
    return render_template("career.html", career=career, tasks=c_tasks)


@app.route("/task/<task_id>")
def task_detail(task_id):
    task = TASKS_BY_ID.get(task_id)
    if not task:
        return redirect(url_for("index"))
    career = CAREERS_BY_ID[task["career_id"]]

    # Xáo trộn thứ tự hiển thị, giữ id gốc để chấm điểm
    shuffled = list(enumerate(task["steps"]))  # (correct_index, {"icon","text"})
    random.shuffle(shuffled)
    display_steps = [
        {
            "step_uid": idx,
            "correct_index": ci,
            "text": step["text"],
            "icon": step.get("icon", "📌"),
        }
        for idx, (ci, step) in enumerate(shuffled)
    ]

    return render_template(
        "task.html", task=task, career=career, steps=display_steps
    )


@app.route("/api/task/<task_id>/submit", methods=["POST"])
def submit_task(task_id):
    task = TASKS_BY_ID.get(task_id)
    if not task:
        return jsonify({"error": "not_found"}), 404

    payload = request.get_json(force=True)
    submitted_correct_indices = payload.get("order", [])  # list correct_index theo thứ tự HS xếp
    total = len(task["steps"])

    if len(submitted_correct_indices) != total:
        return jsonify({"error": "invalid_order"}), 400

    correct_positions = sum(
        1 for pos, ci in enumerate(submitted_correct_indices) if pos == ci
    )
    accuracy = correct_positions / total

    skill_points, completed = get_progress()
    earned = {}
    for skill_id, weight in task["skill_weight"].items():
        points = round(accuracy * weight * 10)
        earned[skill_id] = points
        skill_points[skill_id] = skill_points.get(skill_id, 0) + points

    if task_id not in completed:
        completed.append(task_id)

    session["skill_points"] = skill_points
    session["completed_tasks"] = completed
    session.modified = True

    return jsonify(
        {
            "accuracy": round(accuracy * 100),
            "correct_positions": correct_positions,
            "total": total,
            "earned": {SKILLS_BY_ID[k]["name"]: v for k, v in earned.items()},
        }
    )


@app.route("/result")
def result():
    skill_points, completed = get_progress()

    total_points = sum(skill_points.values()) or 1
    skill_bars = [
        {
            "name": s["name"],
            "points": skill_points.get(s["id"], 0),
            "pct": round(skill_points.get(s["id"], 0) / total_points * 100),
        }
        for s in SKILLS
    ]
    skill_bars.sort(key=lambda x: x["points"], reverse=True)

    # Chấm điểm mức độ phù hợp với từng ngành: tích vô hướng giữa
    # vector năng lực của học sinh và hồ sơ yêu cầu năng lực của ngành.
    matches = []
    for career in CAREERS:
        profile = CAREER_SKILL_PROFILE[career["id"]]
        score = sum(skill_points.get(sid, 0) * w for sid, w in profile.items())
        matches.append(
            {
                **career,
                "match_score": score,
                "tried": any(
                    t["id"] in completed for t in tasks_for_career(career["id"])
                ),
            }
        )
    max_score = max((m["match_score"] for m in matches), default=0) or 1
    for m in matches:
        m["match_pct"] = round(m["match_score"] / max_score * 100)
    matches.sort(key=lambda x: x["match_score"], reverse=True)

    return render_template(
        "result.html",
        skill_bars=skill_bars,
        matches=matches,
        completed_count=len(completed),
        total_tasks=len(TASKS),
    )


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    import os
    # Chỉ bật debug/reloader khi chạy thủ công trên máy (KHÔNG dùng khi deploy).
    # Khi deploy thật, dùng gunicorn (xem README) thay vì chạy file này trực tiếp.
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
