import turtle as t
import random
from math import e 

# Constants
WINSIZE = (700, 700)
T = 65 # 'Temperature': Change this values to 'anneal' the probability function

# Define the walls
# (x, y1, y2) y1 > y2
verticalWalls = ((-350, 350, -350), (-250, 350, -150), (-150, 150, -50), (-150, -150, -250), (-50, 350, 150),
                 (-50, -50, -250), (50, -150, -250), (50, 150, -150), (150, 150, 50), (150, 350, 250),
                 (150, -150, -350), (250, 350, 50), (250, -50, -150),  (350, 350, -350))

# (y, x1, x2) x1 < x2
horizontalWalls = ((-350, 350, -350),  (-250, -350, -150),  (-150, 150, 250),  (-50, -150, -50), (250, 50, 150),
                   (50, 150, 250), (50, -50, 50), (150, -150, -50), (150, 50, 150), (350, 350, -350))

initialPosition = (-300, 300)
destination = (350, -350)

# Functions


def draw_maze(vertical_wall_array, horizontal_wall_array):
    wall_pen = t.Turtle()
    wall_pen.ht()
    wall_pen.pensize(10)
    wall_pen.color('#0DA192')
    wall_pen.speed(0)
    wall_pen.penup()

    for i in vertical_wall_array:
        wall_pen.goto(i[0], i[1])
        wall_pen.pendown()
        wall_pen.goto(i[0], i[2])
        wall_pen.penup()
    
    for i in horizontal_wall_array:
        wall_pen.goto(i[1], i[0])
        wall_pen.pendown()
        wall_pen.goto(i[2], i[0])
        wall_pen.penup()


def draw_square(initial_x, initial_y, side_length):
    square_turtle = t.Turtle()
    square_turtle.ht()
    square_turtle.fillcolor('#0DA192')
    square_turtle.pencolor('#0DA192')
    square_turtle.penup()
    square_turtle.speed(0)
    square_turtle.goto(initial_x, initial_y)
    square_turtle.pendown()
    square_turtle.begin_fill()

    for _ in range(4):
        square_turtle.forward(side_length)
        square_turtle.right(90)
    square_turtle.end_fill()


def valid_move(old_x, old_y, new_x, new_y):
    valid = True

    # Return False if the move is crossing a wall
    for i in verticalWalls:
        if (old_x >= i[0] >= new_x) or (old_x <= i[0] <= new_x):
            if i[1] >= old_y + (((new_y - old_y) / (new_x - old_x)) * (i[0] - old_x)) >= i[2]:
                return False

    for i in horizontalWalls:
        if (old_y >= i[0] >= new_y) or (old_y <= i[0] <= new_y):
            if i[1] <= old_x + ((i[0] - old_y) / ((new_y - old_y) / (new_x - old_x))) <= i[2]:
                return False

    return valid

#Window
wn = t.Screen()
wn.title("Maze")
wn.bgcolor('#14BDAC')
wn.setup(width=WINSIZE[0], height=WINSIZE[1])

draw_maze(verticalWalls, horizontalWalls)
draw_square(-350, 350, 100)
draw_square(250, -250, 100)

# Set up the turtle that solves the mazes
pathFinder = t.Turtle()
pathFinder.shape('turtle')
pathFinder.speed(0)
pathFinder.color('#FFFFFF')
pathFinder.penup()
pathFinder.goto(initialPosition[0], initialPosition[1])
pathFinder.speed(10)
pathFinder.pendown()

# Variables
moves = 0
prevEnergy = pathFinder.ycor() - pathFinder.xcor()


# Main loop
while True:

    # Generate a random move
    newX = pathFinder.xcor() + random.uniform(-30, 30)
    newY = pathFinder.ycor() + random.uniform(-30, 30)

    if valid_move(pathFinder.xcor(), pathFinder.ycor(), newX, newY):
        # Energy function
        energy = newY - newX
        # 'Probability' of accepting the move
        p = e**(-(energy - prevEnergy)/T)

        if random.uniform(0, 1) < p and -350 <= newX <= 350 and -350 <= newY <= 350:
            pathFinder.goto(newX, newY)
            moves += 1
            prevEnergy = energy

    # Check if the turtle has reached the destination
    if pathFinder.xcor() > (destination[0]-50) and pathFinder.ycor() < (destination[1]+50):
        print(f'No. of moves taken = {moves}')
        break 

t.done()
