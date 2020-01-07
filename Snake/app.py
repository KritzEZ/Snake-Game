from random import randint
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

MOVE_INC = 20
moves_per_sec = 15
GAME_SPEED = 1000 // moves_per_sec

class Snake(tk.Canvas):
    def __init__(self, highscore):
        super().__init__(width=600, height=620, background="black", highlightthickness=0)
        self.snake_positions = [(100,100), (80,100), (60,100)]
        self.food_position = self.set_new_food_position()
        self.score = 0
        self.highscore = highscore
        self.highscoremessage = "Congratulations, You Got A Highscore."
        self.direction = "Right"
        self.bind_all("<Key>", self.on_key_press)

        self.load_assets()
        beginnerButton = Button(self, text="Beginner", command=self.beginner, bg="#504F52", fg="#ffffff", padx=2, pady=2, width=20, bd=5, font=("TfDefaultFont", 14))
        intermediateButton = Button(self, text="Intermediate", command=self.intermediate, bg="#504F52", fg="#ffffff", padx=2, pady=2, width=20, bd=5, font=("TfDefaultFont", 14))
        advancedButton = Button(self, text="Advanced", command=self.advanced, bg="#504F52", fg="#ffffff", padx=2, pady=2, width=20, bd=5, font=("TfDefaultFont", 14))
        beginnerButton.place(relx=0.5, y= self.winfo_height() / 2 + 40, anchor=CENTER)
        intermediateButton.place(relx=0.5, y= self.winfo_height() / 2 + 100, anchor=CENTER)
        advancedButton.place(relx=0.5, y= self.winfo_height() / 2 + 160, anchor=CENTER)
        # self.getDifficulty

        # self.after(GAME_SPEED, self.perform_actions)

    def getDifficulty(self):
        beginnerButton = Button(self, text="Easy", bg="#504F52", fg="#ffffff", padx=2, pady=2, width=20, bd=5, font=("TfDefaultFont", 14))
        intermediateButton = Button(self, text="Exit Game", command=self.intermediate, bg="#504F52", fg="#ffffff", padx=2, pady=2, width=20, bd=5, font=("TfDefaultFont", 14))
        advancedButton = Button(self, text="Exit Game", command=self.advanced, bg="#504F52", fg="#ffffff", padx=2, pady=2, width=20, bd=5, font=("TfDefaultFont", 14))
        beginnerButton.place(relx=0.5, y= self.winfo_height() / 2 + 40, anchor=CENTER)
        intermediateButton.place(relx=0.5, y= self.winfo_height() / 2 + 100, anchor=CENTER)
        advancedButton.place(relx=0.5, y= self.winfo_height() / 2 + 160, anchor=CENTER)

    def beginner(self):
        for widgets in self.winfo_children():
            widgets.destroy()
        self.create_objects()
        self.after(GAME_SPEED, self.perform_actions)
    
    def intermediate(self):
        for widgets in self.winfo_children():
            widgets.destroy()
        self.create_objects()
        global moves_per_sec
        moves_per_sec += 300
        self.after(GAME_SPEED, self.perform_actions)

    
    def advanced(self):
        for widgets in self.winfo_children():
            widgets.destroy()
        self.create_objects()
        # global moves_per_sec
        # moves_per_sec += 985
        print(moves_per_sec)
        print(GAME_SPEED)
        self.after(GAME_SPEED, self.perform_actions)
        
    
    def load_assets(self):
        try:
            self.snake_body_image = Image.open("./assets/body.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.snake_food_image = Image.open("./assets/food.png")
            self.snake_food = ImageTk.PhotoImage(self.snake_food_image)
        except IOError as error:
            print(error)
            root.destroy()

    def create_objects(self):
        self.create_text(110, 12, text=f"Score: {self.score}     Highscore: {self.highscore}", tag="score", fill="#ffffff", font=("TfDefaultFont", 14))
        for x_pos, y_pos in self.snake_positions:
            self.create_image(x_pos, y_pos, image=self.snake_body, tag="snake")
        self.create_image(*self.food_position, image=self.snake_food, tag="food")
        self.create_rectangle(7, 27, 592, 613, outline="#ffffff")

    def move_snake(self):
        head_x_pos, head_y_pos  = self.snake_positions[0]

        if self.direction == "Left":
            new_head_pos = (head_x_pos - MOVE_INC, head_y_pos)
        elif self.direction == "Right":
            new_head_pos = (head_x_pos + MOVE_INC, head_y_pos)
        elif self.direction == "Down":
            new_head_pos = (head_x_pos, head_y_pos + MOVE_INC)
        elif self.direction == "Up":
            new_head_pos = (head_x_pos, head_y_pos - MOVE_INC)

        self.snake_positions = [new_head_pos] + self.snake_positions[:-1] 

        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position) 

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()
            return
        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions)

    def check_collisions(self):
        head_x_pos, head_y_pos  = self.snake_positions[0]
        return (
            head_x_pos in (0, 600)
            or head_y_pos in (20, 620)
            or (head_x_pos, head_y_pos) in self.snake_positions[1:]
        )
    
    def on_key_press(self, e):
        new_direction = e.keysym
        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if new_direction in all_directions and {new_direction, self.direction} not in opposites:
            self.direction = new_direction

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            if self.score % 5 == 0:
                global moves_per_sec
                moves_per_sec += 1

            self.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag="snake"
            )
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), *self.food_position)

            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score {self.score} Highscore {self.highscore}", tag="score")

    def set_new_food_position(self):
        while True:
            x_pos = randint(1,29) * MOVE_INC
            y_pos = randint(3, 30) * MOVE_INC

            food_position = (x_pos, y_pos)

            if food_position not in self.snake_positions:
                return food_position       
            
    def end_game(self):
        self.delete(tk.ALL)
        if self.score>self.highscore:
            self.highscore = self.score
            self.create_text(
                self.winfo_width() / 2,
                self.winfo_height() / 2 - 50,
                text=f"Game Over! You Scored {self.score}!",
                fill="#ffffff",
                font=("TkDefaultFont", 24)
            )
            self.create_text(
                self.winfo_width() / 2,
                self.winfo_height() / 2 - 25,
                text=f"\n  {self.highscoremessage}",
                fill="#ffffff",
                font=("TkDefaultFont", 16)
            )
        else:
            self.create_text(
                self.winfo_width() / 2,
                self.winfo_height() / 2 - 50,
                text=F"Game Over! You Scored {self.score}!",
                fill="#ffffff",
                font=("TkDefaultFont", 24)
            )
        playagainButton = Button(self, text="Play Again", command=self.playagain, bg="#504F52", fg="#ffffff", padx=2, pady=2, width=20, bd=5, font=("TfDefaultFont", 14))
        exitButton = Button(self, text="Exit Game", command=self.quitgame, bg="#504F52", fg="#ffffff", padx=2, pady=2, width=20, bd=5, font=("TfDefaultFont", 14))
        playagainButton.place(relx=0.5, y= self.winfo_height() / 2 + 40, anchor=CENTER)
        exitButton.place(relx=0.5, y= self.winfo_height() / 2 + 100, anchor=CENTER)

    def quitgame(self):
        exit()

    def playagain(self):
        score = self.highscore
        self.destroy()
        board = Snake(score)
        board.pack()    

root = tk.Tk()
root.title("Snake")
root.resizable(False, False)

board = Snake(0)
board.pack()

root.mainloop()