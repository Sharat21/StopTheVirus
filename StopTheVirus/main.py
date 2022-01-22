'''
PyJaC: Rebooted Hackathon - Beginner Category
Team #23 - T.I.D.E Tech (Thinking, Innovating, Designing, Executing)
Group Members: Aditya Kumar, Sharat Krishnan, Jay Patel
Prompts: Create an interactive game
         Write a Program that has an Element of Randomness in it

Stop The Virus!
This is a fun game (inspired from very real events) which involves player attempting
to shoot down as many viruses as they can using the vaccine. The viruses are falling
down from random locations while also shooting infectors which the player must dodge.
The player has the ability to move left to right and also shoot at any angle.

Instructions:
Use 'a' key to move left and the 'd' key to move right
Use the mouse key to aim and click to shoot at the specified angle

NOTE: This is not an accurate depiction of how viruses work. It's just a fun video game!
'''
import pygame
import random
import math
from pygame import mixer

pygame.init()

# Constants/Global Variables representing colors, sizes etc.
white = (229, 235, 235)
player_colour = (210, 87, 27)
background = (28, 27, 27)
grid_w = 800
grid_l = 600
block_size = 15
block_virus = 35
block_virus_bullet = 25
block_vaccine_x = 40
block_vaccine_y = 120
block_vaccine_bullet = 40
angle = 0
score_count = 0

# Constants/Global Variables involving the pygame library
clock = pygame.time.Clock()
game_screen = pygame.display.set_mode((grid_w, grid_l))
font_style = pygame.font.SysFont("bahnschrift", 25)
start_img = pygame.image.load('start_button.png').convert_alpha()
start_img = pygame.transform.scale(start_img, (250, 100))
end_img = pygame.image.load('exit_button.png').convert_alpha()
end_img = pygame.transform.scale(end_img, (250, 100))
score_font = pygame.font.SysFont("comicsansms", 40)

pygame.display.set_caption('Stop The Virus!')


class Button:
    def __init__(self, x: int, y: int, image) -> None:
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self) -> bool:
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        game_screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


# Class for movement and drawings of all entities on screen
class Block:
    def __init__(self, x: float, y: float = -10) -> None:
        self.x = x
        self.y = y
        self.virus = pygame.image.load("COVID19.png")
        self.virus = pygame.transform.scale(self.virus,
                                            (block_virus, block_virus))
        self.virus_bullet = pygame.image.load("virus_bullet.png")
        self.virus_bullet = pygame.transform.scale(self.virus_bullet, (
            block_virus_bullet, block_virus_bullet))
        self.life = pygame.image.load("life.png")
        self.life = pygame.transform.scale(self.life, (
            block_vaccine_bullet, block_vaccine_bullet))
        self.syrange_image = pygame.image.load("vaccine.png")
        self.syrange_image = pygame.transform.scale(self.syrange_image, (
            block_vaccine_x, block_vaccine_y))

    def draw_virus(self) -> None:
        game_screen.blit(self.virus, [self.x, self.y, block_virus, block_virus])
        self.rect = pygame.Rect(self.x, self.y, block_virus, block_virus)

    def draw_virus_bullet(self) -> None:
        game_screen.blit(self.virus_bullet, [self.x, self.y, block_virus_bullet,
                                             block_virus_bullet])
        self.rect = pygame.Rect(self.x, self.y, block_virus_bullet,
                                block_virus_bullet)

    def draw_vaccine(self, ang: float = 0) -> None:
        if ang < -200:
            ang = 35
        if ang < -20:
            ang = -20
        if ang > 35:
            ang = 35
        image = pygame.transform.rotate(self.syrange_image, ang)
        game_screen.blit(image,
                         [self.x, self.y, block_vaccine_x, block_vaccine_y])
        self.rect = pygame.Rect(self.x, self.y, block_vaccine_x + 20,
                                block_vaccine_y + 20)

    def draw_vaccine_bullet(self) -> None:
        game_screen.blit(self.life, [self.x, self.y, block_vaccine_bullet,
                                     block_vaccine_bullet])
        self.rect = pygame.Rect(self.x, self.y, block_vaccine_bullet,
                                block_vaccine_bullet)

    # Virus movement
    def enemy_move(self) -> None:
        self.y += 7  # 2
        self.draw_virus()

    # Virus shooting
    def enemy_shoot(self) -> None:
        self.y += 10
        self.draw_virus_bullet()

    # Player shooting Vaccine
    def player_shoot(self) -> None:
        self.y -= 10
        self.draw_vaccine_bullet()

    def __eq__(self, other) -> bool:
        return self.rect.colliderect(other.rect)


