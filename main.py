import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

# game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')


#define fonts
font = pygame.font.SysFont('Times New Roman', 26)

# define colours (rgb values)
red = (255, 0, 0)
green = (0, 255, 0)



# Load images
# Background image
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
#pannel image
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()

# Create function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x , y))

# Function for drawing background
def draw_background():
    screen.blit(background_img, (0, 0))

# Function for drawing panel
def draw_panel():
    # draW panel rectangle
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    # show knight state
    draw_text(f"{knight.name} HP: {knight.hp}", font, red, 100, screen_height - bottom_panel + 10)
    for count, i in enumerate(bandit_list):
        # show name and health
        draw_text(f"{i.name} HP: {i.hp}", font, red, 550, (screen_height - bottom_panel + 10) + count * 60)


# Fighter class
class Fighter():
    def __init__(self, x, y, name, max_hp,   strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0         # 0 is idle, 1: attack, 2: hurt, 3: dead
        self.update_time = pygame.time.get_ticks()
        #load idle images
        temp_list = []
        for i in range(8):          # 0-7
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png') # load image
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3)) # make image bigger
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load attack images
        temp_list = []
        for i in range(8):          # 0-7
            img = pygame.image.load(f'img/{self.name}/Attack/{i}.png') # load image
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3)) # make image bigger
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if animation has run out reset back to start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    # Draw the class
    def draw(self):
        screen.blit(self.image, self.rect)


class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        # update with new health
        self.hp = hp
        # calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))





knight = Fighter(200, 260, 'Knight', 30, 10, 3)
bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)
bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp)

# knight.hp = 15

run = True
while run:

    clock.tick(fps)

    # Draw background
    draw_background()

    # Draw background
    draw_panel()
    knight_health_bar.draw(knight.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)

    # Draw Fighters
    knight.update()
    knight.draw()
    for bandit in bandit_list:
        bandit.update()
        bandit.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
