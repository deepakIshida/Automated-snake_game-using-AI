from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
from math import cos, sin, radians
import time

MOVE_DISTANCE = 20

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My Snake Game - AI Controlled")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()

    # --- Improved AI Movement ---
    directions = [("up", 90), ("down", 270), ("left", 180), ("right", 0)]
    safe_moves = []

    for name, angle in directions:
        rad = radians(angle)
        next_x = snake.head.xcor() + MOVE_DISTANCE * round(cos(rad))
        next_y = snake.head.ycor() + MOVE_DISTANCE * round(sin(rad))

        # Check wall collision
        if not (-280 < next_x < 280 and -280 < next_y < 280):
            continue

        # Check self collision
        collision = False
        for segment in snake.segments[1:]:
            if segment.distance(next_x, next_y) < 10:
                collision = True
                break
        if not collision:
            safe_moves.append((name, angle))

    # Choose best safe move toward food
    best_move = None
    min_dist = float('inf')
    for name, angle in safe_moves:
        rad = radians(angle)
        future_x = snake.head.xcor() + MOVE_DISTANCE * round(cos(rad))
        future_y = snake.head.ycor() + MOVE_DISTANCE * round(sin(rad))
        dx = food.xcor() - future_x
        dy = food.ycor() - future_y
        dist = abs(dx) + abs(dy)
        if dist < min_dist:
            min_dist = dist
            best_move = name

    # Move
    if best_move == "up":
        snake.up()
    elif best_move == "down":
        snake.down()
    elif best_move == "left":
        snake.left()
    elif best_move == "right":
        snake.right()

    snake.move()

    # Detect collision with food
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()

    # Detect collision with wall
    if (
        snake.head.xcor() > 280 or snake.head.xcor() < -280 or
        snake.head.ycor() > 280 or snake.head.ycor() < -280
    ):
        game_is_on = False
        scoreboard.game_over()

    # Detect collision with tail
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            game_is_on = False
            scoreboard.game_over()

screen.exitonclick()
