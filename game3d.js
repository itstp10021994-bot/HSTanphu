// Mô phỏng 3D: học sinh điều khiển nhân vật người đi lại trong không gian
// 3D, tiếp cận từng "điểm tương tác" (hotspot) và thực hiện thao tác theo
// đúng thứ tự quy trình nghề nghiệp. Dùng Three.js (miễn phí, CDN, không
// cần cài đặt) + model nhân vật rigged miễn phí có sẵn trong kho mẫu chính
// thức của Three.js.
//
// QUAN TRỌNG: thư viện Three.js được tải bằng dynamic import() bên trong
// initGame3D() (không phải import tĩnh ở đầu file). Lý do: nếu tải thất
// bại (mạng chặn CDN, v.v.), lỗi có thể được bắt (try/catch) và hiển thị
// rõ ràng cho người dùng thay vì để màn hình đen im lặng không rõ nguyên nhân.

let THREE = null;
let GLTFLoader = null;

const THREE_VERSION = "0.160.0";
const CHARACTER_MODEL_URL =
  "https://cdn.jsdelivr.net/gh/mrdoob/three.js@r160/examples/models/gltf/Soldier.glb";

const HOTSPOT_LAYOUT = [
  [-6, -4], [6, -5], [-7, 3], [7, 4], [0, -7.5], [0, 7], [-3, 6.5], [3, -7],
];

const MOVE_SPEED = 4.2; // đơn vị/giây
const INTERACT_RADIUS = 2.0;
const ROOM_HALF = 9;

function showFatalError(container, title, detail) {
  container.innerHTML = "";
  const box = document.createElement("div");
  box.className = "game3d-error";
  box.innerHTML =
    `<strong>${title}</strong><p>${detail}</p>` +
    `<p class="game3d-error-hint">Thử tải lại trang. Nếu vẫn lỗi, có thể mạng của bạn đang chặn ` +
    `cdn.jsdelivr.net — hãy thử mạng khác hoặc báo cho người quản trị mạng mở CDN này.</p>`;
  container.appendChild(box);
}

function buildRoom(careerId, accentColor) {
  const group = new THREE.Group();

  const floorColor = {
    dev: 0x1b2035, doctor: 0x241a1c, chef: 0x241d13,
    teacher: 0x1a2333, civil: 0x241f18, lawyer: 0x201a2e, pilot: 0x16232e, photographer: 0x2a1a24,
  }[careerId] || 0x1b1d33;
  const floor = new THREE.Mesh(
    new THREE.PlaneGeometry(ROOM_HALF * 2 + 2, ROOM_HALF * 2 + 2),
    new THREE.MeshStandardMaterial({ color: floorColor, roughness: 0.9 })
  );
  floor.rotation.x = -Math.PI / 2;
  floor.receiveShadow = true;
  group.add(floor);

  // Tường thấp bao quanh để định hình không gian
  const wallMat = new THREE.MeshStandardMaterial({ color: 0x2a2e55, roughness: 1 });
  const wallHeight = 3;
  const wallThickness = 0.4;
  const positions = [
    [0, -ROOM_HALF - 1, ROOM_HALF * 2 + 2, wallThickness],
    [0, ROOM_HALF + 1, ROOM_HALF * 2 + 2, wallThickness],
    [-ROOM_HALF - 1, 0, wallThickness, ROOM_HALF * 2 + 2],
    [ROOM_HALF + 1, 0, wallThickness, ROOM_HALF * 2 + 2],
  ];
  positions.forEach(([x, z, w, d]) => {
    const wall = new THREE.Mesh(new THREE.BoxGeometry(w, wallHeight, d), wallMat);
    wall.position.set(x, wallHeight / 2, z);
    group.add(wall);
  });

  // Vật trang trí đơn giản theo ngành, chỉ để gợi không khí — không tương tác
  const propMat = new THREE.MeshStandardMaterial({ color: accentColor, roughness: 0.6 });
  const props = [];
  if (careerId === "dev") {
    props.push({ size: [2.2, 1.1, 1], pos: [-3, 0.55, -2] });
    props.push({ size: [1.2, 0.9, 0.1], pos: [-3, 1.3, -2.4] });
  } else if (careerId === "doctor") {
    props.push({ size: [2, 0.6, 1], pos: [3, 0.3, 2] });
    props.push({ size: [0.6, 1, 0.6], pos: [4.2, 0.5, 1.2] });
  } else if (careerId === "chef") {
    props.push({ size: [2, 0.9, 0.8], pos: [-2, 0.45, 3] });
    props.push({ size: [1.4, 0.8, 0.8], pos: [2.5, 0.4, -2.5] });
  } else if (careerId === "teacher") {
    props.push({ size: [2.6, 1.4, 0.1], pos: [0, 0.7, -4.4] }); // bảng đen
    props.push({ size: [1.8, 0.8, 0.7], pos: [0, 0.4, -2.2] }); // bàn giáo viên
  } else if (careerId === "civil") {
    props.push({ size: [1.6, 0.5, 1.6], pos: [-3, 0.25, 2] }); // khối móng đang thi công
    props.push({ size: [0.3, 1.6, 0.3], pos: [3, 0.8, -2] }); // cột thép
  } else if (careerId === "lawyer") {
    props.push({ size: [2.4, 1, 1.1], pos: [0, 0.5, -3] }); // bục toà
    props.push({ size: [1.4, 0.8, 0.7], pos: [-3, 0.4, 2] }); // bàn hồ sơ
  } else if (careerId === "pilot") {
    props.push({ size: [2.6, 1, 1.4], pos: [0, 0.5, -3.5] }); // bảng điều khiển
    props.push({ size: [0.5, 0.9, 0.5], pos: [-2.4, 0.45, -3] }); // ghế lái
  } else if (careerId === "photographer") {
    props.push({ size: [0.15, 1.6, 0.15], pos: [-3, 0.8, -2] }); // chân máy
    props.push({ size: [1, 1.4, 0.08], pos: [2.5, 0.7, -3] }); // phông nền
  } else {
    props.push({ size: [1.6, 0.9, 0.8], pos: [-2, 0.45, 2] });
  }
  props.forEach(({ size, pos }) => {
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(...size), propMat);
    mesh.position.set(...pos);
    group.add(mesh);
  });

  return group;
}

