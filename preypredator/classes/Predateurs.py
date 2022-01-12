from pygame.math import Vector2
import core
import random

class Predateur:
    def __init__(self):
        #self.position = Vector2(0,0)
        self.position = Vector2(random.randint(0,400),random.randint(0,400))
        self.vitesse = Vector2(0,0)
        self.acceleration = Vector2(0,0)
        self.vivante = True

        self.couleur = (0,255,0)
        self.taille = 10

        self.maxVitesse = 5
        self.maxAcceleration = 1

        self.vision = 100

    def afficher(self):
        core.Draw.circle(self.couleur,self.position,self.taille)

    def deplacement(self,proies):
        proiesDansVision=[]
        cible = None
        distanceCible = 100

        for p in proies:
            if p.position.distance_to(self.position) < self.vision:
                proiesDansVision.append(p)
                if p.position.distance_to(self.position) < distanceCible:
                    cible = p
                    distanceCible = p.position.distance_to(self.position)

        if cible is not None:
            force = cible.position - self.position
            self.acceleration = force

            if self.acceleration.length() > self.maxAcceleration:
                self.acceleration.scale_to_length()

            self.vitesse = self.vitesse + self.acceleration

        if self.vitesse.length() > self.maxVitesse :
            self.vitesse.scale_to_length(self.maxVitesse)

        self.position = self.position + self.vitesse