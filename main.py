import pygame
import button
from utils import *
from Single_Player import *
from credits import credits
from settings import settings
from rankings import *
from Multi_Player import *

pygame.init()

#create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")


#game variables
game_paused = False
menu_state = "main"

#define fonts
font = pygame.font.SysFont("arialblack", 20)

#define colours
TEXT_COL = (255, 255, 255)

#load button images
title_screen_img = pygame.image.load("images/Title_Screen.png").convert_alpha()
rankings_img = pygame.image.load("images/Rankings_Button.png").convert_alpha()
credits_img = pygame.image.load("images/Credits_Button.png").convert_alpha()
settings_img = pygame.image.load('images/Settings_Button.png').convert_alpha()
time_trials_img = pygame.image.load('images/Time_Trials_Button.png').convert_alpha()
vs_mode_img = pygame.image.load('images/VS_Mode_Button.png').convert_alpha()
back_img = pygame.image.load("images/Back.png").convert_alpha()


#create button instances
rankings_button = button.Button(-250, 200, rankings_img, 1)
credits_button = button.Button(450, 400, credits_img, 0.5)
settings_button = button.Button(-250, 100, settings_img, 1)
time_trials_button = button.Button(-250, -100, time_trials_img, 1)
vs_mode_button = button.Button(-250, 0, vs_mode_img, 1)
back_button = button.Button(-100, 200, back_img, 1)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  main_screen.blit(img, (x, y))

#game loop
run = True
game_paused = True
while run:
    pos = pygame.mouse.get_pos()
    #check if game is paused
    
    #check menu state
    if menu_state == "main":
      main_screen.blit(title_screen_img, (0, 0))
      time_trials_button.draw(main_screen)
      vs_mode_button.draw(main_screen)
      rankings_button.draw(main_screen) 
      settings_button.draw(main_screen)      
      credits_button.draw(main_screen)
    elif menu_state == "play_game":
      value = play_game()
      if value == "main":
        menu_state = "main"
      print(menu_state)
    elif menu_state == "multiplayer":
      value = multiplayer()
      if value == "main":
        menu_state = "main"
    elif menu_state == "settings":
      value = settings()
      if value == "main":
        menu_state = "main"
    elif menu_state == "rankings":
      value = rankings()
      if value == "main":
        menu_state = "main"
    elif menu_state == "credits":
      value = credits()
      if value == "main":
        menu_state = "main"

    #event handler
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        print("Game is being quit in start page, in for loop")
        
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          game_paused = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if menu_state == "main":
          if 85<= pos[0] <= 375 and 215 <= pos[1] <= 300:
            menu_state = "play_game"
          elif 85<= pos[0] <= 375 and 320 <= pos[1] <= 400:
            menu_state = "multiplayer"
          elif 85<= pos[0] <= 375 and 415 <= pos[1] <= 500:
            menu_state = "settings"
          elif 85<= pos[0] <= 375 and 520 <= pos[1] <= 600:
            menu_state = "rankings"
          elif 620<= pos[0] <= 765 and 560 <= pos[1] <= 600:
            menu_state = "credits"
        else:
          if 235<= pos[0] <= 525 and 490 <= pos[1] <= 570:
            menu_state = "main"

    pygame.display.update()


pygame.quit()
