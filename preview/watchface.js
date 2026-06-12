const WIDTH = 336;
const HEIGHT = 480;
const BOOT_TEXT = "Hello world!";
const BOOT_DURATION = 3000;
const REVEAL_DURATION = 850;

const palette = {
  black: "#000000",
  green: "#42f58d",
  dimGreen: "#13733e",
  ghost: "rgba(66, 245, 141, 0.16)",
  text: "#dfffe9",
  muted: "#679b78",
  scan: "rgba(66, 245, 141, 0.055)"
};

const glyphs = {
  " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
  "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
  ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
  ":": ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
  ">": ["10000", "01000", "00100", "00010", "00100", "01000", "10000"],
  "/": ["00001", "00010", "00100", "01000", "10000", "00000", "00000"],
  "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
  "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
  "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
  "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
  "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
  "5": ["11111", "10000", "10000", "11110", "00001", "00001", "11110"],
  "6": ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
  "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
  "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
  "9": ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],
  A: ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
  B: ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
  C: ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
  D: ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
  E: ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
  F: ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
  H: ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
  I: ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
  L: ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
  M: ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
  O: ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
  P: ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
  R: ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
  S: ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
  T: ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
  W: ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
  Y: ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
  a: ["00000", "01110", "00001", "01111", "10001", "10011", "01101"],
  b: ["10000", "10000", "10110", "11001", "10001", "10001", "11110"],
  c: ["00000", "00000", "01111", "10000", "10000", "10000", "01111"],
  d: ["00001", "00001", "01101", "10011", "10001", "10001", "01111"],
  e: ["00000", "01110", "10001", "11111", "10000", "10000", "01111"],
  f: ["00110", "01001", "01000", "11100", "01000", "01000", "01000"],
  h: ["10000", "10000", "10110", "11001", "10001", "10001", "10001"],
  i: ["00100", "00000", "01100", "00100", "00100", "00100", "01110"],
  l: ["01100", "00100", "00100", "00100", "00100", "00100", "01110"],
  n: ["00000", "00000", "10110", "11001", "10001", "10001", "10001"],
  o: ["00000", "00000", "01110", "10001", "10001", "10001", "01110"],
  p: ["00000", "00000", "11110", "10001", "11110", "10000", "10000"],
  r: ["00000", "00000", "10110", "11001", "10000", "10000", "10000"],
  s: ["00000", "00000", "01111", "10000", "01110", "00001", "11110"],
  t: ["01000", "01000", "11110", "01000", "01000", "01001", "00110"],
  w: ["00000", "00000", "10001", "10001", "10101", "10101", "01010"]
};

const canvas = document.getElementById("watchface");
const ctx = canvas.getContext("2d");
const restartButton = document.getElementById("restart");
const toggleButton = document.getElementById("toggle");
const downloadButton = document.getElementById("download");

let startedAt = performance.now();
let paused = false;
let pausedAt = 0;
let animationFrame = 0;

function easeOutCubic(t) {
  return 1 - Math.pow(1 - t, 3);
}

