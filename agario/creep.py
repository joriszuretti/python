from random import random

import pygame

from pygame.math import Vector2

class Creep:
    def __init__(self):
        self.position = Vector2(0, 0)
        self.taille = 10
        self.couleur = (random.init(255, 0, 0),random.init(0, 255, 0),random.init(0, 0, 255))
        self.masse = 10

    def update(self):
        self.position.x += random.randint(0,5)
        self.position.y += random.randint(0.5)

    def show (self,screen):
        pygame.draw.circle(screen,self.couleur,[int(self.position.x),int(self.position.y)],self.taille)