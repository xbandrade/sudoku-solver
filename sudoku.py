import tkinter as tk
import tkinter.tix as tix
import sudoku_solver
from app import App
from config import *


def main():
    root = tix.Tk()
    root.tk.eval(f'tk::PlaceWindow . center')
    sudoku_solver.clear_b()
    root.geometry(f'{str(W)}x{str(H)}')
    root.title('Sudoku')
    root.resizable(False, False)
    app = App(root)
    canvas = app.create_canvas(W, H, '#8895AF')
    app.draw_grid()
    app.insert_text(f'Custom board', MARGIN+BOARD_SIZE+SQUARE_SIZE, SQUARE_SIZE)
    app.board_buttons('Board')  # TODO: make this a dropdown list
    app.answers_buttons('Hide Answers', SQUARE_SIZE * 2.3, width=11, btn=1)
    app.answers_buttons('Solve Board', width=11, btn=2)
    app.clear_board('Clear Board', width=11)
    app.board_edit('Edit Board', width=11)
    app.info_button()
    app.github_button()
    # Add image to button
    canvas.pack(fill=tk.BOTH, expand=True)
    app.mainloop()


if __name__ == '__main__':
    print('~~~~~~~~Sudoku Solver~~~~~~~~')
    print('https://github.com/xbandrade/sudokuSolver')
    main()
