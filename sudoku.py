import tkinter as tk
import sudoku_solver
from app import App
from config import *


def main():
    root = tk.Tk()
    root.geometry(f'{str(W)}x{str(H)}')
    root.tk.eval('tk::PlaceWindow . center')
    root.resizable(False, False)
    root.iconbitmap("img/sdk.ico")
    root.title('Sudoku Solver')
    sudoku_solver.restart()
    app = App(root)
    canvas = app.create_canvas(W, H, '#969696')
    canvas.pack(fill=tk.BOTH, expand=True)
    app.create_grid()
    app.board_text('Custom board')
    app.load_board('Board')
    app.show_answers('Solve Board')
    app.hide_answers('Hide Answers')
    app.clear_board('Clear Board')
    app.edit_board('Edit Board')
    app.info_button()
    app.github_button()
    app.mainloop()


if __name__ == '__main__':
    print('~~~~~~~~Sudoku Solver~~~~~~~~')
    print('https://github.com/xbandrade/sudoku-solver')
    main()
