import pygame
import core
from pygame.math import Vector2


class Joueur(Drawable):
    """Used to represent the concept of a player.
    """
    COLOR_LIST = [
        (37, 7, 255),
        (35, 183, 253),
        (48, 254, 241),
        (19, 79, 251),
        (255, 7, 230),
        (255, 7, 23),
        (6, 254, 13)]

    FONT_COLOR = (50, 50, 50)

    def __init__(self, surface, camera, name=""):
        super().__init__(surface, camera)
        self.x = random.randint(100, 400)
        self.y = random.randint(100, 400)
        self.mass = 20
        self.speed = 4
        self.color = col = random.choice(Joueur.COLOR_LIST)
        self.outlineColor = (
            int(col[0] - col[0] / 3),
            int(col[1] - col[1] / 3),
            int(col[2] - col[2] / 3))
        if name:
            self.name = name
        else:
            self.name = "Anonymous"
        self.pieces = []

    def collisionDetection(self, edibles):
        """Detects cells being inside the radius of current player.
        Those cells are eaten.
        """
        for edible in edibles:
            if (getDistance((edible.x, edible.y), (self.x, self.y)) <= self.mass / 2):
                self.mass += 0.5
                edibles.remove(edible)

    def move(self):
        """Updates players current position depending on player's mouse relative position.
        """

        dX, dY = pygame.mouse.get_pos()
        # Find the angle from the center of the screen to the mouse in radians [-Pi, Pi]
        rotation = math.atan2(dY - float(core.WINDOW_SIZE[0]) / 2, dX - float(core.WINDOW_SIZE[1]) / 2)
        # Convert radians to degrees [-180, 180]
        rotation *= 180 / math.pi
        # Normalize to [-1, 1]
        # First project the point from unit circle to X-axis
        # Then map resulting interval to [-1, 1]
        normalized = (90 - math.fabs(rotation)) / 90
        vx = self.speed * normalized
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
        center = (int(self.x * zoom + x), int(self.y * zoom + y))

        # Draw the ouline of the player as a darker, bigger circle
        pygame.draw.circle(self.surface, self.outlineColor, center, int((self.mass / 2 + 3) * zoom))
        # Draw the actual player as a circle
        pygame.draw.circle(self.surface, self.color, center, int(self.mass / 2 * zoom))
        # Draw player's name
        fw, fh = font.size(self.name)
        drawText(self.name, (self.x * zoom + x - int(fw / 2), self.y * zoom + y - int(fh / 2)),
                 Joueur.FONT_COLOR)