# Class for angle shooting enemies
class Shooting(Block):
    def __init__(self, x: float, y: float, targetx: float, targety: float):
        super().__init__(x, y)
        self.targetx = targetx
        self.targety = targety
        self.angle = math.atan2(targety - y, targetx - x)
        self.degrees = self.angle * 180 / math.pi
        self.x = x
        self.y = y
        if self.angle > 2.25:
            self.angle = -2.25
        if self.angle < -2.25:
            self.angle = -2.25
        elif self.angle > -1.2:
            self.angle = -1.2
        self.Fx = 20 * math.cos(self.angle)
        self.Fy = 20 * math.sin(self.angle)

    def shot_bullet(self) -> None:
        self.x = self.x + self.Fx
        self.y = self.y + self.Fy
        super().draw_vaccine_bullet()


# Function for the starting menu of the game
def main_menu() -> None:
    game_close = False
    mixer.music.load("jpjp.wav")
    mixer.music.play(-1)
    while not game_close:
        game_start_bg = pygame.image.load('pixel-city-chill.gif')
        game_start_bg = pygame.transform.scale(game_start_bg, (800, 600))

        title_img = pygame.image.load('intro.png')
        title_img = pygame.transform.scale(title_img, (600, 500))
        game_screen.blit(game_start_bg, [0, 0])
        game_screen.blit(title_img, [125, -100])
        for event in pygame.event.get():

            if not event.type == pygame.KEYDOWN:
                if start_button.draw():
                    mixer.music.stop()
                    game()
                if end_button.draw():
                    mixer.music.stop()
                    pygame.quit()
                    quit()
                pygame.display.update()
            else:
                game()


# Bullet and Virus Collision
def shooting_enemies(list_bullets: list, list_enemies: list) -> bool:
    for j in reversed(range(len(list_bullets))):
        for i in reversed(range(len(list_enemies))):
            if list_bullets[j] == list_enemies[i]:
                list_enemies.pop(i)
                list_bullets.pop(j)
                return True
    return False


#  Virus/Virus Bullet and Player Collision
def death(list_player: list, list_enemies: list) -> bool:
    for j in reversed(range(len(list_player))):
        for i in reversed(range(len(list_enemies))):
            if list_player[j] == list_enemies[i]:
                return True
    return False


# Scoreboard
def player_score(game_score: int) -> None:
    value = score_font.render("  Score: " + " " + str(game_score), True, white)
    game_screen.blit(value, [grid_w / 2, grid_l / 3])


def message2(msg: str, color: str) -> None:
    mesg = score_font.render(msg, True, color)
    game_screen.blit(mesg, [135, 15])


def message3_behind(msg: str, color: str) -> None:
    mesg = score_font.render(msg, True, color)
    game_screen.blit(mesg, [138, 15])


def high_score(msg: str, color: str) -> None:
    mesg = score_font.render(msg, True, color)
    game_screen.blit(mesg, [450, 265])


def highscore_behind(msg: str, color: str) -> None:
    mesg = score_font.render(msg, True, color)
    game_screen.blit(mesg, [453, 265])


def score(msg: str, color: str) -> None:
    mesg = score_font.render(msg, True, color)
    game_screen.blit(mesg, [450, 200])


def score_behind(msg: str, color: str) -> None:
    mesg = score_font.render(msg, True, color)
    game_screen.blit(mesg, [450, 200])


def message(msg: str, color: tuple) -> None:
    mesg = font_style.render(msg, True, color)
    game_screen.blit(mesg, [grid_w / 6, grid_l / 3])


# Sound effects when game ends
def game_crash_sound() -> None:
    mixer.music.load("Game Voice.wav")
    mixer.music.stop()
    mixer.music.load("Game Over.wav")
    mixer.music.play()
    mixer.music.stop()


highscore_lst = []
start_button = Button(275, 300, start_img)
end_button = Button(275, 450, end_img)


