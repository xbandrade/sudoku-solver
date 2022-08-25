import tkinter as tk
import tkinter.tix as tix
import sudokuSolver
from app import App
from config import *
# from glob import glob


def main():
    # arr = [f for f in glob('boards/b*.dat')]
    root = tix.Tk()
    root.tk.eval(f'tk::PlaceWindow . center')
    # root.withdraw()
    sudokuSolver.clear_b()
    root.geometry(f'{str(w)}x{str(h)}')
    root.title('Sudoku')
    root.resizable(False, False)
    app = App(root)
    canvas = app.create_canvas(w, h, '#8895AF')
    app.draw_grid()
    app.insert_text(f'Custom board', margin+board_size+square_size, square_size)
    app.board_buttons('Board')  # TODO: make this a dropdown list
    app.answers_buttons('Hide Answers', square_size * 2.3, width=11, btn=1)
    app.answers_buttons('Solve Board', width=11, btn=2)
    app.clear_board('Clear Board', width=11)
    app.board_edit('Edit Board', width=11)
    app.info_button()
    app.github_button()
    # Add image to button
    canvas.pack(fill=tk.BOTH, expand=True)
    # root.deiconify()
    app.mainloop()


if __name__ == '__main__':
    print('~~~~~~~~Sudoku Solver~~~~~~~~')
    print('https://github.com/xbandrade/sudokuSolver')
    main()
