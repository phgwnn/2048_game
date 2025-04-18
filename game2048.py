import random 
import tkinter as tk 


class Game2048(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2048")
        self.geometry("500x500")
        self.resizable(False, False)

        self.game_over_label = None
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.high_score = 0 
        self.saved_high_score = 0 
        self.history = []
        self.create_widgets()
        self.start_new_game()
        self.back_used = False
        self.bind("<Key>", self.handle_key)
    
    def create_widgets(self):
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=10)

        score_frame = tk.Frame(top_frame)
        score_frame.pack(side="left", padx=10, pady=10)

        self.score_label = tk.Label(
            score_frame, text = f"Score: {self.score}", font = ("Helvetica", 12))
        self.score_label.pack(side = "top", padx = 10, pady = 10)

        self.high_score_label = tk.Label(
            score_frame, text = f"Score: {self.high_score}", font = ("Helvetica", 12))
        self.high_score_label.pack(side = 'top', padx = 10, pady = 10)

        button_frame = tk.Frame(top_frame)
        button_frame.pack(side="right", padx = 10, pady = 10)

        self.restart_button = tk.Button(
            button_frame, text = "Restart", command = self.start_new_game, font = ("Helvetica", 12))
        self.restart_button.pack(padx = 10, pady = 10)
         
        self.back_button = tk.Button(
            button_frame, text = "Back", command= self.go_back, font = ("Helvetica", 12))
        self.back_button.pack()

        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack()

        self.cells = [[tk.Label(self.grid_frame, text = "", width = 4, height = 2,
                                font = ("Helvetica", 24), bg = "#FFB9B9", relief = "ridge")
                        for _ in range(4)] for _ in range(4)]
        
        for i in range(4):
            for j in range(4):
                self.cells[i][j].grid(row = i, column= j, padx = 5, pady = 5)



    def add_random_tile(self):
        empty_tiles = [(i, j) for i in range(4)
                        for j in range(4) if self.grid[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.grid[i][j] = 2 if random.random() < 0.7 else 4

    def update_grid(self):
        for i in range(4):
            for j in range(4):
                value = self.grid[i][j]
                self.cells[i][j]. config(
                    text = str(value) if value != 0 else "", bg = self.get_color(value))

            self.score_label.config(text = f"Score: {self.score}")
            
            if self.score > self.high_score:
                self.high_score = self.score
                self.saved_high_score = self.high_score

            self.high_score_label.config(text = f"High Score: {self.high_score}")

            if self.check_game_over():
                self.game_over()


    def go_back(self):
        if len(self.history) > 1 and not self.back_used: 
            last_grid, last_score = self.history[-1]  
            self.grid = [row[:] for row in last_grid]
            self.score = last_score
            self.history.pop() 
            self.update_grid()

            self.back_used = True

    def make_move(self, new_grid, new_score):
        self.history.append((new_grid, new_score))  
        self.grid = [row[:] for row in new_grid]
        self.score = new_score  
        self.update_grid()

        self.back_used = False


    def get_color(self, value):
        colors = {
            0: "#FFEBD4",
            2: "#FFDDD2",
            4: "#F8C4B4",
            8: "#FFB9B9",
            16: "#F7A4A4",
            32: "#FF9494",
            64: "#FF8787",
            128: "#EF9595",
            256: "#EFB495",
            512: "#EFD595",
            1024: "#EBEF95",
            2048: "#FFD966",
            }
        return colors.get(value, '#7F7F7F')

    def handle_key(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.history.append((self.clone_grid(), self.score))
            self.back_used = False
            if event.keysym == "Up":
                self.move_up()
            elif event.keysym == "Down":
                self.move_down()
            elif event.keysym == "Left":
                self.move_left()
            elif event.keysym == "Right":
                self.move_right()
            self.add_random_tile()
            self.update_grid()

    def move_left(self):
        for i in range(4):
            self.merge_row(self.grid[i])
    
    def move_right(self):
        for i in range(4):
            self.grid[i].reverse()
            self.merge_row(self.grid[i])
            self.grid[i].reverse()

    def move_up(self):
        self.grid = [list(row) for row in zip(*self.grid)]
        self.move_left()
        self.grid = [list(row) for row in zip(*self.grid)]

    def move_down(self):
        self.grid = [list(row) for row in zip (*self.grid)]
        self.move_right()
        self.grid = [list(row) for row in zip(*self.grid)]

    def merge_row(self, row):
        new_row = [num for num in row if num != 0]
        i = 0 
        while i < len(new_row) - 1:
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                self.score += new_row[i]
                del new_row[i + 1]
            i += 1
        new_row += [0] * (4 - len(new_row))
        row[:] = new_row
    
    def check_game_over(self):
        if any(0 in row for row in self.grid):
            return False
        for i in range(4):
            for j in range(4):
                if (j < 3 and self.grid[i][j] == self.grid[i][j + 1] or (i < 3 and self.grid[i][j] == self.grid[i + 1][j])):
                    return False
        return True

    def game_over(self):
        if not self.game_over_label:
            self.game_over_label = tk.Label(
                self, text = "Game Over!", font = ("Helvetica", 24))
            self.game_over_label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.unbind("<Key>")
        self.restart_button.config(state = "normal")
        self.back_button.config(state = 'normal')


    def start_new_game(self):
        if self.game_over_label:
            self.game_over_label.destroy()
            self.game_over_label = None

        self.history = []
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.high_score = self.saved_high_score
        self.score_label.config(text = f"Score: {self.score}")
        self.high_score_label.config(text = f"High Score: {self.high_score}")
        self.restart_button.config(state = "normal")
        self.back_button.config(state = 'normal')

        for i in range(4):
            for j in range(4):
                self.cells[i][j]. config(text = "", bg = "#ccc0b3")

        self.add_random_tile()
        self.add_random_tile()
        self.history.append((self.clone_grid(), self.score))
        self.update_grid()
        self.bind("<Key>",self.handle_key)

    
    
    def clone_grid(self):
        return [row[:] for row in self.grid]




if __name__ == "__main__":
    game = Game2048()
    game.mainloop()