# The Game Function that implements features of the game
def game() -> None:
    game_over = False
    game_close = False
    x1_change = 0
    x1 = grid_w / 2
    y1 = 450
    list_bullets = []
    list_enemies = []
    list_bullet_enemy = []
    max_spawn = 80
    max_spawn_enemies = 80
    player_lst = []
    count_score = 0
    player_score(count_score)
    score_img = pygame.image.load('score_card.png').convert_alpha()
    score_img = pygame.transform.scale(score_img, (120, 50))
    mixer.music.load("game_music.wav")
    mixer.music.play(-1)

    # The periodic loop that runs until the game is ended
    while not game_over:
        while game_close:
            global highscore_lst
            highscore_lst.append(count_score)
            max_score = max(highscore_lst)
            highscore_img = pygame.image.load('higscore.png').convert_alpha()
            highscore_img = pygame.transform.scale(highscore_img, (150, 95))
            game_crash_sound()
            restart_bg = pygame.image.load('bg.png')
            restart_bg = pygame.transform.scale(restart_bg, (800, 600))
            game_screen.blit(restart_bg, [0, 0])

            replay_img = pygame.image.load('replay.png')
            replay_img = pygame.transform.scale(replay_img, (180, 90))

            home_img = pygame.image.load('home_new.png').convert_alpha()
            home_img = pygame.transform.scale(home_img, (165, 70))

            over_text = pygame.image.load('game_over.png')
            over_text = pygame.transform.scale(over_text, (250, 130))
            game_screen.blit(highscore_img, [250, 260])
            game_screen.blit(score_img, [250, 200])

            lime_green = (224, 255, 255)
            black = (0, 0, 0)
            highscore_behind(str(max_score), black)
            high_score(str(max_score), lime_green)
            score_behind(str(count_score), lime_green)
            score(str(count_score), lime_green)

            game_screen.blit(over_text, [250, 50])
            replay_button = Button(275, 350, replay_img)
            home_button = Button(280, 450, home_img)
            if replay_button.draw():
                mixer.music.stop()
                game()
            if home_button.draw():
                mixer.music.stop()
                main_menu()
            pygame.display.update()

            # Looking at user input through keyboard
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game()

        # Looking at user input through keyboard
        for event in pygame.event.get():
            global angle
            if event.type == pygame.QUIT:
                game_over = True
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_a]:
                x1_change = -block_size * 2
            elif pressed[pygame.K_d]:
                x1_change = block_size * 2
            elif pressed[pygame.K_ESCAPE]:
                game_over = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                coordinates = pygame.mouse.get_pos()
                bullet = Shooting(x1, y1, coordinates[0], coordinates[1])
                angle = -90 - bullet.degrees
                if angle < 0:
                    bullet.x += 20
                list_bullets.append(bullet)
            if event.type == pygame.MOUSEMOTION:
                coordinates = pygame.mouse.get_pos()
                bullet = Shooting(x1, y1, coordinates[0], coordinates[1])
                angle = -90 - bullet.degrees

        if x1 > block_size and x1_change < 0:
            x1 += x1_change
        elif x1 < (grid_w - block_size * 4) and x1_change > 0:
            x1 += x1_change

        x1_change = 0
        main_bg = pygame.image.load('game_background.png').convert_alpha()
        main_bg = pygame.transform.scale(main_bg, (800, 600))
        game_screen.blit(main_bg, [0, 0])
        enemies_x = round(
            random.randrange(0, (grid_w - block_size * 4)) / 10.0) * 10.0

        # Randomly spawns enemies at random positions
        if random.randint(12, max_spawn) == 15:
            list_enemies.append(Block(enemies_x))
            if max_spawn > 15:
                max_spawn -= 1

        player = Block(x1, y1)
        player.draw_vaccine(angle)
        player_lst.append(player)
        if len(player_lst) == 0:
            player_lst.append(player)
        else:
            player_lst.append(player)
            player_lst = [player_lst[-1]]

        for i in range(len(list_enemies)):
            if random.randint(0, max_spawn_enemies) == 15:
                list_bullet_enemy.append(
                    Block(list_enemies[i].x + 5, list_enemies[i].y))
                if max_spawn_enemies > 15:
                    max_spawn_enemies += -1
            list_enemies[i].enemy_move()

        for i in range(len(list_bullet_enemy)):
            list_bullet_enemy[i].enemy_shoot()

        for i in range(len(list_bullets)):
            if type(list_bullets[i]) == Block:
                list_bullets[i].player_shoot()
            else:
                list_bullets[i].shot_bullet()

        for i in range(len(list_enemies)):
            if list_enemies[i].y > 600:
                game_close = True

        for i in range(len(list_bullet_enemy)):
            if list_bullet_enemy[i].y > 600:
                game_close = True

        if shooting_enemies(list_bullets, list_enemies):
            count_score += 1
        if shooting_enemies(list_bullets, list_bullet_enemy):
            count_score += 1

        if death(player_lst, list_bullet_enemy):
            game_close = True
        if death(player_lst, list_enemies):
            game_close = True
        lime_green = (224, 255, 255)
        black = (0, 0, 0)
        game_screen.blit(score_img, [8, 20])
        message3_behind(str(count_score), black)
        message2(str(count_score), lime_green)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    quit()


main_menu()
