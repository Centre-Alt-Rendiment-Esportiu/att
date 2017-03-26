class Player(object):
    def __init__(self):
        self.score = 0

    def add_score(self):
        self.score += 1

    def reset_score(self):
        self.score = 0
