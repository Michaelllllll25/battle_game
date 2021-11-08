import pygame

pygame.init()

# game window
bottom_panel = 260
screen_width = 555
screen_height = 500 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')


# Load images
# Background image
background_img = pygame.image.load('img/Background/8bTWrwW.jpg').convert_alpha()
#pannel image
panel_img = pygame.image.load('img/Icons/panel.jpg').convert_alpha()


# Function for drawing background
def draw_background():
    screen.blit(background_img, (0, 0))

# Function for drawing panel
def draw_panel():
    screen.blit(panel_img, (0, screen_height - bottom_panel))


run = True
while run:
    # Draw background
    draw_background()

    # Draw background
    draw_panel()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
