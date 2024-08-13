import pygame
import button  # Ensure this module and Button class are implemented correctly

def settings():
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Credits")

    back_img = pygame.image.load("images/Back.png").convert_alpha()

    back_button = button.Button(-75, 200, back_img, 1)  # Position adjusted for visibility

    # Define colors
    TEXT_COL = (0, 0, 0)
    BG_COLOR = (157, 217, 243)  # Light blue

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        main_screen.blit(img, (x, y))

    font_large = pygame.font.SysFont("Arial Black", 40)
    font_medium = pygame.font.SysFont("Arial Black", 25)
    font_small = pygame.font.SysFont("Arial Black", 15)

    #load button images
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


    run = True
    while run:

        main_screen.fill(BG_COLOR)
            
        pos = pygame.mouse.get_pos()
        time_trials_button.draw(main_screen)
        vs_mode_button.draw(main_screen)
        rankings_button.draw(main_screen) 
        settings_button.draw(main_screen)      
        credits_button.draw(main_screen)
        draw_text("Settings Page", font_large, TEXT_COL, 250, 100)

        back_button.draw(main_screen)  # Ensure button.draw() method is implemented

        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 265<= pos[0] <= 550 and 490 <= pos[1] <= 565:
                    value = "main"
                    return value

        pygame.display.update()

    pygame.quit()
