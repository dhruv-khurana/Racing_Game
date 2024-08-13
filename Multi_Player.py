import pygame
import math
from pygame import mixer
import button
import threading

from utils import scale_image, blit_rotate_center

# Initialize constants and settings
steering_sens = 5
FPS = 60
speed = 50
attempt = 0
scores = []
multiplayer = True
menu = False
TEXT_COL = (255, 255, 255)
menu_state = "main"  # Initial menu state

pygame.init()
mixer.init()
mixer.music.load("images/Music")
mixer.music.set_volume(0.4)
mixer.music.play()

font = pygame.font.SysFont("Arial", 25)

# Load and scale images
TRACK = scale_image(pygame.image.load("images/Track.png"), 0.85)
TRACK_BORDER = scale_image(pygame.image.load("images/Track_Border"), 0.85)
FINISH = scale_image(pygame.image.load("images/Finish_Line"), 0.65)
RED_CAR = scale_image(pygame.image.load("images/Red_Car"), 0.015)
BLUE_CAR = scale_image(pygame.image.load("files/imgs/Blue_Car"), 0.037)
BACKGROUND = scale_image(pygame.image.load("files/imgs/Background_Image"), 15)

# Get track dimensions and create masks

TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (400, 50)

# Initialize window
WIN = pygame.display.set_mode((1940, 992))
pygame.display.set_caption("Turbo Tracks")

class AbstractCar:
    def __init__(self, max_vel, rotation_vel, IMG, START_POS):
        self.img = IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = -90
        self.x, self.y = START_POS
        self.acceleration = 0.5
        self.bounce_factor = 0.7  # Factor to reduce velocity upon collision

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win, offset):
        blit_rotate_center(win, self.img, (self.x - offset[0], self.y - offset[1]), self.angle)

    def display(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration*2, 0)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def bounce(self):
        # Reduce the car's velocity upon collision to prevent it from going through walls
        self.vel *= -self.bounce_factor
        radians = math.radians(self.angle)
        
        # Move the car back slightly in the direction opposite to the current velocity
        self.x += math.sin(radians) * 10  # Adjust this value to ensure it doesn't get stuck but also doesn't go through walls
        self.y += math.cos(radians) * 10  # Adjust this value to ensure it doesn't get stuck but also doesn't go through walls
        self.vel = 0  # Reset velocity to prevent further bouncing

    def reduce_speed(self):
        # Reduce speed but ensure it doesn't become negative
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def reset(self):
        self.x, self.y = (440, 60)
        self.angle = -90
        self.vel = 0

player1 = AbstractCar(speed, steering_sens, RED_CAR, (440, 60))
player2 = AbstractCar(speed, steering_sens, BLUE_CAR, (440, 90))

def draw(win, images, winner=None):
    if multiplayer:
        win.blit(TRACK, (0, 0))  # Draw the track first
        for img, pos in images[1:]:
            win.blit(img, pos)  # Draw the remaining images
        player1.display(win)
        player2.display(win)
        if winner:
            draw_text(f"Player {winner} wins!", font, TEXT_COL, 1940 // 2, 992 // 2)
            return True
        pygame.display.update()

def handle_keys(player_car, player_2):
    keys = pygame.key.get_pressed()
    moved = False
    m2 = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
        player_car.acceleration = 0.3 if keys[pygame.K_LSHIFT] else 0.02

    if keys[pygame.K_LEFT]:
        player_2.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player_2.rotate(right=True)
    if keys[pygame.K_UP]:
        m2 = True
        player_2.move_forward()
        player_2.acceleration = 0.3 if keys[pygame.K_RSHIFT] else 0.02
    if keys[pygame.K_DOWN]:
        m2 = True
        player2.move_backward()

    if keys[pygame.K_r]:
        player_car.reset()
        player2.reset()


    if not moved:
        player_car.reduce_speed()

    if not m2:
        player_2.reduce_speed()

    return None

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    WIN.blit(img, (x, y))

images = [(TRACK_BORDER, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POSITION)]

run = True
clock = pygame.time.Clock()

def collision_detection():
    while run:
        if multiplayer:
            f1 = player1.collide(FINISH_MASK, *FINISH_POSITION)
            f2 = player2.collide(FINISH_MASK, *FINISH_POSITION)
            if f1:
                draw(WIN, images, winner="1")
                pygame.time.wait(10)
                pygame.display.update()
                player1.reset()
                player2.reset()

            elif f2:
                draw(WIN, images, winner="2")
                pygame.time.wait(10)
                pygame.display.update()
                player1.reset()
                player2.reset()

        if player1.collide(TRACK_BORDER_MASK) is not None:
            player1.bounce()

        if player2.collide(TRACK_BORDER_MASK) is not None:
            player2.bounce()

# Start collision detection thread
def multiplayer():
    collision_thread = threading.Thread(target=collision_detection, daemon=True)
    collision_thread.start()
    
    run = True
    while run:
        clock.tick(FPS)

        win_value = draw(WIN, images)
        if win_value:
            value = "main"
            return value


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        handle_keys(player1, player2)

        # Perform collision detection
        if player1.collide(TRACK_BORDER_MASK) is not None:
            player1.bounce()
        finish_poi_collide = player1.collide(FINISH_MASK, *FINISH_POSITION)
        if finish_poi_collide is not None:
            if finish_poi_collide[1] == 0:
                player1.bounce()
            else:
                return 'main'
            
        if player2.collide(TRACK_BORDER_MASK) is not None:
            player2.bounce()
        finish_poi_collide = player2.collide(FINISH_MASK, *FINISH_POSITION)
        if finish_poi_collide is not None:
            if finish_poi_collide[1] == 0:
                player2.bounce()
            else:
                return 'main'

        pygame.display.update()

    pygame.quit()
