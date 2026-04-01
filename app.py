import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Snake Game</title>
<style>
body{
    background:black;
    color:lime;
    font-family:monospace;
    text-align:center;
    margin:0;
    min-height:100vh;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:20px;
    box-sizing:border-box;
    overflow:hidden;
}

h1{
    margin:0 0 14px 0;
    width:400px;
    text-align:center;
    transition: transform 0.08s linear, opacity 0.08s linear, filter 0.08s linear;
}

.page{
    width:100%;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
}

.game-area{
    width:400px;
    display:flex;
    flex-direction:column;
    align-items:center;
    transition: transform 0.08s linear, opacity 0.08s linear, filter 0.08s linear;
}

canvas{
    background:#111;
    border:3px solid lime;
    margin-bottom:10px;
    max-width:100%;
    height:auto;
    transition: transform 0.06s linear, filter 0.06s linear, opacity 0.06s linear;
}

.info{
    margin-bottom:10px;
}

.controls p{
    margin:2px 0;
}

.note{
    margin-top:12px;
    font-size:14px;
    color:#8f8;
}

.preview-controls{
    margin-top:14px;
    display:flex;
    flex-direction:column;
    align-items:center;
    gap:10px;
}

.preview-controls label{
    color:lime;
    font-size:16px;
}

.preview-controls select, .mode-button{
    background:#111;
    color:lime;
    border:2px solid lime;
    font-family:monospace;
    font-size:15px;
    padding:6px 10px;
    cursor:pointer;
}

.mode-button{
    margin-top:12px;
    width:240px;
}

