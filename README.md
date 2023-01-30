# Sudoku Solver
### **Sudoku Solver in Python**

Fill in the grid with a sudoku problem or choose a board from the dropdown menu, then click the Solve Board button.

### ➡️ Run 
***python -m sudoku***

Sudoku solving techniques implemented:
> - Naked single, pair, triple and quad
> - Hidden single, pair, triple and quad
> - Locked candidates
> - X-wing
> - XY-wing

If these techniques can't fully solve the problem, the Dancing Links technique will be used to efficiently solve it.

A 'Load Image' option was implemented to read a sudoku board from a picture using Google's Tesseract OCR.

The idea is to keep track of every technique used and create the option to show a step-by-step solution.

### ➡️ Libraries
- tkinter
- NumPy
- pillow
- OpenCV
- pytesseract
