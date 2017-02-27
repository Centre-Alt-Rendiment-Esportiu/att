ballColors = ((0, 255, 0), (255, 0, 0))


class Ball:
    def __init__(self, center, colorIndx):
        self.center = center
        self.color = ballColors[colorIndx]
