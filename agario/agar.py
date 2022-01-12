import pygame
import random
import math
import core
from classes.fenetre import Fenetre


def setup():

    f = Fenetre()
    f.defTaille(1200,700)
    f.defFps(60)
    f.defCouleur((255,255,255))
    f.set(core)

# Pygame initialization
pygame.init()
clock = pygame.time.Clock()
try:
    font = pygame.font.Font("utf-8",20)
    big_font = pygame.font.Font("utf-8",24)
except:
    font = pygame.font.SysFont('utf-8',20,True)

# Surface Definitions
MAIN_SURFACE = pygame.display.set_mode(core.WINDOW_SIZE)

# Auxiliary Functions
def drawText(message,pos,color=(255,255,255)):
    """Affiche le texte
    """
    MAIN_SURFACE.blit(font.render(message,1,color),pos)

def getDistance(a, b):
    """Calculates Euclidean distance between given points.
    """
    diffX = math.fabs(a[0]-b[0])
    diffY = math.fabs(a[1]-b[1])
    return ((diffX**2)+(diffY**2))**(0.5)

def afficher():
    Painter.afficher(core)

# Auxiliary Classes
class Painter:
    """Used to organize the drawing/ updating procedure.
    Implemantation based on Strategy Pattern.
    Note that Painter draws objects in a FIFO order.
    Objects added first, are always going to be drawn first.
    """

    def __init__(self):
        self.paintings = []

    def add(self, drawable):
        self.paintings.append(drawable)

    def paint(self):
        for drawing in self.paintings:
            drawing.draw()


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

class Drawable:
    """Used as an abstract base-class for every drawable element.
    """

    def __init__(self, surface, camera):
        self.surface = surface
        self.camera = camera

    def draw(self):
        pass

class Grille(Drawable):
    """Grille de fond d'écran
    """

    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.color = (230,240,240)

    def draw(self):
        # Grille = ensemble de lignes horizontales et prépendiculaires
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        for i in range(0,2000,5):
            pygame.draw.line(self.surface,  self.color, (x, i*zoom + y), (2000*zoom + x, i*zoom + y), 3)
            pygame.draw.line(self.surface, self.color, (i*zoom + x, y), (i*zoom + x, 2000*zoom + y), 3)

class HUD(Drawable):
    """Used to represent all necessary Head-Up Display information on screen.
    """
    
    def __init__(self, surface, camera):
        super().__init__(surface, camera)

class Joueur(Drawable):
    """Used to represent the concept of a player.
    """
    COLOR_LIST = [
    (37,7,255),
    (35,183,253),
    (48,254,241),
    (19,79,251),
    (255,7,230),
    (255,7,23),
    (6,254,13)]

    FONT_COLOR = (50, 50, 50)
    
    def __init__(self, surface, camera, name = ""):
        super().__init__(surface, camera)
        self.x = random.randint(100,400)
        self.y = random.randint(100,400)
        self.mass = 20
        self.speed = 4
        self.color = col = random.choice(Joueur.COLOR_LIST)
        self.outlineColor = (
            int(col[0]-col[0]/3),
            int(col[1]-col[1]/3),
            int(col[2]-col[2]/3))
        if name: self.name = name
        else: self.name = "Anonymous"
        self.pieces = []


    def collisionDetection(self, edibles):
        """Detects cells being inside the radius of current player.
        Those cells are eaten.
        """
        for edible in edibles:
            if(getDistance((edible.x, edible.y), (self.x,self.y)) <= self.mass/2):
                self.mass+=0.5
                edibles.remove(edible)


    def move(self):
        """Updates players current position depending on player's mouse relative position.
        """
        
        dX, dY = pygame.mouse.get_pos()
        # Find the angle from the center of the screen to the mouse in radians [-Pi, Pi]
        rotation = math.atan2(dY - float(core.WINDOW_SIZE[0])/2, dX - float(core.WINDOW_SIZE[1])/2)
        # Convert radians to degrees [-180, 180]
        rotation *= 180/math.pi
        # Normalize to [-1, 1]
        # First project the point from unit circle to X-axis
        # Then map resulting interval to [-1, 1]
        normalized = (90 - math.fabs(rotation))/90
        vx = self.speed*normalized
        vy = 0
        if rotation < 0:
            vy = -self.speed + math.fabs(vx)
        else:
            vy = self.speed - math.fabs(vx)
        tmpX = self.x + vx
        tmpY = self.y + vy
        self.x = tmpX
        self.y = tmpY

    def draw(self):
        """Draws the player as an outlined circle.
        """
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x*zoom + x), int(self.y*zoom + y))
        
        # Draw the ouline of the player as a darker, bigger circle
        pygame.draw.circle(self.surface, self.outlineColor, center, int((self.mass/2 + 3)*zoom))
        # Draw the actual player as a circle
        pygame.draw.circle(self.surface, self.color, center, int(self.mass/2*zoom))
        # Draw player's name
        fw, fh = font.size(self.name)
        drawText(self.name, (self.x*zoom + x - int(fw/2), self.y*zoom + y - int(fh/2)),
                 Joueur.FONT_COLOR)

class Cell(Drawable): # Semantically, this is a parent class of player

    """Représenter cellules
    """

    CELL_COLORS = [
    (80,252,54),
    (36,244,255),
    (243,31,46),
    (4,39,243),
    (254,6,178),
    (255,211,7),
    (216,6,254),
    (145,255,7),
    (7,255,182),
    (255,6,86),
    (147,7,255)]
    
    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.x = random.randint(20,1980)
        self.y = random.randint(20,1980)
        self.mass = 7
        self.color = random.choice(Cell.CELL_COLORS)

    def draw(self):
        """Dessine une cellule.
        """
        zoom = self.camera.zoom
        x,y = self.camera.x, self.camera.y
        center = (int(self.x*zoom + x), int(self.y*zoom + y))
        pygame.draw.circle(self.surface, self.color, center, int(self.mass*zoom))
        
class CellList(Drawable):
    """Regrouper et organiser les cellules.
    Garde également une trace des cellules vivantes/mortes
    """

    def __init__(self, surface, camera, numOfCells):
        super().__init__(surface, camera)
        self.count = numOfCells
        self.list = []
        for i in range(self.count): self.list.append(Cell(self.surface, self.camera))

    def draw(self):
        for cell in self.list:
            cell.draw()

    

# Initialize essential entities
C = Camera()

Grille = Grille(MAIN_SURFACE, C)
cells = CellList(MAIN_SURFACE, C, 2000)
'Nom du joueur'
blob = Joueur(MAIN_SURFACE, C, "Joris")
hud = HUD(MAIN_SURFACE, C)

P = Painter()

P.add(Grille)
P.add(cells)
P.add(blob)
P.add(hud)

# BOUCLE JEU PRINCIPAL
while(True):
    
    clock.tick(70)
    
    for e in pygame.event.get():
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            if(e.key == pygame.K_SPACE):
                del(C)
                blob.split()
            if(e.key == pygame.K_w):
                blob.feed()
        if(e.type == pygame.QUIT):
            pygame.quit()
            quit()

    blob.move()
    blob.collisionDetection(cells.list)
    C.update(blob)
    MAIN_SURFACE.fill((242,251,255))
    P.paint()
    # Start calculating next frame
    pygame.display.flip()
