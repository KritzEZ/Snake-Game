#Kritarth Shah
#Version 4.0
#Changes: Indiviual highscores for each level and home screem improved to look better with Snake Logo
#Date: Jan 14 2020
#Gameplay credit goes to teclado (youtube)

from random import randint
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

MOVE_INC = 20

class Snake(tk.Canvas):
    def __init__(self,highscorearray):
        super().__init__(width=600, height=620, background="black", highlightthickness=0)
        self.snake_positions = [(100,100), (80,100), (60,100)]
        self.food_position = self.set_new_food_position()
        self.score = 0
        self.allhighscore = {"Beginner":highscorearray[0], "Intermediate":highscorearray[1], "Advanced":highscorearray[2]}
        self.direction = "Right"
        self.bind_all("<Key>", self.on_key_press)

        self.load_assets()
        self.getDifficulty()

    #Homes Screen Level Buttons (Beginner, Intermediate, Advanced) all go to their own functions when clicked on
    def getDifficulty(self):
        beginnerButton = Button(self, text="Beginner", command=self.beginner, bg="#504F52", fg="#ffffff", padx=2, pady=2, width=20, bd=5, font=("TfDefaultFont", 14))
        intermediateButton = Button(self, text="Intermediate", command=self.intermediate, bg="#504F52", fg="#ffffff", padx=2, pady=2, width=20, bd=5, font=("TfDefaultFont", 14))
        advancedButton = Button(self, text="Advanced", command=self.advanced, bg="#504F52", fg="#ffffff", padx=2, pady=2, width=20, bd=5, font=("TfDefaultFont", 14))
        beginnerButton.place(x=300, y=150, anchor=CENTER)
        intermediateButton.place(x=300, y=220, anchor=CENTER)
        advancedButton.place(x=300, y=290, anchor=CENTER)
        self.image = self.create_image(300,60, image=self.snake_logo)

    #---------------------------------------------------------------------------------------------------------------
    #All functions are used from button press, setting the type of level and the speed of the game
    #Starts gameplay at the end
    def beginner(self):
        self.levelkey = "Beginner"
        self.clearscreen()
        self.speed = 1000//15
        self.after(self.speed, self.perform_actions)
    
    def intermediate(self):
        self.levelkey = "Intermediate"
        self.clearscreen()
        self.speed = 1000//20
        self.after(self.speed, self.perform_actions)

    def advanced(self):
        self.levelkey = "Advanced"
        self.clearscreen()
        self.speed = 1000//30
        self.after(self.speed, self.perform_actions)
    #---------------------------------------------------------------------------------------------------------------

    #Function clears the screen of all images and buttons from the homescreen and starts to create the objects required in the game play
    def clearscreen(self):
        for widgets in self.winfo_children():
            widgets.destroy()
        self.delete(self.image)
        self.create_objects()
        
    #Tries to open all the images required in the game and creates it into a Image object
    #If an image does not exit in the directory, will print error message and destroy game
    def load_assets(self):
        try:
            self.snake_logo_image = Image.open("./assets/logo.png")
            self.snake_logo = ImageTk.PhotoImage(self.snake_logo_image)

            self.snake_body_image = Image.open("./assets/body.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.snake_food_image = Image.open("./assets/food.png")
            self.snake_food = ImageTk.PhotoImage(self.snake_food_image)
        except IOError as error:
            print(error)
            root.destroy()

    #Adds top text of gameplay and creates rectangle for snake boarders
    #Creates the snake body at the original placement --> decided in the initilizer
    #Creates food image and places it at position determined from food_position function
    def create_objects(self):
        self.create_text(215, 12, text=f"Score: {self.score}     Highscore: {self.allhighscore.get(self.levelkey)}     Difficulty: {self.levelkey}", tag="score", fill="#ffffff", font=("TfDefaultFont", 14))
        for x_pos, y_pos in self.snake_positions:
            self.create_image(x_pos, y_pos, image=self.snake_body, tag="snake")
        self.create_image(*self.food_position, image=self.snake_food, tag="food")
        self.create_rectangle(7, 27, 592, 613, outline="#ffffff")

    #Direction of the snake traveling according to the keyboard unput by the user (Determines the new position of the head)
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

    #Puts all individual functions into one creating the gameplay
    def perform_actions(self):
        if self.check_collisions():
            self.end_game()
            return
        self.check_food_collision()
        self.move_snake()
        self.after(self.speed, self.perform_actions)

    #Checks if the head of the snake touches any borders or hits another body piece in the snake
    def check_collisions(self):
        head_x_pos, head_y_pos  = self.snake_positions[0]
        return (
            head_x_pos in (0, 600)
            or head_y_pos in (20, 620)
            or (head_x_pos, head_y_pos) in self.snake_positions[1:]
        )
    
    #Checks if the input by user is one of the directions that the game takes and also checks to see of the new direction is not oppisite to the current direction of the snake 
    #(becuase thats not possible --> will collide)
    def on_key_press(self, e):
        new_direction = e.keysym
        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if new_direction in all_directions and {new_direction, self.direction} not in opposites:
            self.direction = new_direction

    #Checks to see of the head of the snake has collided with the food position
    #If so, the score will increment by one, one body image will be added to the current body of the snake and a new food image will be placed at position given by a different function
    #Updates the score text at the top of the game
    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag="snake")
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), *self.food_position)

            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score {self.score}     Highscore {self.allhighscore.get(self.levelkey)}     Difficulty: {self.levelkey}", tag="score")

    #Gets and returns new random position of food within the boarders and check of the food position is not over any of the snake body positions
    def set_new_food_position(self):
        while True:
            x_pos = randint(1,29) * MOVE_INC
            y_pos = randint(3, 30) * MOVE_INC

            food_position = (x_pos, y_pos)

            if food_position not in self.snake_positions:
                return food_position       

    #End of game page
    #If new highscore is achieved, a different messages if utputed and the highscore in the array is changed to the new value using the key of level
    #Outputs nornal message if no highscore is achieved  
    #Play Again or Exit game buttons at the end          
    def end_game(self):
        self.delete(tk.ALL)
        if self.score>self.allhighscore.get(self.levelkey):
            newscore = {self.levelkey:self.score}
            self.allhighscore.update(newscore)
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
                text=f"\n  Congratulations, You Got A Highscore.",
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

    #Exit button command
    def quitgame(self):
        exit()

    #Play Again button command, calling the class again with updated highscore array
    def playagain(self):
        self.destroy()
        board = Snake([self.allhighscore.get("Beginner"),self.allhighscore.get("Intermediate"),self.allhighscore.get("Advanced")])
        board.pack()    

root = tk.Tk()
root.title("Snake")
root.resizable(False, False)

board = Snake([0,0,0])
board.pack()

root.mainloop()