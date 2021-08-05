import turtle
import time
import random


def start_settings():
    window = turtle.Screen()
    window.setup(width=800, height=600)
    window.title('Snake by GKerr')
    window.bgcolor('black')
    window.tracer(0)
    return window


class Movement:
    def __init__(self, snake):
        self.player = snake

    def move_loop(self):
        if Player.player_head_direction == 'up':
            y = self.player.ycor()
            if y >= 290:
                y = -290
            else:
                y += 15
            self.player.sety(y)
        elif Player.player_head_direction == 'down':
            y = self.player.ycor()
            if y <= -290:
                y = 290
            else:
                y -= 15
            self.player.sety(y)
        elif Player.player_head_direction == 'left':
            x = self.player.xcor()
            if x <= -390:
                x = 390
            else:
                x -= 15
            self.player.setx(x)
        elif Player.player_head_direction == 'right':
            x = self.player.xcor()
            if x >= 390:
                x = -390
            else:
                x += 15
            self.player.setx(x)

    @staticmethod
    def up():
        if Player.player_head_direction != 'down':
            Player.player_head_direction = 'up'

    @staticmethod
    def down():
        if Player.player_head_direction != 'up':
            Player.player_head_direction = 'down'

    @staticmethod
    def left():
        if Player.player_head_direction != 'right':
            Player.player_head_direction = 'left'

    @staticmethod
    def right():
        if Player.player_head_direction != 'left':
            Player.player_head_direction = 'right'


class Body:
    player_body = []
    player_body_color = 'green'
    player_body_shape = 'square'

    @staticmethod
    def player_body_settings():
        body_part = turtle.Turtle()
        body_part.shape(Body.player_body_shape)
        body_part.color(Body.player_body_color)
        body_part.speed(0)
        body_part.shapesize(stretch_wid=1, stretch_len=1)
        body_part.penup()
        return body_part


class Player:
    player_head_color = 'green'
    player_head_shape = 'square'
    player_head_direction = 'up'

    @staticmethod
    def player_settings():
        player = turtle.Turtle()
        player.shape(Player.player_head_shape)
        player.color(Player.player_head_color)
        player.speed(0)
        player.penup()
        player.shapesize(stretch_wid=1, stretch_len=1)
        player.goto(0, 0)
        return player


class Score:
    high_score = 0
    score = 0

    @staticmethod
    def score_settings():
        scoreboard = turtle.Turtle()
        scoreboard.color('white')
        scoreboard.penup()
        scoreboard.speed(0)
        scoreboard.goto(-340, 270)
        scoreboard.write(f'Score: {Score.score}', align='center', font=('Arial', 20, 'normal'))
        scoreboard.hideturtle()
        return scoreboard

    @staticmethod
    def high_score_settings():
        high_score = turtle.Turtle()
        high_score.color('white')
        high_score.penup()
        high_score.speed(0)
        high_score.goto(270, 270)
        high_score.write(f'High score: {Score.high_score}', align='center', font=('Arial', 20, 'normal'))
        high_score.hideturtle()
        return high_score


class Food:
    food_shape = 'circle'
    food_color = 'red'

    @staticmethod
    def food_settings():
        food = turtle.Turtle()
        food.shape(Food.food_shape)
        food.color(Food.food_color)
        food.speed(0)
        food.penup()
        food.shapesize(stretch_wid=0.5, stretch_len=0.5)
        food.goto(random.randint(-390, 390), random.randint(-290, 290))
        return food


class Collision:
    def __init__(self, player, food):
        self.food = food
        self.player = player

    def food_collision(self):
        if (self.food.ycor() == self.player.ycor() and self.food.xcor() == self.player.xcor()) or self.player.distance(
                self.food) < 15:
            Score.score += 10
            self.food.goto(random.randint(-390, 390), random.randint(-290, 290))
            return True


def check_score():
    if Score.score > Score.high_score:
        Score.high_score = Score.score
        return True


def game_loop():
    window = start_settings()
    player = Player().player_settings()
    movement = Movement(player)
    food = Food.food_settings()
    score = Score.score_settings()
    high_score = Score.high_score_settings()
    collision = Collision(player, food)
    body = Body()
    body.player_body.append(Body.player_body_settings())
    body.player_body[0].goto(player.xcor(), player.ycor())
    while True:
        window.update()
        movement.move_loop()
        time.sleep(0.1)
        window.listen()
        window.onkey(movement.up, 'Up')
        window.onkey(movement.down, 'Down')
        window.onkey(movement.left, 'Left')
        window.onkey(movement.right, 'Right')

        if collision.food_collision():
            score.clear()
            score.write(f'Score: {Score.score}', align='center', font=('Arial', 20, 'normal'))
            body.player_body.append(body.player_body_settings())

        if len(body.player_body) > 0:
            x = player.xcor()
            y = player.ycor()
            body.player_body[0].goto(x, y)

        for i in range(len(body.player_body) - 1, 0, -1):
            x = body.player_body[i - 1].xcor()
            y = body.player_body[i - 1].ycor()
            body.player_body[i].goto(x, y)

        for index in range(len(body.player_body)):
            if index <= 2:
                continue
            if body.player_body[index].distance(player) < 20:
                time.sleep(1)
                player.clear()
                for hide in body.player_body:
                    hide.goto(1000, 1000)
                body.player_body.clear()
                body.player_body = []
                player.goto(0, 0)
                Player.player_head_direction = 'end'
                if check_score():
                    Score.score = 0
                    score.clear()
                    score.write(f'Score: {Score.score}', align='center', font=('Arial', 20, 'normal'))
                    high_score.clear()
                    high_score.write(f'High score: {Score.high_score}', align='center', font=('Arial', 20, 'normal'))


game_loop()
