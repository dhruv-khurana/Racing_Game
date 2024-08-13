import pygame
from Single_Player import show_leaderboard
import json
import os
import button

pygame.init()

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load button image
back_img = pygame.image.load("images/Back").convert_alpha()

# Create back button instance
back_button = button.Button(-75, 200, back_img, 1)  # Adjust position and scale as needed

# Define colors
TEXT_COL = (0, 0, 0)
BG_COLOR = (157, 217, 243)  # Light blue

# Define fonts
font_large = pygame.font.SysFont("Arial Black", 40)
font_medium = pygame.font.SysFont("Arial Black", 25)
font_small = pygame.font.SysFont("Arial Black", 15)

clock = pygame.time.Clock()
WIN = pygame.display.set_mode((800, 600))

# Load high scores from file
def load_high_scores():
    global high_scores
    if os.path.exists("the_high_scores.json"):
        with open("the_high_scores.json", "r") as file:
            high_scores = json.load(file)

# Show leaderboard
def show_leaderboard(main_screen, high_scores):
    main_screen.fill(BG_COLOR)
    title_surf = font_large.render("Leaderboard", True, TEXT_COL)
    main_screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 50))
    for i, score in enumerate(high_scores):
        initials = score["initials"]
        time = f'{score["score"] / 1000:.2f}s'
        score_surf = font_medium.render(f"{i + 1}. {initials}: {time}", True, TEXT_COL)
        main_screen.blit(score_surf, (SCREEN_WIDTH // 2 - score_surf.get_width() // 2, 150 + i * 30))
    back_button.draw(main_screen)
    pygame.display.flip()

# Rankings function
def rankings():
    run = True
    FPS = 60
    show_leaderboard_flag = True
    load_high_scores()
    while run:
        clock.tick(FPS)
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 265<= pos[0] <= 550 and 490 <= pos[1] <= 565:
                    value = "main"
                    return value

        if show_leaderboard_flag:
            show_leaderboard(main_screen, high_scores)
        back_button.draw(main_screen)  # Ensure button.draw() method is implemented
    
        pygame.display.update()

    pygame.quit()
