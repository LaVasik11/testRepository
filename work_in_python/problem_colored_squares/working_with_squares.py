import random


class SquareProblem:
    def __init__(self, problem=None):
        self.colors = ["red", "lime", "blue", "yellow", "violet", "grey"]
        self.squares = problem or self.generate_squares()

    def generate_squares(self):
        color_list = self.colors * 6
        random.shuffle(color_list)
        return [color_list[i:i + 6] for i in range(0, 36, 6)]

    def shuffle_squares(self):
        self.squares = self.generate_squares()

    def show_squares(self):
        for row in self.squares:
            print(row)

    def shift_row(self, row_index, direction):
        print(f'row_index: {row_index} | direction: {direction}')
        if direction == 'left':
            self.squares[row_index] = self.squares[row_index][1:] + [self.squares[row_index][0]]
        elif direction == 'right':
            self.squares[row_index] = [self.squares[row_index][-1]] + self.squares[row_index][:-1]

    def shift_column(self, col_index, direction):
        print(f'col_index: {col_index} | direction: {direction}')
        col = [self.squares[i][col_index] for i in range(6)]
        if direction == 'up':
            col = col[1:] + [col[0]]
        elif direction == 'down':
            col = [col[-1]] + col[:-1]
        for i in range(6):
            self.squares[i][col_index] = col[i]

    def fill_row_with_color(self, row_index, color):
        max_attempts = 3000
        attempts = 0

        while any(self.squares[row_index][i] != color for i in range(6)):
            if attempts >= max_attempts:
                print("-"*80)
                print(f"Exceeded max attempts on row {row_index} with color {color}")
                return False

            attempts += 1
            for ni in range(row_index + 1, 6):
                for nj in range(6):
                    if self.squares[ni][nj] == color:
                        for target_col in range(6):
                            if self.squares[row_index][target_col] != color:
                                for _ in range(ni - row_index):
                                    self.shift_column(target_col, "down")

                                if target_col > nj:
                                    for _ in range(target_col - nj):
                                        self.shift_row(ni, "right")
                                else:
                                    for _ in range(nj - target_col):
                                        self.shift_row(ni, "left")

                                for _ in range(ni - row_index):
                                    self.shift_column(target_col, "up")

                                break
        return True

    def fill_all_rows(self):
        for i, color in enumerate(self.colors):
            if not self.fill_row_with_color(i, color):
                print(f"Failed to fill row {i} with color {color}")
                break


problem = SquareProblem()
problem.show_squares()
print("-"*80)
problem.fill_all_rows()
problem.show_squares()