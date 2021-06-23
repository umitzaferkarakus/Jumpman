import pygame
from pygame.locals import *
from pygame import mixer
from Settings import *
from os import path
import random
import time
import mob
import CoinRope as CR


pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
clock = pygame.time.Clock()
# Font
font = pygame.font.SysFont('Snap ITC', 70)
font_score = pygame.font.SysFont('Snap ITC', 30)
font_author = pygame.font.SysFont('Snap ITC', 30)
# Screen display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)


# Play And Load Sounds
pygame.mixer.music.load('sounds/game.wav')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 0)
coin_sound = pygame.mixer.Sound('sounds/coin.wav')
coin_sound.set_volume(0.5)
jump_sound = pygame.mixer.Sound('sounds/jump.wav')
jump_sound.set_volume(0.5)
LevelUp_sound = pygame.mixer.Sound('sounds/level_up.wav')
LevelUp_sound.set_volume(0.5)
GameOver_sound = pygame.mixer.Sound('sounds/game_over.wav')
GameOver_sound.set_volume(0.1)

# Function for draw text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	win.blit(img, (x, y))

# Function for Reset Level
def reset_level(Level):
    player.restart(100, HEIGHT - 130)
    enemyX_group.empty()
    enemyY_group.empty()
    lava_group.empty()
    coin_group.empty()
    rope_group.empty()
    bullet_group.empty()


    if Level == 1:
        world_data = Map1
    if Level == 2:
        world_data = Map2
    if Level == 3:
        world_data = Map3
    world = World(world_data)
    return world

# Create Button
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.click = False

    def draw(self):
        status = False
        # mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                status = True
                self.click = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.click = False
        # draw button
        win.blit(self.image, self.rect)
        return status


class Player():
    def __init__(self, x, y):
        self.restart(x, y)

    def update(self, GameContinue):
        dx = 0
        dy = 0
        walk_cooldown = 5
        if GameContinue == 0:
            # Keypressed
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_sound.play()
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_UP] and self.climb == True:
                self.vel_y = -5
                if not pygame.sprite.spritecollide(self,rope_group,False):
                    self.climb == False
            if key[pygame.K_UP] == False:
                self.climb = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Player animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            if self.jumped == True:
                self.image = self.images_jump
            if key[pygame.K_SPACE] == False and key[pygame.K_UP] == False and key[pygame.K_RIGHT] == False and key[pygame.K_LEFT] == False:
                if self.direction == 1:
                    self.image = self.images_stand
                if self.direction == -1:
                    self.image = pygame.transform.flip(self.images_stand, True, False)
            # Gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # Collision
            self.in_air = True
            for tile in world.tile_list:
                # Collision in x
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Collision in y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # check for collision
            if pygame.sprite.spritecollide(self, enemyX_group, False):
                GameContinue = -1
            if pygame.sprite.spritecollide(self, enemyY_group, False):
                GameContinue = -1
            if pygame.sprite.spritecollide(self, lava_group, False):
                GameContinue = -1
            if pygame.sprite.spritecollide(self, spike_group, False):
                GameContinue = -1
            if pygame.sprite.spritecollide(self, bullet_group, False):
                GameContinue = -1
            if pygame.sprite.spritecollide(self,rope_group, False):
                self.climb = True
                self.image = pygame.image.load('img/p3_climb.png')
                self.image = pygame.transform.scale(self.image, (34, 40))


            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy
            if self.rect.x >= 770:
                self.rect.x = 770
            if self.rect.x <= 0:
                self.rect.x = 0
            if self.rect.y <= 0:
                self.rect.y = 0
            if self.rect.y >= 790:
                GameContinue = -1
        elif GameContinue == -1:
            self.image = self.dead_img
            if self.rect.y > 200:
                self.rect.y -= 5

        # draw player
        win.blit(self.image, self.rect)


        return GameContinue

    def restart(self, x, y):
        self.images_right = []
        self.images_left = []
        self.images_jump = pygame.image.load('img/p3_jump.png')
        self.images_jump = pygame.transform.scale(self.images_jump,(35,40))
        self.images_stand = pygame.image.load('img/p3_stand.png')
        self.images_stand = pygame.transform.scale(self.images_stand, (35, 40))
        self.index = 0
        self.counter = 0
        for num in range(1, 11):
            img_right = pygame.image.load(f'img/P3_walk{num}.png')
            img_right = pygame.transform.scale(img_right, (35, 40))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_img = pygame.image.load('img/ghost_dead.png')
        self.dead_img = pygame.transform.scale(self.dead_img, (35,40))
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True
        self.climb = False


