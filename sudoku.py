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
    sudoku_solver.clear_b()
    app = App(root)
    canvas = app.create_canvas(W, H, '#969696')
    app.draw_grid()
    app.insert_text('Custom board')
    app.load_board('Board')
    app.reveal_answers('Solve Board')
    app.hide_answers('Hide Answers')
    app.clear_board('Clear Board')
    app.board_edit('Edit Board')
    app.info_button()
    app.github_button()
    canvas.pack(fill=tk.BOTH, expand=True)
    app.mainloop()


if __name__ == '__main__':
    print('~~~~~~~~Sudoku Solver~~~~~~~~')
    print('https://github.com/xbandrade/sudoku-solver')
    main()