.glitch-on body,
.glitch-on{
    cursor:crosshair;
}
</style>
</head>
<body>
<div id="bsod" style="display:none; position:fixed; inset:0; width:100vw; height:100vh; background:#0078d7; color:white; z-index:999999; font-family:'Segoe UI Light','Segoe UI',Arial,sans-serif; box-sizing:border-box; overflow:hidden;">
  <div style="position:absolute; left:10vw; top:14vh; right:10vw; text-align:left;">
    <div style="font-size:120px; line-height:0.9; font-weight:300; margin-bottom:48px;">:(</div>
    <div style="font-size:32px; line-height:1.35; max-width:760px; font-weight:300; margin-bottom:42px;">
      Your PC ran into a problem and needs to restart. We're<br>
      just collecting some error info, and then we'll restart for<br>
      you.
    </div>
    <div style="font-size:28px; line-height:1.2; font-weight:300; margin-bottom:56px;">200% complete</div>
    <div style="display:flex; align-items:flex-start; gap:18px;">
      <div style="width:92px; height:92px; background:white; display:flex; align-items:center; justify-content:center; overflow:hidden;">
        <img src="https://api.qrserver.com/v1/create-qr-code/?size=92x92&data=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DdQw4w9WgXcQ" alt="QR code to Rick Astley video" style="width:92px; height:92px; display:block;">
      </div>
      <div style="font-size:14px; line-height:1.9; font-weight:300; max-width:760px;">
        For more information about this issue and possible fixes, visit windows.com/stopcode
        <br><br>
        If you call a support person, give them this info:
        <br>
        Stop code: SNAKE_GLITCH_OVERFLOW
      </div>
    </div>
  </div>
</div>

<div class="page">
  <h1 id="titleText">Snake Game</h1>

  <div class="game-area" id="gameArea">
    <div class="info">
      <h2>Score: <span id="score">0</span></h2>
      <h2>High Score: <span id="highScore">0</span></h2>
      <p>Speed Level: <span id="speedLevel">2</span></p>
      <p>Pass-Through Walls: <span id="ghostMode">OFF</span></p>
      <p>Status: <span id="gameStatus">READY</span></p>
      <p>Glitch Mode: <span id="glitchModeStatus">OFF</span></p>
      <p>Corruption: <span id="glitchLevelText">0% / 200%</span></p>
      <p id="glitchAvoidRow" style="display:none;">Auto-Avoid Walls While Glitching: <span id="glitchAvoidStatus">OFF</span></p>
    </div>

    <canvas id="game" width="400" height="400"></canvas>

    <div class="preview-controls">
      <label for="themeSelect">Snake Color:</label>
      <select id="themeSelect" onchange="applySelectedTheme()">
        <option value="#00FF00">Green</option>
        <option value="#FF0000">Red</option>
        <option value="#0000FF">Blue</option>
        <option value="#FFFF00">Yellow</option>
        <option value="#FF00FF">Magenta</option>
        <option value="#00FFFF">Cyan</option>
        <option value="#FFA500">Orange</option>
        <option value="#800080">Purple</option>
        <option value="#008000">Dark Green</option>
        <option value="#FFC0CB">Pink</option>
        <option value="rainbow-turn">Random Every Turn</option>
      </select>
    </div>

    <button id="glitchAvoidButton" class="mode-button" onclick="toggleGlitchAvoidWalls()" style="display:none;">Glitch Wall Avoidance: OFF (V)</button>

    <div class="controls">
      <p>Start / Restart: R key</p>
      <p>Move: Arrow Keys or WASD</p>
      <p>Speed Level: 1, 2, 3 keys</p>
      <p>Toggle Ghost Mode: 0 key</p>
      <p>Pause/Resume: P key</p>
      <p>Toggle Glitch Mode: B key</p>
      <p>Toggle Auto-Avoid Walls While Glitching: V key</p>
      <p>Hide BSOD: F11</p>
    </div>

    <p class="note">High score is stored locally in the browser. While glitch mode is on, wall avoidance makes the snake turn away from walls instead of passing through them.</p>
  </div>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const glitchAvoidButton = document.getElementById("glitchAvoidButton");
const titleText = document.getElementById("titleText");
const gameArea = document.getElementById("gameArea");
const bsod = document.getElementById("bsod");

const grid = 20;
let count = 0;
let speed = 2;
let ghostMode = false;
let paused = true;
let gameOver = false;
let started = false;

let snakeHeadColor = "#00FF00";
let snakeBodyColor = "#32CD32";
let rainbowTurnMode = false;

let glitchMode = false;
let glitchLevel = 0;
let glitchTicks = 0;
let glitchFlash = 0;
let fakeStatusFlip = false;
let visualOffsetX = 0;
let visualOffsetY = 0;
let lastRealStatus = "READY";
let glitchAvoidWalls = false;
let bsodActive = false;

const speedThresholds = {
  1: 7,
  2: 6,
  3: 5
};

const defaultSnake = () => ({
  x: 160,
  y: 200,
  dx: grid,
  dy: 0,
  cells: [
    {x: 160, y: 200},
    {x: 140, y: 200},
    {x: 120, y: 200}
  ],
  maxCells: 3
});

let snake = defaultSnake();

let apple = {
  x: 240,
  y: 200
};

let score = 0;
let highScore = Number(localStorage.getItem("snakeHighScore") || 0);

document.getElementById("highScore").innerText = highScore;
document.getElementById("themeSelect").value = snakeHeadColor;

function updateStatusText(text){
  lastRealStatus = text;
  if (!fakeStatusFlip){
    document.getElementById("gameStatus").innerText = text;
  }
}

function updateGlitchUI(){
  document.getElementById("glitchModeStatus").innerText = glitchMode ? "ON" : "OFF";
  document.getElementById("glitchLevelText").innerText = `${Math.round(glitchLevel * 100)}% / 200%`;
  document.getElementById("glitchAvoidStatus").innerText = glitchAvoidWalls ? "ON" : "OFF";
  document.getElementById("glitchAvoidRow").style.display = glitchMode ? "block" : "none";
  glitchAvoidButton.style.display = glitchMode ? "inline-block" : "none";
  glitchAvoidButton.textContent = `Glitch Wall Avoidance: ${glitchAvoidWalls ? "ON" : "OFF"} (V)`;
}

function toggleGlitchAvoidWalls(){
  if (!glitchMode || bsodActive) return;
  glitchAvoidWalls = !glitchAvoidWalls;
  updateGlitchUI();
}

function clearVisualGlitchEffects(){
  document.body.classList.remove("glitch-on");
  canvas.style.transform = "translate(0px, 0px)";
  canvas.style.filter = "none";
  canvas.style.opacity = "1";
  gameArea.style.transform = "translate(0px, 0px)";
  gameArea.style.filter = "none";
  gameArea.style.opacity = "1";
  titleText.style.transform = "translate(0px, 0px)";
  titleText.style.filter = "none";
  titleText.style.opacity = "1";
}

function hideBSOD(){
  bsod.style.display = "none";
  bsodActive = false;
}

function resetGlitchState(){
  glitchLevel = 0;
  glitchTicks = 0;
  glitchFlash = 0;
  fakeStatusFlip = false;
  visualOffsetX = 0;
  visualOffsetY = 0;
  glitchAvoidWalls = false;
  clearVisualGlitchEffects();
  hideBSOD();
  document.getElementById("gameStatus").innerText = lastRealStatus;
  updateGlitchUI();
}

function toggleGlitchMode(){
  if (bsodActive) return;
  glitchMode = !glitchMode;
  if (glitchMode){
    document.body.classList.add("glitch-on");
    glitchLevel = 0;
    glitchTicks = 0;
    glitchFlash = 0;
    fakeStatusFlip = false;
    glitchAvoidWalls = false;
  } else {
    resetGlitchState();
  }
  updateGlitchUI();
}

function getRandomInt(min, max){
  return Math.floor(Math.random() * (max - min)) + min;
}

function setSpeed(level){
  speed = level;
  document.getElementById("speedLevel").innerText = level;
}

function toggleGhost(){
  if (bsodActive) return;
  ghostMode = !ghostMode;
  document.getElementById("ghostMode").innerText = ghostMode ? "ON" : "OFF";
}

function togglePause(){
  if (!started || gameOver || bsodActive) return;
  paused = !paused;
  updateStatusText(paused ? "PAUSED" : "RUNNING");
}

function setHighScore(){
  if (score > highScore){
    highScore = score;
    localStorage.setItem("snakeHighScore", String(highScore));
    document.getElementById("highScore").innerText = highScore;
  }
}

function placeApple(){
  apple.x = getRandomInt(0, 20) * grid;
  apple.y = getRandomInt(0, 20) * grid;
}

function drawStartScreen(message = "Press R to Start"){
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#111";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = snakeBodyColor;
  ctx.fillRect(120, 200, grid - 1, grid - 1);
  ctx.fillRect(140, 200, grid - 1, grid - 1);

  ctx.fillStyle = snakeHeadColor;
  ctx.fillRect(160, 200, grid - 1, grid - 1);

  drawPreviewEyes();

  ctx.fillStyle = "red";
  ctx.fillRect(240, 200, grid - 1, grid - 1);

  if (glitchMode && glitchLevel > 0.2 && Math.random() < glitchLevel * 0.5){
    ctx.fillStyle = randomColor();
    ctx.fillRect(getRandomInt(0, canvas.width - 20), getRandomInt(0, canvas.height - 20), 20, 20);
  }

  ctx.fillStyle = glitchMode && Math.random() < glitchLevel * 0.4 ? randomColor() : "lime";
  ctx.font = "28px monospace";
  ctx.textAlign = "center";
  ctx.fillText(glitchMode && glitchLevel > 0.65 && Math.random() < 0.25 ? "SN4KE" : "SNAKE", canvas.width / 2, 120);

  ctx.font = "18px monospace";
  ctx.fillText(message, canvas.width / 2, 155);

  ctx.font = "16px monospace";
  ctx.fillText("Arrow Keys or WASD to Move", canvas.width / 2, 300);
  ctx.fillText("1 / 2 / 3 = Speed   0 = Ghost Mode", canvas.width / 2, 325);
  ctx.fillText("P = Pause   B = Glitch Mode   V = Glitch Avoid", canvas.width / 2, 350);
}

function drawPreviewEyes(){
  ctx.fillStyle = "black";
  ctx.fillRect(172, 204, 3, 3);
  ctx.fillRect(172, 212, 3, 3);
}

function startGame(){
  if (bsodActive) return;
  snake = defaultSnake();
  score = 0;
  count = 0;
  paused = false;
  gameOver = false;
  started = true;
  document.getElementById("score").innerText = score;
  updateStatusText("RUNNING");
  apple.x = 240;
  apple.y = 200;
}

function endGame(){
  setHighScore();
  paused = true;
  gameOver = true;
  started = false;
  updateStatusText("GAME OVER");
  drawStartScreen("Game Over - Press R to Restart");
}

function applySelectedTheme(){
  const selected = document.getElementById("themeSelect").value;
  setTheme(selected);
}

function randomColor(){
  const hue = Math.floor(Math.random() * 360);
  return `hsl(${hue}, 100%, 50%)`;
}

function lightenHexColor(hex, percent){
  let num = parseInt(hex.replace("#", ""), 16),
      r = (num >> 16) + percent,
      g = ((num >> 8) & 0x00FF) + percent,
      b = (num & 0x0000FF) + percent;

  r = (r > 255) ? 255 : r;
  g = (g > 255) ? 255 : g;
  b = (b > 255) ? 255 : b;

  return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

function cssToRgb(cssColor){
  const temp = document.createElement("div");
  temp.style.color = cssColor;
  document.body.appendChild(temp);
  const computed = getComputedStyle(temp).color;
  document.body.removeChild(temp);
  const matches = computed.match(/\d+/g);
  if (!matches || matches.length < 3) return [0, 255, 0];
  return [
    parseInt(matches[0], 10),
    parseInt(matches[1], 10),
    parseInt(matches[2], 10)
  ];
}

function lightenCssColor(cssColor, amount){
  const [r, g, b] = cssToRgb(cssColor);
  return `rgb(${Math.min(255, r + amount)}, ${Math.min(255, g + amount)}, ${Math.min(255, b + amount)})`;
}

function applyRandomTurnColor(){
  const color = randomColor();
  snakeHeadColor = color;
  snakeBodyColor = lightenCssColor(color, 50);
}

function setTheme(color){
  rainbowTurnMode = color === "rainbow-turn";
  if (rainbowTurnMode){
    applyRandomTurnColor();
  } else {
    snakeHeadColor = color;
    snakeBodyColor = lightenHexColor(color, 50);
  }

  const message = gameOver ? "Game Over - Press R to Restart" : "Press R to Start";
  if (!started || gameOver || paused){
    drawStartScreen(message);
  }
}

function drawSnakeEyes(x, y){
  ctx.fillStyle = "black";
  const eyeSize = 3;
  let eyes = [];

  if (snake.dx > 0){
    eyes = [{x: x + 12, y: y + 4}, {x: x + 12, y: y + 12}];
  } else if (snake.dx < 0){
    eyes = [{x: x + 4, y: y + 4}, {x: x + 4, y: y + 12}];
  } else if (snake.dy < 0){
    eyes = [{x: x + 4, y: y + 4}, {x: x + 12, y: y + 4}];
  } else {
    eyes = [{x: x + 4, y: y + 12}, {x: x + 12, y: y + 12}];
  }

  eyes.forEach(function(eye){
    ctx.fillRect(eye.x, eye.y, eyeSize, eyeSize);
  });
}

function applyVisualGlitchEffects(){
  if (!glitchMode || bsodActive){
    return;
  }

  const intensity = glitchLevel;
  const shakeRange = Math.max(0, Math.floor(intensity * 8));
  visualOffsetX = getRandomInt(-shakeRange, shakeRange + 1);
  visualOffsetY = getRandomInt(-shakeRange, shakeRange + 1);

  canvas.style.transform = `translate(${visualOffsetX}px, ${visualOffsetY}px)`;
  gameArea.style.transform = `translate(${Math.round(visualOffsetX * 0.35)}px, ${Math.round(visualOffsetY * 0.35)}px)`;
  titleText.style.transform = `translate(${Math.round(visualOffsetX * 0.2)}px, ${Math.round(visualOffsetY * 0.2)}px)`;

  const hue = Math.floor(Math.random() * 360);
  canvas.style.filter = intensity > 0.15 ? `hue-rotate(${Math.floor(intensity * 120)}deg) blur(${(intensity * 1.6).toFixed(2)}px)` : "none";
  gameArea.style.filter = intensity > 0.45 && Math.random() < intensity * 0.25 ? `drop-shadow(0 0 8px hsl(${hue}, 100%, 50%))` : "none";
  titleText.style.filter = intensity > 0.3 && Math.random() < intensity * 0.3 ? `drop-shadow(0 0 5px hsl(${hue}, 100%, 50%))` : "none";

  canvas.style.opacity = String(Math.max(0.72, 1 - intensity * 0.18));
  gameArea.style.opacity = String(Math.max(0.85, 1 - intensity * 0.10));
  titleText.style.opacity = String(Math.max(0.80, 1 - intensity * 0.12));

  if (intensity > 0.35 && Math.random() < intensity * 0.12){
    fakeStatusFlip = !fakeStatusFlip;
    document.getElementById("gameStatus").innerText = fakeStatusFlip ? "ERROR" : lastRealStatus;
  }

  if (glitchFlash > 0){
    glitchFlash--;
    ctx.fillStyle = randomColor();
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }
}

function willHitWall(x, y){
  return x < 0 || x >= canvas.width || y < 0 || y >= canvas.height;
}

function canMoveDirection(dx, dy){
  const nextX = snake.x + dx;
  const nextY = snake.y + dy;
  return !willHitWall(nextX, nextY);
}

function autoAvoidGlitchWalls(){
  if (!(glitchMode && glitchAvoidWalls) || bsodActive) return;

  const nextX = snake.x + snake.dx;
  const nextY = snake.y + snake.dy;
  if (!willHitWall(nextX, nextY)) return;

  const options = [
    {dx: grid, dy: 0},
    {dx: -grid, dy: 0},
    {dx: 0, dy: grid},
    {dx: 0, dy: -grid}
  ].filter(dir => {
    if (dir.dx === -snake.dx && dir.dy === -snake.dy) return false;
    return canMoveDirection(dir.dx, dir.dy);
  });

  if (options.length > 0){
    const pick = options[getRandomInt(0, options.length)];
    snake.dx = pick.dx;
    snake.dy = pick.dy;
    if (rainbowTurnMode){
      applyRandomTurnColor();
    }
  }
}

function triggerBSOD(){
  if (bsodActive) return;

  bsodActive = true;
  paused = true;
  started = false;
  gameOver = true;

  document.body.classList.remove("glitch-on");
  canvas.style.transform = "translate(0px, 0px)";
  canvas.style.filter = "none";
  canvas.style.opacity = "1";
  gameArea.style.transform = "translate(0px, 0px)";
  gameArea.style.filter = "none";
  gameArea.style.opacity = "1";
  titleText.style.transform = "translate(0px, 0px)";
  titleText.style.filter = "none";
  titleText.style.opacity = "1";

  bsod.style.display = "block";
  bsod.style.width = `${window.innerWidth}px`;
  bsod.style.height = `${window.innerHeight}px`;

  if (document.documentElement.requestFullscreen){
    document.documentElement.requestFullscreen().catch(() => {});
  }
}

function maybeAdvanceGlitch(){
  if (!glitchMode || !started || paused || gameOver || bsodActive) return;

  glitchTicks++;
  if (glitchTicks % 30 === 0){
    glitchLevel = Math.min(2, glitchLevel + 0.01875);
    updateGlitchUI();
    if (glitchLevel >= 2){
      triggerBSOD();
      return;
    }
  }

  if (glitchLevel > 0.15 && Math.random() < glitchLevel * 0.03){
    glitchFlash = 1;
  }
}

function loop(){
  requestAnimationFrame(loop);

  if (bsodActive) return;

  if (!started || paused || gameOver){
    if (glitchMode){
      applyVisualGlitchEffects();
    }
    return;
  }

  maybeAdvanceGlitch();

  let threshold = speedThresholds[speed];
  if (glitchMode && glitchLevel > 0){
    if (Math.random() < glitchLevel * 0.18){
      threshold += 1;
    }
    if (Math.random() < glitchLevel * 0.08){
      threshold += 2;
    }
  }

  if (++count < threshold){
    if (glitchMode){
      applyVisualGlitchEffects();
    }
    return;
  }
  count = 0;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (glitchMode && glitchLevel > 0.25 && Math.random() < glitchLevel * 0.08){
    const dirs = [
      {dx: grid, dy: 0},
      {dx: -grid, dy: 0},
      {dx: 0, dy: grid},
      {dx: 0, dy: -grid}
    ];
    const valid = dirs.filter(d => !(d.dx === -snake.dx && d.dy === -snake.dy));
    const pick = valid[getRandomInt(0, valid.length)];
    snake.dx = pick.dx;
    snake.dy = pick.dy;
  }

  autoAvoidGlitchWalls();

  snake.x += snake.dx;
  snake.y += snake.dy;

  if (glitchMode && glitchLevel > 0.45 && Math.random() < glitchLevel * 0.05){
    snake.x += (Math.random() < 0.5 ? -grid : grid);
  }
  if (glitchMode && glitchLevel > 0.45 && Math.random() < glitchLevel * 0.05){
    snake.y += (Math.random() < 0.5 ? -grid : grid);
  }

  if (ghostMode){
    if (snake.x < 0) snake.x = canvas.width - grid;
    else if (snake.x >= canvas.width) snake.x = 0;

    if (snake.y < 0) snake.y = canvas.height - grid;
    else if (snake.y >= canvas.height) snake.y = 0;
  } else {
    if (
      snake.x < 0 ||
      snake.x >= canvas.width ||
      snake.y < 0 ||
      snake.y >= canvas.height
    ){
      endGame();
      return;
    }
  }

  snake.cells.unshift({x: snake.x, y: snake.y});
  if (snake.cells.length > snake.maxCells) snake.cells.pop();

  let appleColor = "red";
  if (glitchMode && glitchLevel > 0.2 && Math.random() < glitchLevel * 0.2){
    appleColor = randomColor();
  }
  ctx.fillStyle = appleColor;
  ctx.fillRect(apple.x, apple.y, grid - 1, grid - 1);

  for (let index = 0; index < snake.cells.length; index++){
    const cell = snake.cells[index];

    let fillColor = index === 0 ? snakeHeadColor : snakeBodyColor;
    if (glitchMode && glitchLevel > 0.18 && Math.random() < glitchLevel * 0.12){
      fillColor = randomColor();
    }

    ctx.fillStyle = fillColor;
    ctx.fillRect(cell.x, cell.y, grid - 1, grid - 1);

    if (glitchMode && glitchLevel > 0.55 && Math.random() < glitchLevel * 0.07){
      ctx.strokeStyle = randomColor();
      ctx.strokeRect(cell.x + getRandomInt(-3, 4), cell.y + getRandomInt(-3, 4), grid - 1, grid - 1);
    }

    if (index === 0){
      drawSnakeEyes(cell.x, cell.y);
    }

    if (cell.x === apple.x && cell.y === apple.y){
      snake.maxCells++;
      score++;
      document.getElementById("score").innerText = score;
      setHighScore();
      placeApple();
    }

    for (let i = index + 1; i < snake.cells.length; i++){
      if (cell.x === snake.cells[i].x && cell.y === snake.cells[i].y){
        endGame();
        return;
      }
    }
  }

  if (glitchMode && glitchLevel > 0.5 && Math.random() < glitchLevel * 0.08 && snake.cells.length > 1){
    const ghostCell = snake.cells[Math.min(1, snake.cells.length - 1)];
    ctx.fillStyle = "rgba(255,255,255,0.35)";
    ctx.fillRect(ghostCell.x + getRandomInt(-10, 11), ghostCell.y + getRandomInt(-10, 11), grid - 1, grid - 1);
  }

  if (glitchMode && glitchLevel > 0.4 && Math.random() < glitchLevel * 0.12){
    for (let i = 0; i < Math.ceil(glitchLevel * 4); i++){
      ctx.fillStyle = randomColor();
      ctx.fillRect(getRandomInt(0, canvas.width), getRandomInt(0, canvas.height), getRandomInt(4, 25), getRandomInt(2, 12));
    }
  }

  applyVisualGlitchEffects();
}

function tryDirection(newDx, newDy, axis){
  if (!started || gameOver || bsodActive) return false;
  if (axis === "x" && snake.dx !== 0) return false;
  if (axis === "y" && snake.dy !== 0) return false;

  if (glitchMode && glitchLevel > 0.35 && Math.random() < glitchLevel * 0.14){
    return false;
  }

  snake.dx = newDx;
  snake.dy = newDy;
  if (rainbowTurnMode){
    applyRandomTurnColor();
  }
  return true;
}

document.addEventListener("keydown", function(e){
  if (e.key === "F11"){
    bsod.style.display = "none";
    bsodActive = false;
    if (document.fullscreenElement && document.exitFullscreen){
      document.exitFullscreen();
    }
    e.preventDefault();
    return;
  }

  if (bsodActive){
    return;
  }

  const key = e.key.toLowerCase();

  if (key === "b"){
    toggleGlitchMode();
    const message = gameOver ? "Game Over - Press R to Restart" : (started ? null : "Press R to Start");
    if (message){
      drawStartScreen(message);
    }
    return;
  }

  if (key === "v"){
    toggleGlitchAvoidWalls();
    return;
  }

  if (key === "r"){
    startGame();
    return;
  }

  if (key === "arrowleft" || key === "a"){
    tryDirection(-grid, 0, "x");
  }
  else if (key === "arrowup" || key === "w"){
    tryDirection(0, -grid, "y");
  }
  else if (key === "arrowright" || key === "d"){
    tryDirection(grid, 0, "x");
  }
  else if (key === "arrowdown" || key === "s"){
    tryDirection(0, grid, "y");
  }
  else if (key === "1"){
    setSpeed(1);
  }
  else if (key === "2"){
    setSpeed(2);
  }
  else if (key === "3"){
    setSpeed(3);
  }
  else if (key === "0"){
    toggleGhost();
  }
  else if (key === "p"){
    togglePause();
  }
});

window.addEventListener("resize", function(){
  if (bsodActive){
    bsod.style.width = `${window.innerWidth}px`;
    bsod.style.height = `${window.innerHeight}px`;
  }
});

applySelectedTheme();
resetGlitchState();
drawStartScreen("Press R to Start");
requestAnimationFrame(loop);
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Snake Game starting on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
