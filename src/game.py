import pygame as pg
import random
from .objects import Stone, Wood, Food
from .char import Char
# Path: src/game.py


class Game:
    def __init__(self):
        pg.init()
        self.size = (800, 600)
        self.screen = pg.display.set_mode(self.size)
        self.transparent_surface = pg.Surface(self.size, pg.SRCALPHA)
        self.transparent_surface.fill((0, 0, 0, 0))
        pg.display.set_caption("My Game")
        self.clock = pg.time.Clock()
        self.running = True
        self.resources_types = ["stone", "wood", "food"]
        self.resources_nb = 10
        self.resources = self.generate_resources(
            self.resources_nb)
        self.chars = self.generate_chars(5)

    def generate_resources(self, quantity):
        resources = []
        for _ in range(quantity):
            x = random.randint(0, self.size[0])
            y = random.randint(0, self.size[1])
            # type is random
            r_type = random.choices(
                self.resources_types, weights=[0.1, 0.2, 0.7], k=1)[0]
            if r_type == "stone":
                resources.append(Stone(x, y))
            elif r_type == "wood":
                resources.append(Wood(x, y))
            elif r_type == "food":
                resources.append(Food(x, y))
        return resources

    def generate_chars(self, quantity):
        chars = []
        for _ in range(quantity):
            x = random.randint(0, self.size[0])
            y = random.randint(0, self.size[1])
            speed = random.randint(50, 100)/100
            cha = random.randint(0, 100) / 100
            intl = random.randint(0, 100) / 100
            chars.append(Char(x, y, cha, intl, speed, "human"))
        return chars

    def display(self):
        # display all resources with their .color attribute
        for resource in self.resources:
            pg.draw.rect(self.screen, resource.color,
                         pg.Rect(resource.x, resource.y, 10, 10))
        # display all chars with their .color attribute
        for char in self.chars:
            shape = char.get_shape()
            shape.bottomright = (char.x + 10, char.y + 10)
            pg.draw.rect(self.screen, char.color, shape)

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.transparent_surface, (0, 0))
            self.display()
            for char in self.chars:
                char.move_to_closest_resource(self.resources)
                char.gather(char.closest)
                if char.survive() == False:
                    self.chars.remove(char)
            for resource in self.resources:
                if resource.quantity <= 0:
                    self.resources.remove(resource)
            if len(self.resources) < self.resources_nb / 2:
                new_resources = self.generate_resources(
                    self.resources_nb - len(self.resources))
                self.resources.extend(new_resources)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            pg.display.flip()

        pg.quit()
