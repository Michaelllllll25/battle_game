import pygame
import random
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

# game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

# define game variables 
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 15     # potion heals by 15
clicked = False      # look for a mouse click
game_over = 0


#define fonts
font = pygame.font.SysFont('Times New Roman', 26)

# define colours (rgb values)
red = (255, 0, 0)
green = (0, 255, 0)



#load images
#background image
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
#panel image
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
#button images
potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()
#load victory and defeat images
victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()
#sword image
sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()


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
    def __init__(self, x, y, name, max_hp, strength, potions):
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
        #load hurt images
        temp_list = []
        for i in range(3):          # 0-2
            img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png') # load image
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3)) # make image bigger
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load death images
        temp_list = []
        for i in range(10):          # 0-11
            img = pygame.image.load(f'img/{self.name}/Death/{i}.png') # load image
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
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        # set variables to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def attack(self, target):
        # deal damage to enemy
        rand = random.randint(-5, 5)      # random number between -5 and 5
        damage = self.strength + rand
        target.hp -= damage
        #run renemy hurt animation
        target.hurt()
        # Check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)                 # created an instance of damage_text
        damage_text_group.add(damage_text)                                                                    # usually it is append but this is a sprite group
        # set variables to attack aniation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):                                      # create hurt method
        # set variables to idle animation 
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):                                      # create death method
        # set variables to death animation 
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.framd_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()


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

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)           # inheriting properties of the sprite class
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # move damage text up
        self.rect.y -= 1         # reason why - y is 0 at top and increases down  the way so it decreases down the way
        # delete text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()        # delete this instance

damage_text_group = pygame.sprite.Group()              # create instances of damge text and add them to this group    



knight = Fighter(200, 260, 'Knight', 30, 10, 3)
bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)
bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp)

# create buttons
potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)              # creates an instance of the button class
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)              # creates an instance of the button class

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

    # draw the damage text
    damage_text_group.update()
    damage_text_group.draw(screen)          # these methods werent created, they alreaqdy exist, they were inhertited from sprite class

    # control player actions
    # reset action variables
    attack = False
    potion = False
    target = None
    # make sure mouse is visible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):              # pos (where mouse is)
            #hide mouse
            pygame.mouse.set_visible(False)
            #show sword in place of mouse cursor
            screen.blit(sword_img, pos)
            if clicked == True and bandit.alive == True:       # assures that if the bandit is dead you can't keep killing him
                attack = True
                target = bandit_list[count]  # tells which bandits have been clicked on making it the target
    if potion_button.draw():
        potion = True
    # show number of potions remaining
    draw_text(str(knight.potions), font, red, 150, screen_height - bottom_panel + 70)

    if game_over == 0:
        # player action
        if knight.alive == True:
            if current_fighter == 1:                   # know whos turn it is
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    # look for player action
                    # attack
                    if attack == True and target != None:    # (target != None) means target is not equal to none
                        knight.attack(target)
                        current_fighter += 1
                        action_cooldown = 0
                    #potion
                    if potion == True:
                        if knight.potions > 0:
                            # check if potion would heal the player beyond max health
                            if knight.max_hp - knight.hp > potion_effect:
                                heal_amount = potion_effect
                            else: 
                                heal_amount = knight.max_hp - knight.hp
                            knight.hp += heal_amount
                            knight.potions -= 1
                            damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)                 # created an instance of damage_text
                            damage_text_group.add(damage_text)                 
                            current_fighter += 1
                            action_cooldown = 0
        else: 
            game_over = -1


        # enemy action
        for count, bandit in enumerate(bandit_list):     # keeps running count using enumerate
            if current_fighter == 2 + count:
                if bandit.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        # check if bandit needs to heal first
                        if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:    # if bandits health is below half it needs to heal
                            # check if potion would heal the bandit beyond max health
                            if bandit.max_hp - bandit.hp > potion_effect:
                                heal_amount = potion_effect
                            else: 
                                heal_amount = bandit.max_hp - bandit.hp
                            bandit.hp += heal_amount
                            bandit.potions -= 1
                            damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green)                 # created an instance of damage_text
                            damage_text_group.add(damage_text)                        
                            current_fighter += 1
                            action_cooldown = 0

                        # attack
                        else:
                            bandit.attack(knight)
                            current_fighter += 1
                            action_cooldown = 0
                else:
                    current_fighter += 1

        # if all fighters have had a turn then reset
        if current_fighter > total_fighters:
            current_fighter = 1

    # check if all bandits are dead
    alive_bandits = 0             # assume they all dead
    for bandit in bandit_list:    # check if any alive
        if bandit.alive == True:
            alive_bandits += 1
    if alive_bandits == 0:
        game_over = 1

    # check if game is over
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250, 50))
        if game_over == -1:
            screen.blit(defeat_img, (290, 50))
        if restart_button.draw():
            knight.reset()
            for bandit in bandit_list:
                bandit.reset()
            current_fighter = 1
            action_cooldown
            game_over = 0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False   # if mouse is released clicked becomes false

    pygame.display.update()

pygame.quit()
