import pygame
import Settings
import random
class EnemyX(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/enemy.png')
        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class EnemyY(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/bat.png')
        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0


    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 1
        if self.move_counter % 25 <= 5:
            self.image = pygame.image.load('img/bat2.png')
            self.image = pygame.transform.scale(self.image, (40,40))
        else:
            self.image = pygame.image.load('img/bat.png')
            self.image = pygame.transform.scale(self.image, (40, 40))
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (40,20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/spikes.png')
        self.image = pygame.transform.scale(img, (40,20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/fly.png')
        self.image = pygame.transform.scale(self.image, (40, 20))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,10)
        self.rect.y = random.randrange(0,600)
        self.speedy = random.randrange(1,5)


    def update(self):
        self.rect.x += self.speedy
        if self.rect.x % 20 <= 16:
            self.image = pygame.image.load('img/fly2.png')
            self.image = pygame.transform.scale(self.image, (40, 20))
        else:
            self.image = pygame.image.load('img/fly.png')
            self.image = pygame.transform.scale(self.image, (40, 20))
        if self.rect.x > 800 - 15:
            self.rect.x = random.randrange(0,10)
            self.rect.y = random.randrange(0, 600)
            self.speedy = random.randrange(1, 5)