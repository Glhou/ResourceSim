

class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255, 255, 255)


class Resource(Object):
    def __init__(self, x, y, r_type):
        super().__init__(x, y)
        self.type = r_type
        self.quantity = 100

    def gather(self, amount):
        self.quantity -= amount
        if self.quantity <= 0:
            return 0
        return amount


class Stone(Resource):
    def __init__(self, x, y):
        super().__init__(x, y, "stone")
        self.color = (100, 100, 100)


class Wood(Resource):
    def __init__(self, x, y):
        super().__init__(x, y, "wood")
        self.color = (139, 69, 19)


class Food(Resource):
    def __init__(self, x, y):
        super().__init__(x, y, "food")
        self.color = (0, 255, 0)
