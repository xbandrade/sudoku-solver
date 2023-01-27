import tkinter as tk
import sudoku_solver
import sudoku_lists
import webbrowser
from tkinter import messagebox
from config import *
from idlelib.tooltip import Hovertip


def open_url():
    print(f'Opening github repository...')
    webbrowser.open_new_tab('https://github.com/xbandrade/sudoku-solver')


def info():
    print(f'Showing info...')
    text = ['Sudoku Solver',
            'Fill in the grid with a sudoku problem or choose',
            'a board, then click the Solve Board button.',
            'Available techniques:',
            '- Naked and hidden: Singles, pairs, triples, quads',
            '- Locked candidates',
            '- X-wing',
            '- XY-wing',
            ]
    messagebox.showinfo(title='Info', message='\n'.join(text))


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
        except (ValueError, AssertionError):
            return False
    else:
        return False


class App(tk.Frame):
    def __init__(self, master=None, canvas=None):
        super().__init__(master)
        self.master = master
        self.canvas = canvas
        self.selected_board = None
        self.entries = []
        self.value_inside = tk.StringVar(self.canvas)
        self.img = tk.PhotoImage(file='img/github.png')
        self.info = tk.PhotoImage(file='img/info.png')

    def create_canvas(self, canvas_width, canvas_height, bg_color):
        self.canvas = tk.Canvas(self.master, width=canvas_width, height=canvas_height, bg=bg_color)
        return self.canvas

    def create_grid(self):
        board = sudoku_solver.board
        if not board:
            print('Failed to load the board!\n')
            return
        for a, row in enumerate(range(MARGIN, BOARD_SIZE + MARGIN, CELL_SIZE)):
            for b, col in enumerate(range(MARGIN, BOARD_SIZE + MARGIN, CELL_SIZE)):
                bgcolor = '#BFBFBF' if (a // 3 * 3 + b // 3) % 2 == 0 else '#A0A0A0'
                fgcolor = '#3C0238'
                vcmd = (self.canvas.register(validate), '%P')
                entry = tk.Entry(self.canvas, justify='center', bg=bgcolor, fg=fgcolor, font='Verdana 15',
                                 readonlybackground=bgcolor, validate='key', validatecommand=vcmd)
                entry.place(x=col, y=row, width=CELL_SIZE, height=CELL_SIZE)
                self.entries.append(entry)

    def dropdown_selection(self, selection):
        self.selected_board = selection

    def board_text(self, text):
        pos_x, pos_y =  H + (W - H) // 2, CELL_SIZE // 2
        self.canvas.create_text(pos_x, pos_y, text=text, font='Verdana 13', tag='txt', anchor='center')

    def solve_board(self):
        """Solves the current board"""
        for p in range(9):
            for q in range(9):
                n = self.entries[9 * p + q].get()
                sudoku_solver.board[p][q] = int(n) if n != '' else 0
        sudoku_solver.board_start = [row[:] for row in sudoku_solver.board]
        # is_valid, msg = sudoku_solver.solver()
        # return not any([sudoku_solver.board[i][j] == 0 for i in range(9) for j in range(9)])
        return sudoku_solver.solver()

    def show_answers_cmd(self):
        board_solved, msg = self.solve_board()
        if not board_solved:
            messagebox.showinfo(title='Error', message=msg, icon='error')
            return
        print(f'Showing answers...\n')
        for p in range(9):
            for q in range(9):
                if (p, q) in sudoku_lists.empty_start:
                    self.entries[9 * p + q].config(state='normal', fg='#209138')
                    self.entries[9 * p + q].insert(0, sudoku_solver.board[p][q])
                else:
                    self.entries[9 * p + q].config(state='readonly', fg='#3C0238')

    def show_answers(self, text, width=11, height=1):
        pos_x, pos_y =  H + (W - H) // 6, CELL_SIZE * 3
        button = tk.Button(self.canvas, text=f'{text}', height=height, width=width, anchor='center')
        button.config(command=self.show_answers_cmd)
        Hovertip(button, 'Solve the current board')
        button.place(x=pos_x, y=pos_y)

    def hide_answers_cmd(self):
        print(f'Hiding answers...\n')
        for p in range(9):
            for q in range(9):
                if sudoku_solver.board_start[p][q] == 0:
                    self.entries[9 * p + q].delete(0, tk.END)

    def hide_answers(self, text, width=11, height=1):
        pos_x, pos_y =  H + 3 * (W - H) // 6, CELL_SIZE * 3
        button = tk.Button(self.canvas, text=f'{text}', height=height, width=width, anchor='center')
        button.config(command=self.hide_answers_cmd)
        Hovertip(button, 'Hide answers of the current board')
        button.place(x=pos_x, y=pos_y)

    def clear_board_cmd(self):
        print('Clearing board...\n')
        sudoku_solver.restart()
        self.canvas.delete('txt')
        for p in range(81):
            self.entries[p].config(state='normal', fg='#3C0238')
            self.entries[p].delete(0, tk.END)
        self.board_text(f'Custom board')
        self.value_inside.set('Custom')

    def clear_board(self, text, width=11, height=1):
        pos_x, pos_y =  H + (W - H) // 6, CELL_SIZE * 4
        button = tk.Button(self.canvas, text=f'{text}', height=height, width=width,
                           command=self.clear_board_cmd)
        Hovertip(button, 'Clear all entries')
        button.place(x=pos_x, y=pos_y)

    def edit_board_cmd(self):
        print(f'Making board fixed numbers editable...\n')
        for p in range(81):
            self.entries[p].config(state='normal', fg='#3C0238')
        messagebox.showinfo(title='Success', message='All cells are now editable!')

    def edit_board(self, text, width=11, height=1):
        pos_x, pos_y =  H + 3 * (W - H) // 6, CELL_SIZE * 4
        button = tk.Button(self.canvas, text=f'{text}', height=height, width=width,
                           command=self.edit_board_cmd)
        Hovertip(button, 'Make all cells editable')
        button.place(x=pos_x, y=pos_y)

    def button_click(self):
        board_number = int(self.selected_board[-2:])
        sudoku_solver.restart()
        self.canvas.delete('txt')
        self.board_text(f'Sudoku board #{board_number}')
        try:
            with open('boards/b' + str(board_number) + '.dat', 'r') as file:
                sudoku_solver.board = [[int(x) for x in line.split(' ')] for line in file]
            sudoku_solver.board_start = [row[:] for row in sudoku_solver.board]
        except IOError:
            print("Couldn't open the file\n")
            exit(1)
        for p in range(9):
            for q in range(9):
                self.entries[9 * p + q].config(state='normal', fg='#3C0238')
                self.entries[9 * p + q].delete(0, tk.END)
                if sudoku_solver.board_start[p][q] != 0:
                    self.entries[9 * p + q].insert(0, sudoku_solver.board[p][q])
                    self.entries[9 * p + q].config(state='readonly')
        print(f'\nBoard #{board_number} loaded!')

    def load_board(self, text):
        pos_x1, pos_x2, pos_y =  H + (W - H) // 3, H + 2 * (W - H) // 3, CELL_SIZE * 1.5
        b_list = [f'{text} {x}' for x in range(1, 11)]
        self.value_inside.set('Custom')
        dropdown = tk.OptionMenu(self.canvas, self.value_inside, *b_list, command=self.dropdown_selection)
        dropdown.place(x=pos_x1, y=pos_y, anchor='center')
        load_button = tk.Button(self.canvas, text='Load Board', command=self.button_click)
        load_button.place(x=pos_x2, y=pos_y, anchor='center')
        Hovertip(load_button, 'Load the selected board')

    def info_button(self, text='Info', width=32, height=32):
        button = tk.Button(self.canvas, text=f'{text}', height=height, width=width,
                           command=lambda: info(), image=self.info)
        button.place(x=W-80, y=H-40)

    def github_button(self):
        button = tk.Button(self.canvas, image=self.img, command=open_url)
        Hovertip(button, 'Go to GitHub repository')
        button.place(x=W-40, y=H-40)
