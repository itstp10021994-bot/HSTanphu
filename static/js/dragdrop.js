// Kéo-thả để sắp xếp lại thứ tự các bước — dùng Pointer Events thuần
// (không phụ thuộc thư viện ngoài, không cần CDN) nên chạy được cả trên
// chuột lẫn cảm ứng, và không bao giờ bị lỗi do mạng chặn tài nguyên ngoài.

(function () {
  const list = document.getElementById("step-list");
  const submitBtn = document.getElementById("submit-btn");
  const feedback = document.getElementById("feedback");
  const feedbackSummary = document.getElementById("feedback-summary");
  const feedbackEarned = document.getElementById("feedback-earned");

  let dragEl = null;
  let startY = 0;
  let startTop = 0;
  let itemHeight = 0;

  function renumber() {
    [...list.children].forEach((li, i) => {
      li.querySelector(".step-order-num").textContent = i + 1;
    });
  }

  function getItems() {
    return [...list.querySelectorAll(".step-item")];
  }

  function onPointerDown(e) {
    const item = e.target.closest(".step-item");
    if (!item) return;
    dragEl = item;
    itemHeight = item.offsetHeight + 10; // 10px = khoảng cách giữa các thẻ
    startY = e.clientY;
    startTop = item.offsetTop;
    item.setPointerCapture(e.pointerId);
    item.classList.add("dragging");
    item.style.zIndex = 5;
    document.addEventListener("pointermove", onPointerMove);
    document.addEventListener("pointerup", onPointerUp);
  }

  function onPointerMove(e) {
    if (!dragEl) return;
    const delta = e.clientY - startY;
    dragEl.style.transform = `translateY(${delta}px)`;

    const items = getItems();
    const dragIndex = items.indexOf(dragEl);
    const dragCenter = startTop + delta + itemHeight / 2;

    items.forEach((sibling, i) => {
      if (sibling === dragEl) return;
      const siblingCenter = sibling.offsetTop + itemHeight / 2;

      if (i < dragIndex && dragCenter < siblingCenter) {
        list.insertBefore(dragEl, sibling);
        startTop = dragEl.offsetTop;
        startY = e.clientY;
        dragEl.style.transform = "translateY(0px)";
        renumber();
      } else if (i > dragIndex && dragCenter > siblingCenter) {
        list.insertBefore(dragEl, sibling.nextSibling);
        startTop = dragEl.offsetTop;
        startY = e.clientY;
        dragEl.style.transform = "translateY(0px)";
        renumber();
      }
    });
  }

  function onPointerUp() {
    if (!dragEl) return;
    dragEl.style.transform = "";
    dragEl.style.zIndex = "";
    dragEl.classList.remove("dragging");
    dragEl = null;
    document.removeEventListener("pointermove", onPointerMove);
    document.removeEventListener("pointerup", onPointerUp);
  }

  list.addEventListener("pointerdown", onPointerDown);
  renumber();

  async function submitOrder() {
    const order = getItems().map((li) => parseInt(li.dataset.correct, 10));
    submitBtn.disabled = true;
    submitBtn.textContent = "Đang chấm điểm...";

    try {
      const res = await fetch(window.TASK_SUBMIT_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ order }),
      });
      const data = await res.json();

      const emoji = data.accuracy === 100 ? "🎉" : data.accuracy >= 60 ? "👍" : "💡";
      feedbackSummary.textContent =
        `${emoji} Độ chính xác: ${data.accuracy}% (đúng vị trí ${data.correct_positions}/${data.total} bước).`;
      feedbackEarned.innerHTML = "";
      Object.entries(data.earned).forEach(([skill, pts]) => {
        const pill = document.createElement("span");
        pill.className = "earned-pill";
        pill.textContent = `+${pts} ${skill}`;
        feedbackEarned.appendChild(pill);
      });
      feedback.hidden = false;
      submitBtn.hidden = true;
      feedback.scrollIntoView({ behavior: "smooth", block: "nearest" });
    } catch (err) {
      submitBtn.disabled = false;
      submitBtn.textContent = "✓ Xác nhận thứ tự";
      alert("Có lỗi khi gửi kết quả, vui lòng thử lại.");
    }
  }

  submitBtn.addEventListener("click", submitOrder);
})();
