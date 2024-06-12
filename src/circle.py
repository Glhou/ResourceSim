from char import Char


class Circle:
    # a Circle is a group of Char with a leader
    def __init__(self, leader):
        self.leader = leader
        self.chars = [leader]

    def add_char(self, char):
        char.circle = self
        self.chars.append(char)
