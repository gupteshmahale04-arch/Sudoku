import numpy as np
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Sudoku Master Web App",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Streamlit container styling to remove margins and center the UI
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 1000px;
    }
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

sudoku_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sudoku Master</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
<style>
  :root {
    --bg: #0f172a;
    --card: #1e293b;
    --border: #334155;
    --primary: #6366f1;
    --primary-light: #818cf8;
    --text: #f8fafc;
    --muted: #94a3b8;
    --clue-color: #38bdf8;
    --user-color: #f1f5f9;
    --cell-bg: #1e293b;
    --cell-selected: rgba(99, 102, 241, 0.4);
    --cell-highlight: rgba(99, 102, 241, 0.15);
    --cell-same-val: rgba(56, 189, 248, 0.25);
    --cell-error: rgba(239, 68, 68, 0.35);
    --grid-outer: #6366f1;
    --grid-thick: #64748b;
    --grid-thin: #334155;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: transparent;
    color: var(--text);
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    padding: 10px;
  }

  .game-container {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 20px 40px -15px rgba(0,0,0,0.5);
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 580px;
    width: 100%;
  }

  .header {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
  }
  .title-wrap h1 {
    font-size: 1.5rem;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .timer-pill {
    background: rgba(255,255,255,0.06);
    border: 1px solid var(--border);
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: var(--clue-color);
  }

  /* 9x9 Sudoku Board */
  .board {
    display: grid;
    grid-template-columns: repeat(9, 1fr);
    width: 100%;
    max-width: 450px;
    aspect-ratio: 1;
    border: 3px solid var(--grid-outer);
    border-radius: 12px;
    overflow: hidden;
    background: var(--border);
    gap: 1px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
  }

  .cell {
    background: var(--cell-bg);
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.5rem;
    font-weight: 700;
    cursor: pointer;
    position: relative;
    transition: background 0.12s ease;
  }

  /* 3x3 Box Thick Borders */
  .cell:nth-child(3n) { border-right: 2px solid var(--grid-thick); }
  .cell:nth-child(9n) { border-right: none; }
  .cell:nth-child(n+19):nth-child(-n+27),
  .cell:nth-child(n+46):nth-child(-n+54) {
    border-bottom: 2px solid var(--grid-thick);
  }

  .cell.clue { color: var(--clue-color); font-weight: 800; }
  .cell.user-filled { color: var(--user-color); }
  .cell.selected { background: var(--cell-selected) !important; outline: 2px solid var(--primary-light); z-index: 2; }
  .cell.highlighted { background: var(--cell-highlight); }
  .cell.same-val { background: var(--cell-same-val); font-weight: 800; }
  .cell.conflict { background: var(--cell-error) !important; color: #f87171 !important; }

  /* Pencil Notes Mini-Grid */
  .notes-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(3, 1fr);
    width: 100%;
    height: 100%;
    pointer-events: none;
  }
  .notes-grid span {
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--muted);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* Controls & Action Buttons */
  .toolbar {
    width: 100%;
    max-width: 450px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-top: 16px;
  }
  .tool-btn {
    background: rgba(255,255,255,0.06);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 10px;
    border-radius: 10px;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    transition: all 0.15s ease;
  }
  .tool-btn:hover { background: rgba(255,255,255,0.12); }
  .tool-btn.active {
    background: var(--primary);
    border-color: var(--primary-light);
    color: #fff;
  }

  /* On-screen Keypad */
  .keypad {
    display: grid;
    grid-template-columns: repeat(9, 1fr);
    gap: 6px;
    width: 100%;
    max-width: 450px;
    margin-top: 14px;
  }
  .key-btn {
    background: #243247;
    border: 1px solid var(--border);
    color: var(--text);
    aspect-ratio: 1;
    border-radius: 10px;
    font-size: 1.25rem;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .key-btn:hover {
    background: var(--primary);
    transform: translateY(-2px);
  }

  .status-msg {
    margin-top: 14px;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--clue-color);
    height: 20px;
    text-align: center;
  }
</style>
</head>
<body>

<div class="game-container">
  <div class="header">
    <div class="title-wrap">
      <h1>🧩 Sudoku Master</h1>
    </div>
    <div class="timer-pill" id="timer">⏱️ 00:00</div>
  </div>

  <!-- 9x9 Board -->
  <div class="board" id="board"></div>

  <div class="status-msg" id="status-msg">Select a cell to begin</div>

  <!-- Keypad (1-9) -->
  <div class="keypad">
    <button class="key-btn" onclick="handleInput(1)">1</button>
    <button class="key-btn" onclick="handleInput(2)">2</button>
    <button class="key-btn" onclick="handleInput(3)">3</button>
    <button class="key-btn" onclick="handleInput(4)">4</button>
    <button class="key-btn" onclick="handleInput(5)">5</button>
    <button class="key-btn" onclick="handleInput(6)">6</button>
    <button class="key-btn" onclick="handleInput(7)">7</button>
    <button class="key-btn" onclick="handleInput(8)">8</button>
    <button class="key-btn" onclick="handleInput(9)">9</button>
  </div>

  <!-- Action Bar -->
  <div class="toolbar">
    <button class="tool-btn" id="notes-btn" onclick="toggleNotes()">
      <span>✏️ Notes</span>
      <span id="notes-status" style="font-size:0.7rem; color:var(--muted)">OFF</span>
    </button>
    <button class="tool-btn" onclick="eraseCell()">
      <span>🗑️ Erase</span>
      <span style="font-size:0.7rem; color:var(--muted)">Clear</span>
    </button>
    <button class="tool-btn" onclick="checkPuzzle()">
      <span>🔍 Validate</span>
      <span style="font-size:0.7rem; color:var(--muted)">Check</span>
    </button>
    <button class="tool-btn" onclick="autoSolve()">
      <span>⚡ Auto-Solve</span>
      <span style="font-size:0.7rem; color:var(--muted)">Instant</span>
    </button>
  </div>
</div>

<script>
  // Initial puzzle configuration from user's code
  const INITIAL = [
    [0, 4, 2, 0, 5, 0, 0, 0, 6],
    [1, 9, 7, 0, 0, 0, 0, 4, 0],
    [5, 6, 0, 4, 0, 0, 1, 0, 9],
    [8, 0, 1, 3, 0, 0, 2, 6, 0],
    [9, 0, 0, 0, 7, 1, 0, 4, 5],
    [0, 3, 0, 2, 5, 6, 0, 0, 0],
    [0, 5, 0, 3, 2, 0, 7, 0, 0],
    [0, 4, 0, 5, 9, 0, 6, 0, 0],
    [0, 0, 7, 0, 6, 0, 0, 8, 0]
  ];

  let boardState = JSON.parse(JSON.stringify(INITIAL));
  let notesState = Array.from({length: 9}, () => Array.from({length: 9}, () => new Set()));
  let selected = { r: null, c: null };
  let notesMode = false;
  let seconds = 0;
  let timerInterval = null;

  function initTimer() {
    timerInterval = setInterval(() => {
      seconds++;
      const m = String(Math.floor(seconds / 60)).padStart(2, '0');
      const s = String(seconds % 60).padStart(2, '0');
      document.getElementById('timer').innerText = `⏱️ ${m}:${s}`;
    }, 1000);
  }

  function renderBoard() {
    const boardEl = document.getElementById('board');
    boardEl.innerHTML = '';

    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        const val = boardState[r][c];
        const isClue = INITIAL[r][c] !== 0;
        const cell = document.createElement('div');
        cell.className = 'cell';
        if (isClue) cell.classList.add('clue');
        else if (val !== 0) cell.classList.add('user-filled');

        // Selection & Highlighting
        if (selected.r === r && selected.c === c) cell.classList.add('selected');
        else if (selected.r === r || selected.c === c || 
                (Math.floor(selected.r/3) === Math.floor(r/3) && Math.floor(selected.c/3) === Math.floor(c/3))) {
          cell.classList.add('highlighted');
        }

        if (selected.r !== null && val !== 0 && val === boardState[selected.r][selected.c]) {
          cell.classList.add('same-val');
        }

        if (val !== 0) {
          cell.innerText = val;
        } else if (notesState[r][c].size > 0) {
          const notesDiv = document.createElement('div');
          notesDiv.className = 'notes-grid';
          for (let n = 1; n <= 9; n++) {
            const span = document.createElement('span');
            span.innerText = notesState[r][c].has(n) ? n : '';
            notesDiv.appendChild(span);
          }
          cell.appendChild(notesDiv);
        }

        cell.onclick = () => selectCell(r, c);
        boardEl.appendChild(cell);
      }
    }
  }

  function selectCell(r, c) {
    selected = { r, c };
    renderBoard();
  }

  function handleInput(num) {
    if (selected.r === null || selected.c === null) return;
    const { r, c } = selected;
    if (INITIAL[r][c] !== 0) return; // clue is read-only

    if (notesMode) {
      if (notesState[r][c].has(num)) notesState[r][c].delete(num);
      else notesState[r][c].add(num);
      boardState[r][c] = 0;
    } else {
      boardState[r][c] = (boardState[r][c] === num) ? 0 : num;
      notesState[r][c].clear();
      checkConflicts();
    }
    renderBoard();
  }

  function eraseCell() {
    if (selected.r === null || selected.c === null) return;
    const { r, c } = selected;
    if (INITIAL[r][c] !== 0) return;
    boardState[r][c] = 0;
    notesState[r][c].clear();
    renderBoard();
  }

  function toggleNotes() {
    notesMode = !notesMode;
    const btn = document.getElementById('notes-btn');
    const status = document.getElementById('notes-status');
    btn.classList.toggle('active', notesMode);
    status.innerText = notesMode ? 'ON' : 'OFF';
  }

  function checkConflicts() {
    const cells = document.querySelectorAll('.cell');
    cells.forEach(el => el.classList.remove('conflict'));

    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        const val = boardState[r][c];
        if (val === 0) continue;

        // Check row and col duplicates
        for (let i = 0; i < 9; i++) {
          if (i !== c && boardState[r][i] === val) markConflict(r, c);
          if (i !== r && boardState[i][c] === val) markConflict(r, c);
        }
        // Check 3x3 box
        const br = Math.floor(r / 3) * 3;
        const bc = Math.floor(c / 3) * 3;
        for (let i = 0; i < 3; i++) {
          for (let j = 0; j < 3; j++) {
            const nr = br + i;
            const nc = bc + j;
            if ((nr !== r || nc !== c) && boardState[nr][nc] === val) {
              markConflict(r, c);
            }
          }
        }
      }
    }
  }

  function markConflict(r, c) {
    const idx = r * 9 + c;
    const cells = document.querySelectorAll('.cell');
    if (cells[idx]) cells[idx].classList.add('conflict');
  }

  // Keyboard navigation & inputs
  window.addEventListener('keydown', (e) => {
    if (selected.r === null) return;
    let { r, c } = selected;

    if (e.key >= '1' && e.key <= '9') handleInput(parseInt(e.key));
    else if (e.key === 'Backspace' || e.key === 'Delete') eraseCell();
    else if (e.key === 'n' || e.key === 'N') toggleNotes();
    else if (e.key === 'ArrowUp') selectCell((r + 8) % 9, c);
    else if (e.key === 'ArrowDown') selectCell((r + 1) % 9, c);
    else if (e.key === 'ArrowLeft') selectCell(r, (c + 8) % 9);
    else if (e.key === 'ArrowRight') selectCell(r, (c + 1) % 9);
  });

  // Backtracking Solver
  function isSafe(grid, r, c, val) {
    for (let i = 0; i < 9; i++) {
      if (grid[r][i] === val || grid[i][c] === val) return false;
    }
    const br = Math.floor(r / 3) * 3;
    const bc = Math.floor(c / 3) * 3;
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 3; j++) {
        if (grid[br + i][bc + j] === val) return false;
      }
    }
    return true;
  }

  function solve(grid) {
    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        if (grid[r][c] === 0) {
          for (let v = 1; v <= 9; v++) {
            if (isSafe(grid, r, c, v)) {
              grid[r][c] = v;
              if (solve(grid)) return true;
              grid[r][c] = 0;
            }
          }
          return false;
        }
      }
    }
    return true;
  }

  function autoSolve() {
    let copy = JSON.parse(JSON.stringify(INITIAL));
    if (solve(copy)) {
      boardState = copy;
      notesState = Array.from({length: 9}, () => Array.from({length: 9}, () => new Set()));
      renderBoard();
      document.getElementById('status-msg').innerText = "✨ Solved with Backtracking Engine!";
      confetti({ particleCount: 80, spread: 60 });
    }
  }

  function checkPuzzle() {
    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        if (boardState[r][c] === 0) {
          document.getElementById('status-msg').innerText = "⚠️ Fill all empty cells first!";
          return;
        }
      }
    }
    let copy = JSON.parse(JSON.stringify(INITIAL));
    solve(copy);
    let correct = true;
    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        if (boardState[r][c] !== copy[r][c]) correct = false;
      }
    }

    if (correct) {
      document.getElementById('status-msg').innerText = "🎉 All correct! Puzzle Completed!";
      confetti({ particleCount: 150, spread: 80 });
    } else {
      document.getElementById('status-msg').innerText = "❌ Some numbers are incorrect or duplicated!";
      checkConflicts();
    }
  }

  // Init
  initTimer();
  renderBoard();
</script>
</body>
</html>
"""

# Render the application seamlessly in Streamlit
components.html(sudoku_html, height=840, scrolling=False)