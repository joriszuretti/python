class Fenetre:
    def  __init__(self):
        self.hauteur = 1200
        self.largeur = 700
        self.fps = 0
        self.couleur = (0,0,0)

    def set(self, core):
        core.bgColor = self.couleur
        core.WINDOW_SIZE = [self.hauteur, self.largeur]
        core.fps = self.fps

    def defHauteur(self, h):
        self.hauteur = h
    def defLargeur(self, l):
        self.hauteur = l
    def defFps(self, f):
        self.fps = f
    def defCouleur(self, c):
        self.couleur = c
    def defTaille(self, h,l):
        self.hauteur=h
        self.largeur=l
    def hauteur(self):
        return self.hauteur()
    def largeur(self):
        return self.largeur()
    def couleur(self):
        return self.couleur
    def fps(self):
        return self.fps