# Sudoku Solver
### **Sudoku Solver in Python**

Fill in the grid with a sudoku problem or choose a board from the dropdown menu, then click the Solve Board button.

### ➡️ Run 
***python -m sudoku***


### ➡️ Sudoku Solver and Generator 
Sudoku solving techniques implemented:
- Naked single, pair, triple and quad
- Hidden single, pair, triple and quad
- Locked candidates
- X-wing
- XY-wing

If these techniques can't fully solve the problem, the Dancing Links technique will be used to efficiently solve it.

A 'Load Image' option was implemented to read a sudoku board from a picture using Google's Tesseract OCR.

A Sudoku board generator was implemented by randomly filling the main diagonal boxes and solving the rest with the Dancing Links technique, then removing some cells according to the chosen difficulty.

The solver keeps track of every technique used, so an option to show a step-by-step solution can be implemented.

### ➡️ Libraries
- tkinter
- NumPy
- pillow
- OpenCV
- pytesseract