function easeInOutCubic(t) {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function clear() {
  ctx.fillStyle = palette.black;
  ctx.fillRect(0, 0, WIDTH, HEIGHT);
}

function drawScanlines(alpha = 1) {
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.fillStyle = palette.scan;
  for (let y = 0; y < HEIGHT; y += 6) {
    ctx.fillRect(0, y, WIDTH, 1);
  }
  ctx.restore();
}

function textWidth(text, size, gap = 1) {
  let width = 0;
  for (const char of text) {
    const glyph = glyphs[char] || glyphs[" "];
    width += glyph[0].length * size + gap * size;
  }
  return Math.max(0, width - gap * size);
}

function drawPixelText(text, x, y, options = {}) {
  const size = options.size || 4;
  const gap = options.gap ?? 1;
  const color = options.color || palette.green;
  const alpha = options.alpha ?? 1;
  const glow = options.glow ?? true;

  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.fillStyle = color;
  if (glow) {
    ctx.shadowColor = color;
    ctx.shadowBlur = options.shadowBlur ?? 9;
  }

  let cursor = x;
  for (const char of text) {
    const glyph = glyphs[char] || glyphs[" "];
    for (let row = 0; row < glyph.length; row += 1) {
      for (let col = 0; col < glyph[row].length; col += 1) {
        if (glyph[row][col] === "1") {
          ctx.fillRect(
            Math.round(cursor + col * size),
            Math.round(y + row * size),
            Math.max(1, size - 1),
            Math.max(1, size - 1)
          );
        }
      }
    }
    cursor += glyph[0].length * size + gap * size;
  }

  ctx.restore();
}

function drawSystemNoise(progress) {
  ctx.save();
  ctx.globalAlpha = 0.25 * (1 - progress);
  ctx.fillStyle = palette.dimGreen;
  for (let i = 0; i < 24; i += 1) {
    const x = (i * 53 + Math.floor(progress * 100)) % WIDTH;
    const y = (i * 31 + 19) % HEIGHT;
    ctx.fillRect(x, y, 1, 1);
  }
  ctx.restore();
}

function drawBoot(elapsed) {
  const progress = clamp(elapsed / BOOT_DURATION, 0, 1);
  const chars = Math.min(BOOT_TEXT.length, Math.max(1, Math.ceil(progress * BOOT_TEXT.length)));
  const phaseProgress = (progress * BOOT_TEXT.length) % 1;
  const text = BOOT_TEXT.slice(0, chars);
  const size = 5;
  const gap = 0;
  const y = 214;
  const finalWidth = textWidth(BOOT_TEXT, size, gap);
  const currentWidth = textWidth(text, size, gap);
  const targetX = (WIDTH - finalWidth) / 2;
  const centerX = (WIDTH - currentWidth) / 2;
  const x = centerX + (targetX - centerX) * easeOutCubic(progress);

  clear();
  drawScanlines(0.9);
  drawSystemNoise(progress);

  ctx.save();
  ctx.globalAlpha = 0.28;
  drawPixelText("$ boot --face", 38, 48, { size: 3, color: palette.dimGreen, shadowBlur: 4 });
  drawPixelText("init display...", 38, 70, { size: 3, color: palette.dimGreen, shadowBlur: 4 });
  ctx.restore();

  drawPixelText(text, x, y, { size, gap, color: palette.green, shadowBlur: 13 });

  const cursorX = x + currentWidth + size * 2;
  const cursorAlpha = chars === BOOT_TEXT.length ? (Math.sin(elapsed / 95) > 0 ? 1 : 0.3) : 0.9;
  ctx.save();
  ctx.globalAlpha = cursorAlpha;
  ctx.fillStyle = palette.green;
  ctx.shadowColor = palette.green;
  ctx.shadowBlur = 12;
  ctx.fillRect(Math.round(cursorX), y, size - 1, size * 7 - 1);
  ctx.restore();

  if (phaseProgress < 0.18 && chars > 1) {
    ctx.save();
    ctx.globalAlpha = 0.28 * (1 - phaseProgress / 0.18);
    drawPixelText(BOOT_TEXT.slice(0, chars - 1), x + 2, y, { size, gap, color: palette.green, shadowBlur: 6 });
    ctx.restore();
  }
}

function drawTerminalLine(label, value, y, alpha = 1) {
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.font = "14px Consolas, Cascadia Mono, monospace";
  ctx.textBaseline = "top";
  ctx.textAlign = "left";
  ctx.fillStyle = palette.green;
  ctx.shadowColor = palette.green;
  ctx.shadowBlur = 7;
  ctx.fillText(">", 34, y - 1);
  ctx.shadowBlur = 0;
  ctx.fillStyle = palette.muted;
  ctx.fillText(label, 54, y - 1);
  ctx.fillStyle = palette.text;
  ctx.textAlign = "right";
  ctx.fillText(value, 300, y - 1);
  ctx.restore();
}

function drawBattery(x, y, value, alpha) {
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.strokeStyle = palette.green;
  ctx.lineWidth = 2;
  ctx.shadowColor = palette.green;
  ctx.shadowBlur = 6;
  ctx.strokeRect(x, y, 32, 14);
  ctx.fillStyle = palette.green;
  ctx.fillRect(x + 34, y + 4, 3, 6);
  ctx.fillRect(x + 3, y + 3, Math.round(26 * value), 8);
  ctx.restore();
}

function drawMain(elapsed, revealProgress = 1) {
  const reveal = easeInOutCubic(clamp(revealProgress, 0, 1));
  const now = new Date();
  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  const weekdays = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];
  const dateLine = `${weekdays[now.getDay()]} ${month}.${day}`;
  const bootAlpha = 1 - reveal;

  clear();
  drawScanlines(0.75);

  if (bootAlpha > 0.01) {
    const bootWidth = textWidth(BOOT_TEXT, 5, 0);
    drawPixelText(BOOT_TEXT, (WIDTH - bootWidth) / 2, 206 - reveal * 72, {
      size: 5,
      gap: 0,
      color: palette.green,
      alpha: bootAlpha,
      shadowBlur: 12
    });
  }

  ctx.save();
  ctx.globalAlpha = reveal;
  drawPixelText("BOOTFACE", 34, 42, { size: 3, color: palette.dimGreen, shadowBlur: 5 });

  ctx.font = "72px Consolas, Cascadia Mono, monospace";
  ctx.textBaseline = "top";
  ctx.textAlign = "center";
  ctx.fillStyle = palette.text;
  ctx.shadowColor = "rgba(66, 245, 141, 0.38)";
  ctx.shadowBlur = 14;
  ctx.fillText(`${hours}:${minutes}`, WIDTH / 2, 116);

  ctx.shadowBlur = 0;
  ctx.font = "17px Consolas, Cascadia Mono, monospace";
  ctx.fillStyle = palette.green;
  ctx.fillText(dateLine, WIDTH / 2, 202);

  ctx.strokeStyle = palette.ghost;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(34, 244);
  ctx.lineTo(302, 244);
  ctx.stroke();

  drawTerminalLine("steps", "8234", 270, reveal);
  drawTerminalLine("heart", "72 bpm", 304, reveal);
  drawTerminalLine("weather", "26C", 338, reveal);
  drawTerminalLine("batt", "86%", 372, reveal);
  drawBattery(34, 420, 0.86, reveal);

  ctx.font = "12px Consolas, Cascadia Mono, monospace";
  ctx.fillStyle = palette.muted;
  ctx.textAlign = "right";
  ctx.fillText("/usr/time/live", 302, 421);

  const blink = Math.sin(elapsed / 420) > 0 ? 1 : 0.25;
  ctx.globalAlpha = reveal * blink;
  ctx.fillStyle = palette.green;
  ctx.shadowColor = palette.green;
  ctx.shadowBlur = 6;
  ctx.fillRect(34, 448, 9, 2);
  ctx.restore();
}