function makeHotspotLabel(text) {
  const el = document.createElement("div");
  el.className = "hotspot-label";
  el.textContent = text;
  return el;
}

function buildFallbackCharacter() {
  const g = new THREE.Group();
  const body = new THREE.Mesh(
    new THREE.CapsuleGeometry(0.4, 0.9, 4, 8),
    new THREE.MeshStandardMaterial({ color: 0xdfe7ff })
  );
  body.position.y = 0.85;
  const head = new THREE.Mesh(
    new THREE.SphereGeometry(0.28, 16, 16),
    new THREE.MeshStandardMaterial({ color: 0xffd8b0 })
  );
  head.position.y = 1.55;
  g.add(body, head);
  return g;
}

export async function initGame3D({ containerId, careerId, accentColor, steps, submitUrl, onSubmitted }) {
  const container = document.getElementById(containerId);

  // ---- Bước 1: tải thư viện Three.js (có thể lỗi do mạng) ----
  try {
    const [threeMod, gltfMod] = await Promise.all([
      import(`https://cdn.jsdelivr.net/npm/three@${THREE_VERSION}/build/three.module.js`),
      import(`https://cdn.jsdelivr.net/npm/three@${THREE_VERSION}/examples/jsm/loaders/GLTFLoader.js`),
    ]);
    THREE = threeMod;
    GLTFLoader = gltfMod.GLTFLoader;
  } catch (err) {
    console.error("Không tải được thư viện Three.js:", err);
    showFatalError(
      container,
      "Không tải được thư viện đồ hoạ 3D",
      "Trình duyệt không tải được thư viện cần thiết từ mạng (cdn.jsdelivr.net)."
    );
    return;
  }

  const hudCount = document.getElementById("hud-count");
  const hudTotal = document.getElementById("hud-total");
  const hudPrompt = document.getElementById("hud-prompt");
  const actionBtn = document.getElementById("action-btn");
  hudTotal.textContent = steps.length;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x14162b);
  scene.fog = new THREE.Fog(0x14162b, 14, 30);

  const camera = new THREE.PerspectiveCamera(55, 1, 0.1, 100);

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true });
  } catch (err) {
    showFatalError(
      container,
      "Trình duyệt không hỗ trợ WebGL",
      "Thiết bị hoặc trình duyệt này không bật được đồ hoạ 3D (WebGL). Hãy thử trình duyệt khác (Chrome/Edge bản mới)."
    );
    return;
  }
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.shadowMap.enabled = true;
  container.appendChild(renderer.domElement);

  const hud = document.getElementById("hud");
  if (hud && hud.parentElement !== container) container.appendChild(hud);

  function resize() {
    const w = container.clientWidth;
    const h = container.clientHeight;
    renderer.setSize(w, h);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  window.addEventListener("resize", resize);

  scene.add(new THREE.HemisphereLight(0x8899ff, 0x141420, 0.9));
  const sun = new THREE.DirectionalLight(0xffffff, 1.1);
  sun.position.set(6, 10, 4);
  sun.castShadow = true;
  scene.add(sun);

  const accent = new THREE.Color(accentColor);
  scene.add(buildRoom(careerId, accent));

  // ---- Hotspots ----
  const labelLayer = document.createElement("div");
  labelLayer.className = "hotspot-label-layer";
  container.appendChild(labelLayer);

  const hotspots = steps.map((step, i) => {
    const [x, z] = HOTSPOT_LAYOUT[i % HOTSPOT_LAYOUT.length];
    const ring = new THREE.Mesh(
      new THREE.CylinderGeometry(1, 1, 0.08, 24),
      new THREE.MeshStandardMaterial({ color: accent, emissive: accent, emissiveIntensity: 0.4 })
    );
    ring.position.set(x, 0.04, z);
    scene.add(ring);

    const label = makeHotspotLabel(step.text);
    labelLayer.appendChild(label);

    return { step, position: new THREE.Vector3(x, 0, z), mesh: ring, label, done: false };
  });

  // ---- Nhân vật ----
  let character = new THREE.Group();
  scene.add(character);
  let mixer = null;
  let idleAction = null;
  let walkAction = null;
  let currentAction = null;
  const clock = new THREE.Clock();

  function fadeToAction(next) {
    if (!next || next === currentAction) return;
    if (currentAction) currentAction.fadeOut(0.2);
    next.reset().fadeIn(0.2).play();
    currentAction = next;
  }

  if (GLTFLoader) {
    try {
      const loader = new GLTFLoader();
      loader.load(
        CHARACTER_MODEL_URL,
        (gltf) => {
          scene.remove(character);
          character = gltf.scene;
          character.traverse((o) => { if (o.isMesh) o.castShadow = true; });
          scene.add(character);

          mixer = new THREE.AnimationMixer(character);
          const clips = gltf.animations || [];
          const findClip = (kw) => clips.find((c) => c.name.toLowerCase().includes(kw));
          const idleClip = findClip("idle") || clips[0];
          const walkClip = findClip("walk") || clips[1] || clips[0];
          if (idleClip) idleAction = mixer.clipAction(idleClip);
          if (walkClip) walkAction = mixer.clipAction(walkClip);
          if (idleAction) fadeToAction(idleAction);
        },
        undefined,
        (err) => {
          console.warn("Không tải được model nhân vật, dùng nhân vật đơn giản thay thế:", err);
          scene.remove(character);
          character = buildFallbackCharacter();
          scene.add(character);
        }
      );
    } catch (err) {
      console.warn("Lỗi GLTFLoader, dùng nhân vật đơn giản thay thế:", err);
      character = buildFallbackCharacter();
      scene.add(character);
    }
  } else {
    character = buildFallbackCharacter();
    scene.add(character);
  }

  // ---- Điều khiển ----
  const input = { up: false, down: false, left: false, right: false };
  const keyMap = {
    ArrowUp: "up", KeyW: "up",
    ArrowDown: "down", KeyS: "down",
    ArrowLeft: "left", KeyA: "left",
    ArrowRight: "right", KeyD: "right",
  };
  window.addEventListener("keydown", (e) => {
    if (keyMap[e.code]) input[keyMap[e.code]] = true;
    if (e.code === "KeyE") tryInteract();
  });
  window.addEventListener("keyup", (e) => {
    if (keyMap[e.code]) input[keyMap[e.code]] = false;
  });

  document.querySelectorAll("#mobile-controls [data-dir]").forEach((btn) => {
    const dir = btn.dataset.dir;
    const set = (v) => (input[dir] = v);
    btn.addEventListener("pointerdown", (e) => { e.preventDefault(); set(true); });
    btn.addEventListener("pointerup", () => set(false));
    btn.addEventListener("pointerleave", () => set(false));
    btn.addEventListener("pointercancel", () => set(false));
  });

  let nearestHotspot = null;
  function updateHotspotProximity() {
    let nearest = null;
    let nearestDist = Infinity;
    hotspots.forEach((h) => {
      if (h.done) return;
      const d = character.position.distanceTo(h.position);
      if (d < nearestDist) { nearestDist = d; nearest = h; }
    });
    if (nearest && nearestDist <= INTERACT_RADIUS) {
      nearestHotspot = nearest;
      hudPrompt.hidden = false;
      hudPrompt.textContent = `Ở gần: "${nearest.step.text}" — nhấn E hoặc bấm nút để thực hiện`;
      actionBtn.hidden = false;
    } else {
      nearestHotspot = null;
      hudPrompt.hidden = true;
      actionBtn.hidden = true;
    }
  }

  const completedOrder = [];
  function tryInteract() {
    if (!nearestHotspot || nearestHotspot.done) return;
    nearestHotspot.done = true;
    nearestHotspot.mesh.material.color.set(0x34d399);
    nearestHotspot.mesh.material.emissive.set(0x34d399);
    nearestHotspot.label.classList.add("done");
    completedOrder.push(nearestHotspot.step.correct_index);
    hudCount.textContent = completedOrder.length;
    hudPrompt.hidden = true;
    actionBtn.hidden = true;

    if (completedOrder.length === hotspots.length) {
      submitOrder();
    }
  }
  actionBtn.addEventListener("click", tryInteract);

  async function submitOrder() {
    try {
      const res = await fetch(submitUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ order: completedOrder }),
      });
      const data = await res.json();
      onSubmitted(data);
    } catch (err) {
      onSubmitted({ error: true });
    }
  }

  // ---- Vòng lặp render ----
  function animate() {
    requestAnimationFrame(animate);
    const dt = Math.min(clock.getDelta(), 0.05);

    const move = new THREE.Vector3(
      (input.right ? 1 : 0) - (input.left ? 1 : 0),
      0,
      (input.down ? 1 : 0) - (input.up ? 1 : 0)
    );
    const isMoving = move.lengthSq() > 0;
    if (isMoving) {
      move.normalize();
      character.position.addScaledVector(move, MOVE_SPEED * dt);
      character.position.x = THREE.MathUtils.clamp(character.position.x, -ROOM_HALF, ROOM_HALF);
      character.position.z = THREE.MathUtils.clamp(character.position.z, -ROOM_HALF, ROOM_HALF);
      const targetAngle = Math.atan2(move.x, move.z);
      character.rotation.y = THREE.MathUtils.lerp(character.rotation.y, targetAngle, 0.25);
      if (walkAction) fadeToAction(walkAction);
    } else if (idleAction) {
      fadeToAction(idleAction);
    }

    if (mixer) mixer.update(dt);

    const camOffset = new THREE.Vector3(0, 5.5, 8);
    const desiredCamPos = character.position.clone().add(camOffset);
    camera.position.lerp(desiredCamPos, 0.08);
    camera.lookAt(character.position.clone().add(new THREE.Vector3(0, 1.2, 0)));

    hotspots.forEach((h) => {
      const p = h.position.clone().add(new THREE.Vector3(0, 1.4, 0));
      p.project(camera);
      const x = (p.x * 0.5 + 0.5) * container.clientWidth;
      const y = (-p.y * 0.5 + 0.5) * container.clientHeight;
      const visible = p.z < 1 && !h.done;
      h.label.style.display = visible ? "block" : "none";
      h.label.style.transform = `translate(${x}px, ${y}px)`;
    });

    updateHotspotProximity();
    renderer.render(scene, camera);
  }

  resize();
  animate();
}