class World():
    def __init__(self, data):
        self.tile_list = []

        # load images
        block_img = pygame.image.load('img/stone1.png')
        grass_img = pygame.image.load('img/stone.png')
        castle_img = pygame.image.load('img/castle.png')
        castleWall_img = pygame.image.load('img/castle_wall.png')
        snow_img = pygame.image.load('img/snow1.png')
        snowWall_img = pygame.image.load('img/snow_wall.png')

        rowCount = 0
        for row in data:
            colCount = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(block_img, (tileSize, tileSize))
                    img_rect = img.get_rect()
                    img_rect.x = colCount * tileSize
                    img_rect.y = rowCount * tileSize
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tileSize, tileSize))
                    img_rect = img.get_rect()
                    img_rect.x = colCount * tileSize
                    img_rect.y = rowCount * tileSize
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    enemy = mob.EnemyX(colCount * tileSize, rowCount * tileSize)
                    enemyX_group.add(enemy)
                if tile == 4:
                    coin = CR.Coin(colCount * tileSize, rowCount * tileSize)
                    coin_group.add(coin)
                if tile == 5:
                    rope = CR.Rope(colCount * tileSize, rowCount * tileSize)
                    rope_group.add(rope)
                if tile == 6:
                    lava = mob.Lava(colCount * tileSize, rowCount * tileSize + (tileSize // 2))
                    lava_group.add(lava)
                if tile == 7:
                    bat = mob.EnemyY(colCount * tileSize, rowCount * tileSize)
                    enemyY_group.add(bat)
                if tile == 8:
                    img = pygame.transform.scale(castle_img, (tileSize, tileSize))
                    img_rect = img.get_rect()
                    img_rect.x = colCount * tileSize
                    img_rect.y = rowCount * tileSize
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 9:
                    img = pygame.transform.scale(castleWall_img, (tileSize, tileSize))
                    img_rect = img.get_rect()
                    img_rect.x = colCount * tileSize
                    img_rect.y = rowCount * tileSize
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 10:
                    img = pygame.transform.scale(snowWall_img, (tileSize, tileSize))
                    img_rect = img.get_rect()
                    img_rect.x = colCount * tileSize
                    img_rect.y = rowCount * tileSize
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 11:
                    img = pygame.transform.scale(snow_img, (tileSize, tileSize // 2))
                    img_rect = img.get_rect()
                    img_rect.x = colCount * tileSize
                    img_rect.y = rowCount * tileSize
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 12:
                    spike = mob.Spike(colCount * tileSize, rowCount * tileSize + (tileSize // 2))
                    spike_group.add(spike)

                colCount += 1
            rowCount += 1

    def draw(self):
        for tile in self.tile_list:
            win.blit(tile[0], tile[1])



player = Player(100, HEIGHT - 130)
#Sprite Group
enemyX_group = pygame.sprite.Group()
enemyY_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
rope_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
for i in range(1):
    b = mob.Bullet()
    bullet_group.add(b)
    bullet_group.add(b)

if Level == 1 :
    world_data = Map1
if Level == 2 :
    world_data = Map2
if Level == 3 :
    world_data = Map3
world = World(world_data)

# create buttons
restart_btn = Button(WIDTH - 500  , HEIGHT // 2 , restart_img)
start_btn = Button(WIDTH // 2 - 120, HEIGHT - 300 , start_img)
exit_btn = Button(WIDTH // 2 - 120, HEIGHT -150, exit_img)

run = True
while run:

    clock.tick(FPS)

    win.blit(bg_img,(0,0))

    if mainMenu == True:
        win.blit(mainBG_img,(0,0))
        draw_text('Zafer Karakuş',font_author,WHITE,540,750)
        if exit_btn.draw():
            run = False
        if start_btn.draw():
            mainMenu = False
    else:
        world.draw()
        # Game Continues
        if GameContinue == 0:
            enemyX_group.update()
            enemyY_group.update()
            bullet_group.update()
            draw_text('X ' + str(Score), font_score, WHITE, 45, 45)
            # Collect Coin
            if pygame.sprite.spritecollide(player, coin_group, True):
                coin_sound.play()
                Score += 10
                if len(coin_group) == 0:
                    GameContinue = 1
                    LevelUp_sound.play()

        #Display
        enemyX_group.draw(win)
        enemyY_group.draw(win)
        coin_group.draw(win)
        lava_group.draw(win)
        rope_group.draw(win)
        bullet_group.draw(win)
        spike_group.draw(win)

        GameContinue = player.update(GameContinue)

        # if player die
        if GameContinue == -1:
            GameOver_sound.play(0)
            if restart_btn.draw():
                world_data = []
                world = reset_level(Level)
                GameContinue = 0
                Score = 0

        #Next Level
        if GameContinue == 1:
            Level +=1
            time.sleep(0.5)
            if Level <= MaxLevel:
                #New Level
                world_data = []
                world = reset_level(Level)
                GameContinue = 0
            else:
                draw_text('YOU WIN!', font, WHITE, (WIDTH // 2) - 200, HEIGHT // 2 - 100)
                draw_text('SCORE:' + str(Score), font, WHITE, (WIDTH // 2) - 170, HEIGHT // 2)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()