function drawFrame(totalElapsed) {
  if (totalElapsed < BOOT_DURATION) {
    drawBoot(totalElapsed);
    return;
  }

  const revealElapsed = totalElapsed - BOOT_DURATION;
  drawMain(totalElapsed, clamp(revealElapsed / REVEAL_DURATION, 0, 1));
}

function loop(now) {
  if (!paused) {
    drawFrame(now - startedAt);
    animationFrame = requestAnimationFrame(loop);
  }
}

function restart() {
  cancelAnimationFrame(animationFrame);
  startedAt = performance.now();
  paused = false;
  toggleButton.textContent = "Pause";
  animationFrame = requestAnimationFrame(loop);
}

function togglePause() {
  if (paused) {
    const pausedDuration = performance.now() - pausedAt;
    startedAt += pausedDuration;
    paused = false;
    toggleButton.textContent = "Pause";
    animationFrame = requestAnimationFrame(loop);
  } else {
    paused = true;
    pausedAt = performance.now();
    toggleButton.textContent = "Resume";
    cancelAnimationFrame(animationFrame);
  }
}

function downloadCurrentFrame() {
  const link = document.createElement("a");
  link.download = "bootface-current.png";
  link.href = canvas.toDataURL("image/png");
  link.click();
}

restartButton.addEventListener("click", restart);
toggleButton.addEventListener("click", togglePause);
downloadButton.addEventListener("click", downloadCurrentFrame);

window.BootfacePreview = {
  drawFrame,
  width: WIDTH,
  height: HEIGHT,
  bootDuration: BOOT_DURATION,
  revealDuration: REVEAL_DURATION
};

restart();
