// Mô phỏng 3D: học sinh điều khiển nhân vật người đi lại trong không gian
// 3D, tiếp cận từng "điểm tương tác" (hotspot) và thực hiện thao tác theo
// đúng thứ tự quy trình nghề nghiệp. Dùng Three.js (miễn phí, CDN, không
// cần cài đặt) + model nhân vật rigged miễn phí có sẵn trong kho mẫu chính
// thức của Three.js.

import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js";
import { GLTFLoader } from "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/loaders/GLTFLoader.js";

const CHARACTER_MODEL_URL =
  "https://cdn.jsdelivr.net/gh/mrdoob/three.js@r160/examples/models/gltf/Soldier.glb";

const HOTSPOT_LAYOUT = [
  [-6, -4], [6, -5], [-7, 3], [7, 4], [0, -7.5], [0, 7], [-3, 6.5], [3, -7],
];

const MOVE_SPEED = 4.2; // đơn vị/giây
const INTERACT_RADIUS = 2.0;
const ROOM_HALF = 9;

function buildRoom(careerId, accentColor) {
  const group = new THREE.Group();

  const floorColor = { dev: 0x1b2035, doctor: 0x241a1c, chef: 0x241d13 }[careerId] || 0x1b1d33;
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
    props.push({ size: [2.2, 1.1, 1], pos: [-3, 0.55, -2] }); // bàn làm việc
    props.push({ size: [1.2, 0.9, 0.1], pos: [-3, 1.3, -2.4] }); // màn hình
  } else if (careerId === "doctor") {
    props.push({ size: [2, 0.6, 1], pos: [3, 0.3, 2] }); // giường bệnh
    props.push({ size: [0.6, 1, 0.6], pos: [4.2, 0.5, 1.2] }); // xe đẩy
  } else if (careerId === "chef") {
    props.push({ size: [2, 0.9, 0.8], pos: [-2, 0.45, 3] }); // bếp
    props.push({ size: [1.4, 0.8, 0.8], pos: [2.5, 0.4, -2.5] }); // bàn bếp
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

export function initGame3D({ containerId, careerId, accentColor, steps, submitUrl, onSubmitted }) {
  const container = document.getElementById(containerId);
  const hudCount = document.getElementById("hud-count");
  const hudTotal = document.getElementById("hud-total");
  const hudPrompt = document.getElementById("hud-prompt");
  const actionBtn = document.getElementById("action-btn");
  hudTotal.textContent = steps.length;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x14162b);
  scene.fog = new THREE.Fog(0x14162b, 14, 30);

  const camera = new THREE.PerspectiveCamera(55, 1, 0.1, 100);

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.shadowMap.enabled = true;
  container.appendChild(renderer.domElement);

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

    return {
      step,
      position: new THREE.Vector3(x, 0, z),
      mesh: ring,
      label,
      done: false,
    };
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

  const loader = new GLTFLoader();
  loader.load(
    CHARACTER_MODEL_URL,
    (gltf) => {
      scene.remove(character);
      character = gltf.scene;
      character.scale.setScalar(1.0);
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
    () => {
      // Không tải được model (mạng chặn CDN, v.v.) — dùng nhân vật đơn giản dựng bằng khối hình
      character = buildFallbackCharacter();
      scene.add(character);
    }
  );

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

    // Camera theo sau nhân vật (góc nhìn thứ ba)
    const camOffset = new THREE.Vector3(0, 5.5, 8).applyAxisAngle(new THREE.Vector3(0, 1, 0), 0);
    const desiredCamPos = character.position.clone().add(camOffset);
    camera.position.lerp(desiredCamPos, 0.08);
    camera.lookAt(character.position.clone().add(new THREE.Vector3(0, 1.2, 0)));

    // Cập nhật vị trí nhãn hotspot trên màn hình 2D
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
