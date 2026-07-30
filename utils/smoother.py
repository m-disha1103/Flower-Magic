class PointSmoother:
    def __init__(self, alpha=0.22):
        self.alpha = alpha
        self.previous = None

    def update(self, point):
        if point is None:
            self.previous = None
            return None

        if self.previous is None:
            self.previous = point
            return point

        x = int(self.previous[0] + self.alpha * (point[0] - self.previous[0]))
        y = int(self.previous[1] + self.alpha * (point[1] - self.previous[1]))

        self.previous = (x, y)
        return self.previous

    def reset(self):
        self.previous = None