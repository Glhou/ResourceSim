import random
import pygame as pg


class Char:
    def __init__(self, x, y, speed, race):
        self.x = x
        self.y = y
        self.speed = speed
        self.race = race
        self.inventory = {}
        self._colors = {
            "human": [(255, 204, 153), (102, 51, 0), (255, 180, 0)],
        }
        self.color = random.choice(self._colors[self.race])
        self.shapes = [pg.Rect(self.x, self.y, 10, 10),
                       pg.Rect(self.x, self.y, 10, 8)]
        self.current_shape = 0
        self.closest = None

    def get_shape(self):
        self.current_shape = (self.current_shape + 1/30) % len(self.shapes)
        return self.shapes[int(self.current_shape)]

    def find_closest_resource(self, resources):
        min_distance = float("inf")
        for resource in resources:
            distance = ((self.x - resource.x) ** 2 +
                        (self.y - resource.y) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                self.closest = resource

    def move_to_closest_resource(self, resources):
        if self.closest == None:
            self.find_closest_resource(resources)
        if self.closest:
            dx = self.closest.x - self.x
            dy = self.closest.y - self.y
            self.move(dx, dy)

    def move(self, dx, dy):
        # Normalize the vector to length of 1
        length = (dx ** 2 + dy ** 2) ** 0.5
        if length != 0:
            dx /= length
            dy /= length
        move_length = ((dx * self.speed) ** 2 + (dy * self.speed) ** 2) ** 0.5
        if move_length > length:
            self.x = self.closest.x
            self.y = self.closest.y
        else:
            self.x = self.x + dx * self.speed
            self.y = self.y + dy * self.speed

    def gather(self, resource):
        # if ressource is at 10 px of the char, gather it
        if ((self.x - resource.x) ** 2 + (self.y - resource.y) ** 2) ** 0.5 < 10:
            if resource.type not in self.inventory:
                self.inventory[resource.type] = 0
            gathered = resource.gather(10)
            if gathered == 0:
                self.closest = None
            else:
                self.speed *= 1.01
            self.inventory[resource.type] += gathered

    def survive(self):
        if "food" in self.inventory:
            self.inventory["food"] -= 1
            return True
        else:
            return False

    def __str__(self):
        return str(self.inventory)
