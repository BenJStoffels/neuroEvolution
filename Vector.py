class Vector:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

    def __add__(self, other):
        if isinstance(other, Vector):
            result = Vector(self.x + other.x,
                            self.y + other.y)
        else:
            result = Vector(self.x + other, self.y + other)

        return result

    def __mul__(self, other):
        if isinstance(other, Vector):
            result = Vector(self.x * other.x,
                            self.y * other.y)
        else:
            result = Vector(self.x * other, self.y * other)

        return result

    def __radd__(self, other):
        return self + other

    def __rmul__(self, other):
        return self * other

    def __sub__(self, other):
        return self + (-1 * other)

    def __rsub__(self, other):
        return self - other

    def __neg__(self):
        return self * -1

    def __repr__(self):
        return "Vector({}, {})".format(self.x, self.y)

    def __str__(self):
        return "{}, {}".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def copy(self):
        result = Vector(self.x, self.y)
        return result
