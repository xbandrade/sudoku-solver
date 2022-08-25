import tkinter as tk
import sudokuSolver
import sudokuLists
from tkinter import messagebox
from config import *
from idlelib.tooltip import Hovertip


def clear_answers(app):
    print(f'Hiding answers...')
    for p in range(9):
        for q in range(9):
            if sudokuSolver.board_start[p][q] == 0:
                app.entries[9 * p + q].delete(0, tk.END)


def edit_board(app):
    print(f'Making board fixed numbers editable...')
    for p in range(81):
        app.entries[p].config(state='normal', fg='#3C0238')
    messagebox.showinfo(title='Success', message='All cells are now editable!')


def clear_entries(app):
    print('Clearing board...')
    app.custom_board = True
    app.custom_solved = False
    sudokuSolver.clear_b()
    app.canvas.delete('txt')
    for p in range(81):
        app.entries[p].config(state='normal', fg='#3C0238')
        app.entries[p].delete(0, tk.END)
    app.insert_text(f'Custom board', margin + board_size + square_size, square_size)


def solve_board(app):
    """Solves the current board"""
    for p in range(9):
        for q in range(9):
            n = app.entries[9 * p + q].get()
            sudokuSolver.board[p][q] = int(n) if n != '' else 0
    sudokuSolver.board_start = [row[:] for row in sudokuSolver.board]
    sudokuSolver.solver()
    return not any([sudokuSolver.board[i][j] == 0 for i in range(9) for j in range(9)])


def show_answers(app):
    print(f'Showing answers...')
    if not solve_board(app):
        messagebox.showinfo(title='Error', message='Failed to solve the board!')
        return
    for p in range(9):
        for q in range(9):
            if (p, q) in sudokuLists.empty_start:
                app.entries[9 * p + q].config(state='normal', fg='#209138')
                app.entries[9 * p + q].insert(0, sudokuSolver.board[p][q])
            else:
                app.entries[9 * p + q].config(state='readonly', fg='#3C0238')


def button_click(app, p, q):
    board_number = q + 1 if p == 0 else q + 6
    app.custom_board = False
    app.custom_solved = False
    # for i in range(81):
    #     app.entries[i].config(state='normal')
    # app.entries = []
    sudokuSolver.clear_b()
    app.canvas.delete('txt')
    app.insert_text(f'Sudoku board #{board_number}', margin + board_size + square_size, square_size)
    try:
        with open('boards/b' + str(board_number) + '.dat', 'r') as file:
            sudokuSolver.board = [[int(x) for x in line.split(' ')] for line in file]
        sudokuSolver.board_start = [row[:] for row in sudokuSolver.board]
        file.close()
    except IOError:
        print("Couldn't open the file\n")
        exit(1)
    for p in range(9):
        for q in range(9):
            app.entries[9 * p + q].config(state='normal')
            app.entries[9 * p + q].delete(0, tk.END)
            if (p, q) not in sudokuLists.empty_start:
                app.entries[9 * p + q].insert(0, sudokuSolver.board[p][q])
                app.entries[9 * p + q].config(state='readonly', fg='#3C0238')
    print(f'\nBoard #{board_number} loaded!')


def validate(k):
    """Only integers from 1 to 9 can be entered."""
    if len(k) == 0:
        return True
    elif len(k) == 1 and k.isdigit():
        try:
            digit = int(k)
            assert digit != 0, 'invalid number 0'
            if 1 <= digit <= 9:
                return True
        except (ValueError, AssertionError):  # as e:
            # print(f'Invalid entry: {e}')
            return False
    else:
        return False


class App(tk.Frame):
    def __init__(self, master=None, canvas=None):
        super().__init__(master)
        self.master = master
        self.canvas = canvas
        self.entries = []
        self.custom_board = True
        self.custom_solved = False

    def create_canvas(self, canvas_width, canvas_height, bg_color):
        self.canvas = tk.Canvas(self.master, width=canvas_width, height=canvas_height, bg=bg_color)
        return self.canvas

    def draw_grid(self, start_board=False):
        board = sudokuSolver.board if not start_board else sudokuSolver.board_start
        if len(board) == 0 or board is None:
            print('Failed to read the board!\n')
            return
        empty_board = all([board[i][j] == 0 for i in range(9) for j in range(9)])
        for a, row in enumerate(range(0 + margin, board_size + margin, square_size)):
            for b, col in enumerate(range(0 + margin, board_size + margin, square_size)):
                bgcolor = '#BFBFBF' if sudokuLists.box_position[(a, b)] % 2 == 0 else '#A0A0A0'
                fgcolor = '#209138' if (a, b) in sudokuLists.empty_start else '#3E3E3E'
                vcmd = (self.canvas.register(validate), '%P')
                temp = tk.Entry(self.canvas, justify='center', bg=bgcolor, fg=fgcolor, font='Verdana 15',
                                readonlybackground=bgcolor, validate='key', validatecommand=vcmd)
                temp.place(x=col, y=row, width=square_size, height=square_size)  # <<<<<<<<<<
                if board[a][b] != 0:
                    temp.insert(0, str(board[a][b]))
                if (a, b) not in sudokuLists.empty_start and not empty_board:
                    temp.config(state='readonly')
                self.entries.append(temp)

    def insert_text(self, text, pos_x, pos_y):
        self.canvas.create_text(pos_x + 3 * pos_y, pos_y * 0.8, text=text, font='Verdana 13', tag='txt')

    def answers_buttons(self, text, posx=0, posy=0, width=6, height=1, btn=1):
        button = tk.Button(self.canvas, text=f'{text}', height=height, width=width)
        if btn == 1:
            button.config(command=lambda: clear_answers(self))
            Hovertip(button, 'Hide answers of the current board')
        elif btn == 2:
            button.config(command=lambda: show_answers(self))
            Hovertip(button, 'Solve the current board')
        button.place(x=board_size + 1.3 * square_size + posx, y=3.7 * square_size + posy)

    def clear_board(self, text, posx=0, posy=0, width=11, height=1):
        button = tk.Button(self.canvas, text=f'{text}', height=height, width=width,
                           command=lambda: clear_entries(self))
        Hovertip(button, 'Clear all entries')
        button.place(x=board_size + 1.3 * square_size + posx, y=5 * square_size + posy)

    def board_edit(self, text, posx=0, posy=0, width=11, height=1):
        button = tk.Button(self.canvas, text=f'{text}', height=height, width=width,
                           command=lambda: edit_board(self))
        Hovertip(button, 'Make all cells editable')
        button.place(x=board_size + 3.6 * square_size + posx, y=5 * square_size + posy)

    def board_buttons(self, text, width=6, height=1):
        btn = []
        for p in range(2):
            for q in range(5):
                btn.append(tk.Button(self.canvas, text=f'{text} {q + 1 if p == 0 else q + 6}',
                                     command=lambda m=p, n=q: button_click(self, m, n),
                                     height=height, width=width))
                btn[q if p == 0 else q + 5].place(x=board_size + 1.3 * square_size * (q + 1),
                                                  y=1.3 * square_size * (p + 1))
