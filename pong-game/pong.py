# Implementation of classic arcade game Pong

import simpleguitk as simplegui
import random
import numpy as np

class PongGame:
    def __init__(self):
        # initialize globals - pos and vel encode vertical info for paddles
        self.WIDTH = 600
        self.HEIGHT = 400
        self.BALL_RADIUS = 20
        self.PAD_WIDTH = 8
        self.PAD_HEIGHT = 80
        self.HALF_PAD_WIDTH = self.PAD_WIDTH / 2
        self.HALF_PAD_HEIGHT = self.PAD_HEIGHT / 2
        self.paddle1_pos = self.HEIGHT / 2.0
        self.paddle2_pos = self.HEIGHT / 2.0
        self.paddle1_vel = 0.0
        self.paddle2_vel = 0.0
        self.score1 = 0
        self.score2 = 0
        self.ball_pos = [0, 0]
        self.ball_vel = [0, 0]
        self.turn = False
        self.ball_init(False)

    # helper function that spawns a ball by updating the
    # ball's position vector and velocity vector
    # if right is True, the ball's velocity is upper right, else upper left
    def ball_init(self, right):
        sign_x, sign_y = -1, -1
        self.turn = right  # Assigns the turn of the player
        if right:
            sign_x, sign_y = 1, -1
        horiz_vel = (random.randrange(120, 240) / 60) * sign_x
        vert_vel = (random.randrange(60, 180) / 60) * sign_y
        self.ball_pos = [self.WIDTH / 2, self.HEIGHT / 2]
        self.ball_vel = [horiz_vel, vert_vel]

    # helper function that restricts the paddles to stay entirely on the canvas
    def paddle_bounds_pos(self, paddle_pos, paddle_vel):
        try_paddle_pos = paddle_pos + paddle_vel
        if try_paddle_pos in np.arange(self.HALF_PAD_HEIGHT, self.HEIGHT - self.HALF_PAD_HEIGHT + 1):
            return try_paddle_pos
        else:
            return paddle_pos

    # helper function that checks whether the ball is actually striking a paddle
    # when it touches a gutter
    def bounce_ball(self, paddle_pos, side):
        if int(self.ball_pos[1]) in range(int(paddle_pos - self.HALF_PAD_HEIGHT), int(paddle_pos + self.HALF_PAD_HEIGHT)) and side:
            self.ball_vel[0] *= -1  # change direction of the ball
            self.ball_vel[0] += (self.ball_vel[0] * 0.1)  # increase the velocity of the ball by 10%
            return True  # the ball is striking a paddle
        return False

    # define event handlers
    def new_game(self):
        self.score1, self.score2 = 0, 0
        self.paddle1_pos = self.HEIGHT / 2.0
        self.paddle2_pos = self.HEIGHT / 2.0
        self.paddle1_vel = 0.0
        self.paddle2_vel = 0.0
        self.ball_init(False)

    def restart_button(self):
        self.new_game()

    def draw(self, c):
        # update paddle's vertical position, keep paddle on the screen
        self.paddle1_pos = self.paddle_bounds_pos(self.paddle1_pos, self.paddle1_vel)
        self.paddle2_pos = self.paddle_bounds_pos(self.paddle2_pos, self.paddle2_vel)
        # draw mid line and gutters
        c.draw_line([self.WIDTH / 2, 0], [self.WIDTH / 2, self.HEIGHT], 1, "White")
        c.draw_line([self.PAD_WIDTH, 0], [self.PAD_WIDTH, self.HEIGHT], 1, "White")
        c.draw_line([self.WIDTH - self.PAD_WIDTH, 0], [self.WIDTH - self.PAD_WIDTH, self.HEIGHT], 1, "White")
        # draw paddles
        c.draw_line([self.HALF_PAD_WIDTH, self.paddle1_pos - self.HALF_PAD_HEIGHT],
                    [self.HALF_PAD_WIDTH, self.paddle1_pos + self.HALF_PAD_HEIGHT],
                    self.PAD_WIDTH, "White")
        c.draw_line([self.WIDTH - self.HALF_PAD_WIDTH, self.paddle2_pos - self.HALF_PAD_HEIGHT],
                    [self.WIDTH - self.HALF_PAD_WIDTH, self.paddle2_pos + self.HALF_PAD_HEIGHT],
                    self.PAD_WIDTH, "White")
        # update ball
        if (self.ball_pos[0] <= self.PAD_WIDTH + self.BALL_RADIUS
                or self.ball_pos[0] >= (self.WIDTH - self.PAD_WIDTH - 1) - self.BALL_RADIUS):
            if self.bounce_ball(self.paddle1_pos, self.ball_pos[0] < self.WIDTH / 2):
                self.turn = True  # the ball strikes against the paddle and is returned to the right player
            elif self.bounce_ball(self.paddle2_pos, self.ball_pos[0] > self.WIDTH / 2):
                self.turn = False  # the ball strikes against the paddle and is returned to the left player
            else:  # scoring the game and the ball is respawned
                if self.turn:
                    self.score1 += 1
                else:
                    self.score2 += 1
                self.ball_init(not self.turn)  # The ball touches a gutter and is directed to the opposite player
        if self.ball_pos[1] <= self.BALL_RADIUS or self.ball_pos[1] >= (self.HEIGHT - 1) - self.BALL_RADIUS:
            self.ball_vel[1] *= -1  # The ball collides and bounces from top to bottom
        self.ball_pos[0] += self.ball_vel[0]
        self.ball_pos[1] += self.ball_vel[1]
        # draw ball and scores
        c.draw_circle(self.ball_pos, self.BALL_RADIUS, 1, "WHITE", "WHITE")
        c.draw_text(str(self.score1), (self.WIDTH / 4, self.HEIGHT / 4), 70, "White", "sans-serif")
        c.draw_text(str(self.score2), (self.WIDTH / 1.5, self.HEIGHT / 4), 70, "White", "sans-serif")

    def keydown(self, key):
        const_vel = self.HEIGHT / self.PAD_HEIGHT  # constant velocity according to the height of the canvas and the paddle
        if key == simplegui.KEY_MAP["w"]:
            self.paddle1_vel = -const_vel
        elif key == simplegui.KEY_MAP["s"]:
            self.paddle1_vel = const_vel
        if key == simplegui.KEY_MAP["up"]:
            self.paddle2_vel = -const_vel
        elif key == simplegui.KEY_MAP["down"]:
            self.paddle2_vel = const_vel

    def keyup(self, key):
        if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
            self.paddle1_vel = 0
        if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
            self.paddle2_vel = 0


pong_game = PongGame()
# create frame
frame = simplegui.create_frame("Pong", pong_game.WIDTH, pong_game.HEIGHT)
frame.set_draw_handler(pong_game.draw)
frame.set_keydown_handler(pong_game.keydown)
frame.set_keyup_handler(pong_game.keyup)
restart = frame.add_button("Restart", pong_game.restart_button, 100)

# start frame
frame.start()

pong_game.new_game()
