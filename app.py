import tkinter as tk
import webbrowser
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import simpledialog as sd

import numpy as np
from idlelib.tooltip import Hovertip

import sudoku_generator
import sudoku_lists
import sudoku_solver
from config import *
from ocr import ocr


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
            'If the problem can\'t be solved by these techniques,',
            'the Dancing Links (DLX) technique will be used.',
            'A random problem can also be generated using the',
            'difficulty dropdown list.',
            '\n[!!] Press F3 to show the OCR Button. Be aware that this',
            'option can fail to recognize the grid numbers depending',
            'on the image quality.'
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
        self.diff = None
        self.entries = []
        self.value_inside = tk.StringVar(self.canvas)
        self.diff_inside = tk.StringVar(self.canvas)
        self.img = tk.PhotoImage(file='img/github.png')
        self.info = tk.PhotoImage(file='img/info.png')

    def create_canvas(self, canvas_width, canvas_height, bg_color):
        self.canvas = tk.Canvas(self.master, width=canvas_width, height=canvas_height, bg=bg_color)
        return self.canvas

    def create_grid(self):
        board = sudoku_solver.board
        if not board.size:
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

    def _dropdown_board(self, selection):
        self.selected_board = selection

    def _dropdown_diff(self, selection):
        self.diff = selection

    def board_text(self, text):
        pos_x, pos_y =  H + (W - H) // 2, CELL_SIZE // 2
        self.canvas.create_text(pos_x, pos_y, text=text, font='Verdana 13', tag='txt', anchor='center')

    def _change_color(self, entry, original):
        entry.config(bg='#FFCCCB')
        entry.after(2000, lambda: entry.config(bg=original))

    def solve_board(self):
        """Solves the current board"""
        for p in range(9):
            for q in range(9):
                n = self.entries[9 * p + q].get()
                sudoku_solver.board[p, q] = int(n) if n != '' else 0
        sudoku_solver.board_start = np.copy(sudoku_solver.board)
        return sudoku_solver.solver()

    def _show_answers_cmd(self):
        board_solved, msg = self.solve_board()
        if not board_solved.size:
            messagebox.showinfo(title='Error', message=msg, icon='error')
            pos = 9 * int(msg[-5]) + int(msg[-2])
            self._change_color(self.entries[pos], self.entries[pos].cget('bg'))
            return
        print(f'Showing answers...\n')
        for p in range(9):
            for q in range(9):
                if (p, q) in sudoku_lists.empty_start:
                    self.entries[9 * p + q].config(state='normal', fg='#209138')
                    self.entries[9 * p + q].insert(0, sudoku_solver.board[p, q])
                else:
                    self.entries[9 * p + q].config(state='readonly', fg='#3C0238')
        if msg:
            messagebox.showinfo(title='Solved', message=msg, icon='info')

    def show_answers(self, text, width=11, height=1):
        pos_x, pos_y =  H + (W - H) // 6, CELL_SIZE * 3.5
        button = tk.Button(self.canvas, text=f'{text}', height=height, width=width, anchor='center')
        button.config(command=self._show_answers_cmd)
        Hovertip(button, 'Solve the current board')
        button.place(x=pos_x, y=pos_y)

    def _hide_answers_cmd(self):
        print(f'Hiding answers...\n')
        for p in range(9):
            for q in range(9):
                if sudoku_solver.board_start[p, q] == 0:
                    self.entries[9 * p + q].delete(0, tk.END)

    def hide_answers(self, text, width=11, height=1):
        pos_x, pos_y =  H + 3 * (W - H) // 6, CELL_SIZE * 3.5
        button = tk.Button(self.canvas, text=f'{text}', height=height, width=width, anchor='center')
        button.config(command=self._hide_answers_cmd)
        Hovertip(button, 'Hide answers of the current board')
        button.place(x=pos_x, y=pos_y)

    def _clear_board_cmd(self):
        print('Clearing board...\n')
        sudoku_solver.restart()
        self.canvas.delete('txt')
        for p in range(81):
            self.entries[p].config(state='normal', fg='#3C0238')
            self.entries[p].delete(0, tk.END)
        self.board_text(f'Custom board')
        self.value_inside.set('Custom ')
        self.selected_board = None

    def clear_board(self, text, width=11, height=1):
        pos_x, pos_y =  H + (W - H) // 6, CELL_SIZE * 4.5
        button = tk.Button(self.canvas, text=f'{text}', height=height, width=width,
                           command=self._clear_board_cmd)
        Hovertip(button, 'Clear all entries')
        button.place(x=pos_x, y=pos_y)

    def _edit_board_cmd(self):
        print(f'Making board fixed numbers editable...\n')
        for p in range(81):
            self.entries[p].config(state='normal', fg='#3C0238')
        self.canvas.delete('txt')
        self.board_text(f'Custom board')
        messagebox.showinfo(title='Success', message='All cells are now editable!')

    def edit_board(self, text, width=11, height=1):
        pos_x, pos_y =  H + 3 * (W - H) // 6, CELL_SIZE * 4.5
        button = tk.Button(self.canvas, text=f'{text}', height=height, width=width,
                           command=self._edit_board_cmd)
        Hovertip(button, 'Make all cells editable')
        button.place(x=pos_x, y=pos_y)

    def _load_button_cmd(self):
        if not self.selected_board:
            messagebox.showinfo(title='Warning', message='Select a board from the list', icon='warning')
            return
        board_number = int(self.selected_board[-2:])
        sudoku_solver.restart()
        self.canvas.delete('txt')
        self.board_text(f'Sudoku board #{board_number}')
        try:
            sudoku_solver.board = np.loadtxt(f'boards/b{board_number}.dat', dtype=int)
            sudoku_solver.board_start = np.copy(sudoku_solver.board)
        except IOError:
            print("Couldn't open the file\n")
            exit(1)
        for p in range(9):
            for q in range(9):
                self.entries[9 * p + q].config(state='normal', fg='#3C0238')
                self.entries[9 * p + q].delete(0, tk.END)
                if sudoku_solver.board_start[p, q] != 0:
                    self.entries[9 * p + q].insert(0, sudoku_solver.board[p, q])
                    self.entries[9 * p + q].config(state='readonly')
        print(f'\nBoard #{board_number} loaded!')

    def load_board(self, text, width=11, height=1):
        pos_x1, pos_x2, pos_y =  H + (W - H) // 3, H + 2 * (W - H) // 3, CELL_SIZE * 1.5
        b_list = [f'{text} {x}' for x in range(1, 11)]
        self.value_inside.set('Custom ')
        dropdown = tk.OptionMenu(self.canvas, self.value_inside, *b_list, command=self._dropdown_board)
        dropdown.place(x=pos_x1, y=pos_y, anchor='center')
        load_button = tk.Button(self.canvas, text='Load Board', command=self._load_button_cmd, 
                                width=width, height=height)
        load_button.place(x=pos_x2, y=pos_y, anchor='center')
        Hovertip(load_button, 'Load the selected board')

    def _read_image_cmd(self):
        path = fd.askopenfilename()
        if not path or path[-4:] not in ('.png', '.jpg', 'jpeg', 'webp'):
            messagebox.showinfo(title='Error', message=r'Invalid file type', icon='error')
            return
        read_board = ocr(path)
        if read_board.size:
            sudoku_solver.board = read_board
            sudoku_solver.board_start = np.copy(sudoku_solver.board)     
            for p in range(9):
                for q in range(9):
                    self.entries[9 * p + q].config(state='normal', fg='#3C0238')
                    self.entries[9 * p + q].delete(0, tk.END)
                    if sudoku_solver.board_start[p, q] != 0:
                        self.entries[9 * p + q].insert(0, sudoku_solver.board[p, q])
                        self.entries[9 * p + q].config(state='readonly')
            print(f'\nImage board loaded!')
            messagebox.showinfo(title='Success', message='Sudoku board found!')    
        else:
            messagebox.showinfo(title='Error', message='Could not find a Sudoku board in the image', 
                                icon='error')
            
    def read_image(self, k, text='Load Image', width=12, height=1):
        _ = k
        pos_x, pos_y =  H + (W - H) // 3, CELL_SIZE * 5.5
        button = tk.Button(self.canvas, text=f'{text}', height=height, width=width,
                           command=self._read_image_cmd)
        Hovertip(button, 'Read a Sudoku problem from image')
        button.place(x=pos_x, y=pos_y)

    def _generate_board(self):
        if not self.diff:
            messagebox.showinfo(title='Warning', message='Select a difficulty from the list', icon='warning')
            return
        sudoku_solver.board = np.copy(sudoku_generator.generate(self.diff))
        sudoku_solver.board_start = np.copy(sudoku_solver.board)            
        for p in range(9):
            for q in range(9):
                self.entries[9 * p + q].config(state='normal', fg='#3C0238')
                self.entries[9 * p + q].delete(0, tk.END)
                if sudoku_solver.board_start[p, q] != 0:
                    self.entries[9 * p + q].insert(0, sudoku_solver.board[p, q])
                    self.entries[9 * p + q].config(state='readonly')
        print(f'\n{self.diff} board generated!')
    
    def generate_board(self, text, width=11, height=1):
        pos_x1, pos_x2, pos_y =  H + (W - H) // 3, H + 2 * (W - H) // 3, CELL_SIZE * 2.5
        diff_list = ['Easy', 'Medium', 'Hard', 'Expert', 'Evil', 'Random']
        self.diff_inside.set('Difficulty')
        dropdown = tk.OptionMenu(self.canvas, self.diff_inside, *diff_list, command=self._dropdown_diff)
        dropdown.place(x=pos_x1, y=pos_y, anchor='center')
        button = tk.Button(self.canvas, text=f'{text}', height=height, width=width,
                           command=self._generate_board)
        button.place(x=pos_x2, y=pos_y, anchor='center')
        Hovertip(button, 'Generate a random sudoku puzzle')

    def info_button(self, text='Info', width=32, height=32):
        button = tk.Button(self.canvas, text=f'{text}', height=height, width=width,
                           command=lambda: info(), image=self.info)
        button.place(x=W-80, y=H-40)

    def github_button(self):
        button = tk.Button(self.canvas, image=self.img, command=open_url)
        Hovertip(button, 'Go to GitHub repository')
        button.place(x=W-40, y=H-40)
