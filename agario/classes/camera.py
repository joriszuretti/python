import core
from classes.joueur import Joueur

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = core.WINDOW_SIZE[0]
        self.height = core.WINDOW_SIZE[1]
        self.zoom = 0.5


    def centre(self,blobOrPos):
        """S'assure que l'objet sera au centre de la vue.
        Le 'zoom' est également prit en compte
        """
        if isinstance(blobOrPos, Joueur):
            x, y = blobOrPos.x, blobOrPos.y
            self.x = (x - (x*self.zoom)) - x + (core.WINDOW_SIZE[0]/2)
            self.y = (y - (y*self.zoom)) - y + (core.WINDOW_SIZE[1]/2)
        elif type(blobOrPos) == tuple:
            self.x, self.y = blobOrPos


    def update(self, target):
        self.zoom = 100/(target.mass)+0.3
        self.centre(blob)