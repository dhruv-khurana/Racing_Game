import pygame
import math
import os
import json
from pygame import mixer
from utils import scale_image, blit_rotate_center

# Initialize Pygame and Mixer
pygame.init()
mixer.init()

# Load music
mixer.music.load("images/Music")
mixer.music.set_volume(0.4)
mixer.music.play()

# Font setup
font = pygame.font.SysFont("Arial Black", 20)
font_large = pygame.font.SysFont("Arial Black", 40)
font_medium = pygame.font.SysFont("Arial Black", 25)
font_small = pygame.font.SysFont("Arial Black", 15)

# Load and scale images
TRACK = scale_image(pygame.image.load("images/Track.png"), 0.85)
TRACK_BORDER = scale_image(pygame.image.load("images/Track_Border"), 0.85)
FINISH = scale_image(pygame.image.load("images/Finish_Line"), 0.65)
RED_CAR = scale_image(pygame.image.load("images/Red_Car"), 0.015)
BACKGROUND = scale_image(pygame.image.load("files/imgs/Background_Image"), 15)

# Get dimensions and create masks
track_width, track_height = TRACK.get_width(), TRACK.get_height()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (375, 60)

# Initialize Pygame window
WIN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Turbo Tracks")
clock = pygame.time.Clock()

# Define colors
TEXT_COL = (0, 0, 0)
BG_COLOR = (157, 217, 243)  # Light blue

# Load high scores from file
high_scores = []
def load_high_scores():
    global high_scores
    if os.path.exists("the_high_scores.json"):
        with open("the_high_scores.json", "r") as file:
            high_scores = json.load(file)

# Save high scores to file
def save_high_scores():
    with open("the_high_scores.json", "w") as file:
        json.dump(high_scores, file)

# Handle high scores and initials
def handle_high_scores(score):
    global high_scores, show_leaderboard_flag, leaderboard_start_time
    high_scores.append({"score": score, "initials": enter_initials()})
    high_scores = sorted(high_scores, key=lambda x: x["score"], reverse=False)[:10]
    save_high_scores()
    show_leaderboard_flag = True
    leaderboard_start_time = pygame.time.get_ticks()

# Enter initials
def enter_initials():
    initials = ""
    while len(initials) < 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(initials) == 3:
                    return initials
                elif pygame.K_a <= event.key <= pygame.K_z:
                    initials += chr(event.key).upper()
        screen.fill((BG_COLOR))
        font = pygame.font.Font(None, 36)
        initials_surf = font.render(f"Enter your initials: {initials}", True, (0,0,0))
        screen.blit(initials_surf, (screen_width // 2 - initials_surf.get_width() // 2, screen_height // 2))
        pygame.display.flip()
        clock.tick(60)
    return initials

def show_leaderboard(main_screen, high_scores):
    main_screen.fill(BG_COLOR)
    font = pygame.font.Font(None, 36)
    title_surf = font.render("Leaderboard", True, TEXT_COL)
    main_screen.blit(title_surf, (screen_width // 2 - title_surf.get_width() // 2, 50))
    for i, score in enumerate(high_scores):
        initials = score["initials"]
        time = f'{score["score"] / 1000:.2f}s'
        score_surf = font.render(f"{i + 1}. {initials}: {time}", True, (0,0,0))
        main_screen.blit(score_surf, (screen_width // 2 - score_surf.get_width() // 2, 100 + i * 30))
    main_screen.blit(font.render("Press Space to Continue", True, (0,0,0)), (screen_width // 2 - score_surf.get_width() +25 // 2, 500))
    pygame.display.flip()

# Define abstract car class
class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = -90
        self.x, self.y = self.START_POS
        self.acceleration = 0.5
        self.bounce_factor = 0.7

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win, offset):
        blit_rotate_center(win, self.img, (self.x - offset[0], self.y - offset[1]), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
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
        return mask.overlap(car_mask, offset)

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = -90
        self.vel = 0

    def bounce(self):
        self.vel *= -self.bounce_factor
        radians = math.radians(self.angle)
        self.x += math.sin(radians) * 10
        self.y += math.cos(radians) * 10
        self.vel = 0

# Define player car class
class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (440, 60)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

# Define game functions
def draw(win, images, player_car, curr):
    offset = (player_car.x - WIN.get_width() // 2, player_car.y - WIN.get_height() // 2)
    win.blit(BACKGROUND, (0, 0))
    for img, pos in images:
        win.blit(img, (pos[0] - offset[0], pos[1] - offset[1]))
    player_car.draw(win, offset)
    win.blit(font.render('Current Time: ' + (f'{curr / 1000:.2f}s'), True, (255, 255, 255)), (10, 50))
    pygame.display.update()

def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False
    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
        player_car.acceleration = 0.3 if keys[pygame.K_LSHIFT] else 0.02
    if keys[pygame.K_r]:
        player_car.reset()
        global start_time
        start_time = pygame.time.get_ticks()
    if not moved:
        player_car.reduce_speed()

def play_game():
    player_car = PlayerCar(50, 5)
    run = True
    FPS = 60

    images = [(TRACK_BORDER, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POSITION)]
    start_time = pygame.time.get_ticks()
    show_leaderboard_flag = False
    start_time = 0
    while run:
        clock.tick(FPS)
        elapsed_time = pygame.time.get_ticks() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if show_leaderboard_flag:
            show_leaderboard(WIN, high_scores)
            if keys[pygame.K_SPACE]:  # 4 seconds
                show_leaderboard_flag = False
                start_time = pygame.time.get_ticks()
                value = "main"
                return value

        else:
            draw(WIN, images, player_car, elapsed_time)
            move_player(player_car)

        # Perform collision detection
        if player_car.collide(TRACK_BORDER_MASK) is not None:
            player_car.bounce()
        finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
        if finish_poi_collide is not None:
            if finish_poi_collide[1] == 0:
                player_car.bounce()
            else:
                if elapsed_time > 50:  # Adding a minimal time threshold to prevent immediate finish detection
                    load_high_scores()
                    handle_high_scores(elapsed_time)
                    player_car.reset()
                    show_leaderboard_flag = True
                    start_time = pygame.time.get_ticks()

    pygame.quit()

if __name__ == "__main__":
    play_game()
