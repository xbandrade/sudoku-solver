# #️⃣ Sudoku Solver
### **Sudoku Solver in Python**

#### ❕Fill in the grid with a sudoku problem or choose a board from the dropdown menu, then click the Solve Board button.
#### ❕You can also generate a random board with Easy, Medium, Hard, Expert or Evil difficulty, or read a sudoku board from an image using the hidden Load Image button.

&nbsp; <img src="https://raw.githubusercontent.com/xbandrade/sudoku-solver/master/img/ocrboard.png" width=60% height=60%> <img src="https://raw.githubusercontent.com/xbandrade/sudoku-solver/master/img/board.webp" width=28% height=28%>


### ➡️ Setup 
```pip install -r requirements.txt```

```python -m sudoku```


### ➡️ Sudoku Solver and Generator 
Sudoku solving techniques implemented:
- Naked single, pair, triple and quad
- Hidden single, pair, triple and quad
- Locked candidates
- X-wing
- XY-wing

### ➡️ Interface Buttons and Options
- `Load Board` Load a default board from the dropdown menu list
- `Generate` Generate a new board with the selected difficulty 
- `Solve Board` Try solving the current board
- `Hide Answers` Hide all answers if the board has been solved
- `Clear Board` Start a new empty sudoku board
- `Edit Board` Make all cells editable
- `Load Image [hidden]` Read a sudoku board from an image using Google's Tesseract OCR. Press `F3` to reveal this button


### ❕Info

- If these techniques can't fully solve the problem, the Dancing Links technique will be used to efficiently solve it. A sudoku board with less than 17 filled cells will always be solved by Dancing Links.

- If the board you are trying to solve is invalid, the invalid cells will be highlighted in red and you can edit them.

&nbsp; <img src="https://raw.githubusercontent.com/xbandrade/sudoku-solver/master/img/invalid.png" width=60% height=60%>

- Please be aware that the `Load Image` function may fail to recognize some cells or even the entire board from an image depending on the image quality.

- The Sudoku board generator was implemented by randomly filling the main diagonal boxes and solving the rest with the Dancing Links technique, then removing some cells according to the chosen difficulty.

- The solver keeps track of every technique used, so an option to show a step-by-step solution can be implemented in the future.

&nbsp; <img src="https://raw.githubusercontent.com/xbandrade/sudoku-solver/master/img/solved.png" width=60% height=60%>

### ➡️ Libraries
- tkinter
- NumPy
- pillow
- OpenCV
- pytesseract

Read more about the Dancing Links technique on [this Wikipedia article](https://en.wikipedia.org/wiki/Dancing_Links).
