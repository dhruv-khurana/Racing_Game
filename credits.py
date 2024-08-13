import pygame
import button  # Ensure this module and Button class are implemented correctly

def credits():
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

    run = True
    while run:

        main_screen.fill(BG_COLOR)
        
        draw_text("Credits", font_large, TEXT_COL, 325, 100)
        draw_text("Developers:", font_medium, TEXT_COL, 75, 200)
        draw_text("Ben Wallace, CEO", font_small, TEXT_COL, 75, 250)
        draw_text("Dhruv Khurana, Main Programmer", font_small, TEXT_COL, 75, 300)
        draw_text("Aaron Lin, UI Design/Programmer", font_small, TEXT_COL, 75, 350)

        draw_text("Special Thanks to:", font_medium, TEXT_COL, 475, 200)
        draw_text("Franklin, For Help", font_small, TEXT_COL, 475, 250)
        draw_text("Chat GPT, Backup Code Debugger", font_small, TEXT_COL, 475, 350)
        draw_text("YouTube, Tutorial Videos", font_small, TEXT_COL, 475, 400)

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
