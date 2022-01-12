import random

from pygame.math import Vector2
import core

class Proie:
    def __init__(self):
        #self.position = Vector2(0,0)
        self.position = Vector2(random.randint(0, 400), random.randint(0, 400))
        #self.vitesse = Vector2(0,0)
        self.vitesse = Vector2(random.uniform(-5, 5), random.uniform(-5, 5))
        self.acceleration = Vector2(0,0)
        self.vivante = True

        self.couleur = (0,255,0)
        self.taille = 10

        self.maxVitesse = 5
        self.maxAcceleration = 1

    def afficher(self):
        core.Draw.circle(self.couleur,self.position,self.taille)

    def deplacement(self):
        self.acceleration = Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

        if self.acceleration.length() > self.maxAcceleration :
            self.acceleration.scale_to_length(0)

        self.vitesse = self.vitesse + self.acceleration

        self.position = self.position + self.vitesse

        # self.acceleration = Vector2

    #def bordure(self):

