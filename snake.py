import tkinter as tk
import random

# Set up the game window
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

# Game configurations
WIDTH = 400
HEIGHT = 400
SPEED = 100  # Milliseconds per movement
SPACE_SIZE = 20  # Size of each segment of the snake
BODY_PARTS = 3  # Initial snake length
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
score = 0

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    global score
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Check if the snake ate the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check if game is over
    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    # Check if snake hits the walls
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True

    # Check if snake hits itself
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(tk.ALL)
    canvas.create_text(WIDTH / 2, HEIGHT / 2 - 20, font=("consolas", 40), text="GAME OVER", fill="red", tag="gameover")
    retry_button.place(x=WIDTH / 2 - 50, y=HEIGHT / 2 + 20)

def restart_game():
    global score
    score = 0
    label.config(text="Score:{}".format(score))

    # Reset the canvas
    canvas.delete(tk.ALL)

    # Create a new snake and food
    snake = Snake()
    food = Food()

    # Start the game again
    next_turn(snake, food)
    retry_button.place_forget()  # Hide the retry button after restarting

# Initialize game
canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=HEIGHT, width=WIDTH)
canvas.pack()

# Score label
label = tk.Label(window, text="Score:{}".format(score), font=("consolas", 20))
label.pack()

direction = "down"

snake = Snake()
food = Food()

# Control bindings
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

# Retry button
retry_button = tk.Button(window, text="Retry", font=("consolas", 15), command=restart_game)

next_turn(snake, food)

window.mainloop()
