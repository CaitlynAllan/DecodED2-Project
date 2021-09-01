from pygame.locals import K_RIGHT, K_SPACE, K_LEFT, KEYDOWN, KEYUP
from pygame import Color, Vector2
from src.constants import BLACK, WHITE

class Game:

    entities: "list"

    def __init__(self):
        self.entities = []

    def handle_input(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    print("Move Left")
                if event.key == K_RIGHT:
                    print("Move Right")
                if event.key == K_SPACE:
                    print("Shoot Bullet")
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    print("Stop Moving Left")
                if event.key == K_RIGHT:
                    print("Stop Moving Right")


    def update(self, delta):
        for i in range(len(self.entities) - 1, -1, -1):
            obj = self.entities[i]
            # Execite entity logic
    
    def render_text(self, display, font, text: str, colour: Color, position: Vector2):
        surface = font.render(text, True, colour)
        display.blit(surface, position)

    def render(self, display, font):
        display.fill(BLACK)
        # loop through entity list and render it
        self.render_text(display, font, "Space Invaders", WHITE, (50, 50))