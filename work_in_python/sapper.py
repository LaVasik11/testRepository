import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror
import time


colors = {
    1: 'blue',
    2: '#008200',
    3: '#FF0000',
    4: '#000084',
    5: '#840000',
    6: '#008284',
    7: '#840084',
    8: '#000000'
}

class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False

    def __repr__(self):
        return f'MyButton({self.x} {self.y}) {self.number}| {self.is_mine}'


class MineSweeper:
    window = tk.Tk()
    ROW = 10
    COLUMNS = 10
    window.geometry(f'{int((ROW+COLUMNS)*5*3.5)}x{int((ROW+COLUMNS)*5*3.5)}+500+250')
    MINES = 15
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True

    def __init__(self):
        self.buttons = []
        self.start_time = None
        self.timer_label = None
        for i in range(MineSweeper.ROW + 2):
            temp = []
            for j in range(MineSweeper.COLUMNS + 2):
                btn = MyButton(MineSweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind('<Button-3>', self.right_click)
                temp.append(btn)
            self.buttons.append(temp)

    def right_click(self, event):
        if MineSweeper.IS_GAME_OVER:
            return
        cur_btn = event.widget
        if cur_btn['state'] == 'normal':
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '🚩'
        elif cur_btn['text'] == '🚩':
            cur_btn['text'] = ''
            cur_btn['state'] = 'normal'

    def click(self, clicked_button: MyButton):
        if MineSweeper.IS_GAME_OVER:
            return

        if MineSweeper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mine_in_buttons()
            self.print_buttons()
            MineSweeper.IS_FIRST_CLICK = False
            self.start_time = time.time()

        if clicked_button.is_mine:
            clicked_button.config(text='*', background='red', disabledforeground='black')
            clicked_button.is_open = True
            MineSweeper.IS_GAME_OVER = True
            showinfo('Game over', 'Вы проиграли!')
            for i in range(1, MineSweeper.ROW + 1):
                for j in range(1, MineSweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
        else:
            color = colors.get(clicked_button.count_bomb, 'black')
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadch_first_search(clicked_button)

        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)


    def breadch_first_search(self, btn: MyButton):
        queue = [btn]
        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [1, 0, -1]:
                    for dy in [1, 0, -1]:
                        next_btn = self.buttons[x+dx][y+dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.ROW and \
                                1 <= next_btn.y <= MineSweeper.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)

    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        self.create_timer_label()
        MineSweeper.IS_FIRST_CLICK = True
        MineSweeper.IS_GAME_OVER = False
        self.start_time = None
        print('-' * MineSweeper.ROW * 2)

    def create_timer_label(self):
        self.timer_label = tk.Label(self.window, text="Время: 0 сек")
        self.timer_label.grid(row=0, column=0, columnspan=MineSweeper.COLUMNS, sticky="W")

    def update_timer_label(self):
        if self.start_time:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Время: {elapsed_time} сек")
        self.window.after(1000, self.update_timer_label)

    def create_settings_win(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.title('Настройки')
        tk.Label(win_settings, text='Количиство строк:').grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, str(MineSweeper.ROW))
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Количиство колонок:').grid(row=1, column=0)
        colum_entry = tk.Entry(win_settings)
        colum_entry.insert(0, str(MineSweeper.COLUMNS))
        colum_entry.grid(row=1, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Количиство мин:').grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0, str(MineSweeper.MINES))
        mines_entry.grid(row=2, column=1, padx=20, pady=20)

        save_btn = tk.Button(win_settings, text='Применить',
                  command=lambda : self.change_settings(row_entry, colum_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_settings(self, row: tk.Entry, colum: tk.Entry, mines: tk.Entry):
        try:
            MineSweeper.ROW = int(row.get())
            MineSweeper.COLUMNS = int(colum.get())
            MineSweeper.MINES = int(mines.get())
        except ValueError:
            showerror('Ошибка', 'ВЫ ввели неправильное значение.')
            return
        self.reload()


    def create_widgets(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Играть', command=self.reload)
        settings_menu.add_command(label='Натсройки', command=self.create_settings_win)
        settings_menu.add_command(label='Выход', command=self.window.destroy)
        menubar.add_cascade(label='Файл', menu=settings_menu)


        count = 1
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick='NWES')
                count += 1

        for i in range(1, MineSweeper.ROW + 1):
            MineSweeper.window.rowconfigure(i, weight=1)
        for j in range(1, MineSweeper.COLUMNS + 1):
            MineSweeper.window.columnconfigure(j, weight=1)

    def open_all_buttons(self):
        for i in range(MineSweeper.ROW + 2):
            for j in range(MineSweeper.COLUMNS + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', background='red', disabledforeground='black')
                elif btn.count_bomb in colors:
                    color = colors.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, fg=color)

    def start(self):
        self.create_widgets()
        self.create_timer_label()
        self.update_timer_label()
        MineSweeper.window.mainloop()

    def print_buttons(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B', end=' ')
                else:
                    print(btn.count_bomb, end=' ')
            print()

    def insert_mines(self, number:int):
        index_mines = self.get_mines_places(number)
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True

    def count_mine_in_buttons(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb

    @staticmethod
    def get_mines_places(exclude_number: int):
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROW + 1))
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:MineSweeper.MINES]

game = MineSweeper()
game.start()