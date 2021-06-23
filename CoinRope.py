import pygame

class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/coin.png')
		self.image = pygame.transform.scale(img, (25 , 25))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)




class Rope(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/stairs.png')
        self.image = pygame.transform.scale(img, (30, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y