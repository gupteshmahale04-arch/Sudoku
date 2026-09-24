
# 🧩 Sudoku Master: Terminal Solver & Interactive Web App

A dual-interface Python Sudoku project featuring a command-line solver using NumPy and Tabulate alongside a modern, responsive web application built with Streamlit, HTML5, CSS Grid, and an automated backtracking solver[cite: 67, 68].

---

## 📋 Table of Contents
* [Overview](#-overview)
* [Key Features](#-key-features)
* [How It Works](#-how-it-works)
  * [Terminal Grid & Sum Verification](#terminal-grid--sum-verification)
  * [Recursive Backtracking Algorithm](#recursive-backtracking-algorithm)
* [Installation & Setup](#-installation--setup)
* [Usage](#-usage)
  * [1. Streamlit Web Application](#1-streamlit-web-application)
  * [2. Terminal CLI Solver](#2-terminal-cli-solver)
* [Keyboard Shortcuts & UI Controls](#-keyboard-shortcuts--ui-controls)
* [📂 File Directory](#-file-directory)

---

## 🔍 Overview
**Sudoku Master** bridges traditional terminal script execution with modern web interactivity[cite: 67, 68]. Users can either solve the puzzle manually using pen, paper, and terminal input or play directly inside a polished dark-themed browser interface equipped with real-time conflict highlights, pencil notes, a live timer, and instant backtracking auto-solve functionality[cite: 67, 68].

---

## ✨ Key Features
* **Interactive Web UI:** Embedded single-page application built using Streamlit components, CSS Grid, and custom JavaScript[cite: 68].
* **Intelligent Backtracking Engine:** Recursive depth-first search solver capable of validating moves and auto-completing the puzzle instantly[cite: 68].
* **Real-Time Conflict Detection:** Automatically highlights conflicting duplicates across rows, columns, and 3×3 subgrids[cite: 68].
* **Pencil Notes Mode:** Enter candidate numbers (1–9) inside empty cells to track possibilities[cite: 68].
* **Responsive Visual Feedback:** Same-value highlighting, row/column/box focus guides, live stopwatch, and victory confetti animations[cite: 68].
* **Terminal Script Verification:** CLI alternative displaying grid states with `tabulate` and validating row and column sums via NumPy array slicing[cite: 67].

---

## 🧠 How It Works

### Terminal Grid & Sum Verification
The CLI script initializes the 9×9 board as a NumPy matrix where clues are fixed integers and unknowns are labeled alphabetically (`A` through `AQ`)[cite: 67]. Once user values are collected via dictionary mappings, it runs row and column checks:

$$\sum_{j=1}^{9} \text{Row}_{i,j} = 45 \quad \text{and} \quad \sum_{i=1}^{9} \text{Col}_{i,j} = 45$$

Any row or column that does not sum to 45 is flagged for correction[cite: 67].

### Recursive Backtracking Algorithm
The web application leverages recursive backtracking to solve or validate any valid Sudoku board[cite: 68]:
1. Find the next empty cell `(r, c)`[cite: 68].
2. Test numbers from `1` through `9`[cite: 68].
3. Validate if placement is safe (no duplicates in row `r`, column `c`, or the $3 \times 3$ sub-box)[cite: 68].
4. Place the candidate number and recursively attempt to solve the remaining board[cite: 68].
5. If no number leads to a solution, reset the cell (`0`) and backtrack to the previous cell[cite: 68].

```javascript
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

```

---

## 🚀 Installation & Setup

1. **Clone the repository:**
```bash
git clone [https://github.com/your-username/sudoku-master.git](https://github.com/your-username/sudoku-master.git)
cd sudoku-master

```


2. **Install required dependencies:**
```bash
pip install streamlit numpy tabulate

```



---

## 🖥️ Usage

### 1. Streamlit Web Application

Launch the interactive web portal in your browser:

```bash
streamlit run app.py

```

*Features:*

* Click any non-clue cell to select it.


* Use on-screen keypads or your keyboard to input numbers.


* Click **Validate** to check your completed solution against the backtrack solver.


* Click **Auto-Solve** to watch the algorithm instantly finish the puzzle.



---

### 2. Terminal CLI Solver

Run the console script to view the grid with letter placeholders and enter values sequentially:

```bash
python main.py

```

* Prompts you to input numbers for placeholders `A` through `AQ`.


* Formats and prints the final board using `tabulate`.


* Identifies and logs specific rows or columns containing errors.



---

## ⌨️ Keyboard Shortcuts & UI Controls

| Key / Control | Functionality |
| --- | --- |
| **`1` – `9**` | Fill selected cell with number (or toggle pencil candidate in Notes mode).|
| **`Backspace` / `Delete**` | Clear value or notes from the selected cell.|
| **`N` / `n**` | Toggle **Pencil Notes** mode ON / OFF.|
| **`Arrow Keys`** | Navigate between grid cells.|
| **Erase Button** | Clear user input from the active cell.|
| **Validate Button** | Check your completed grid for accuracy.|
| **Auto-Solve Button** | Compute and render the verified solution automatically. |

---

## 📂 File Directory

* **`app.py`**: Streamlit application delivering the HTML5/CSS3/JavaScript responsive Sudoku board, real-time conflict highlights, pencil notation, and backtracking solver.


* **`main.py`**: Console application utilizing NumPy arrays and `tabulate` to display the game board, collect variable inputs, and evaluate row/column sum criteria.




