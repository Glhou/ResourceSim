import random
import pygame as pg


class Char:
    def __init__(self, x, y, cha, intl,  speed, race):
        self.x = x
        self.y = y
        self.speed = speed
        self.race = race
        self.inventory = {"food": 100}
        self.cha = cha  # charsima
        self.fil = 100  # feeling
        self.intl = intl  # intelligence
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
        priority_type = None
        if self.intl > 0.5 and self.inventory.get("food", 0) < 10:
            # prioritize food if food is lower than 10
            priority_type = "food"
        min_distance = float("inf")
        for resource in resources:
            distance = ((self.x - resource.x) ** 2 +
                        (self.y - resource.y) ** 2) ** 0.5
            if self.closest:
                closest_type = self.closest.type
            else:
                closest_type = ""
            if (distance < min_distance or (resource.type == priority_type)) and not (closest_type == priority_type):
                min_distance = distance
                if (self.intl < 0.6):
                    # just dumb and sometimes don't see every resources
                    skip = random.randint(0, 1)
                    if skip > 0.2:
                        self.closest = resource
                else:
                    self.closest = resource

    def move_to_closest_resource(self, resources):
        if self.closest == None or self.closest not in resources:
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
            self.inventory["food"] -= 0.1
            self.speed -= 0.001
        if self.speed < 0.1 and self.inventory["food"] > 0.1:
            self.inventory["food"] -= 0.1
            self.speed = 2
        move_length = ((dx * self.speed) ** 2 + (dy * self.speed) ** 2) ** 0.5
        if move_length > length:
            self.x = self.closest.x
            self.y = self.closest.y
        else:
            self.x = self.x + dx * self.speed
            self.y = self.y + dy * self.speed

    def gather(self, resource):
        # if ressource is at 10 px of the char, gather it
        if resource:
            if ((self.x - resource.x) ** 2 + (self.y - resource.y) ** 2) ** 0.5 < 10:
                if resource.type not in self.inventory:
                    self.inventory[resource.type] = 0
                gathered = resource.gather(10)
                if gathered == 0:
                    self.closest = None
                else:
                    self.speed *= 1.001
                self.inventory[resource.type] += gathered

    def survive(self):
        if "food" in self.inventory and self.inventory["food"] > 0:
            return True
        else:
            return False

    def __str__(self):
        return str(self.inventory)
