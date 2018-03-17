import random

class Matrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.matrix = []

        for i in range(rows):
            self.matrix.append([])
            for j in range(cols):
                self.matrix[i].append(1)

    def __str__(self):
        string = ""
        for i, col in enumerate(self.matrix):
            for num in col:
                string += "{}, ".format(num)
            string += "\n"

        return string

    def __pow__(self, val):
        result = Matrix(self.rows,self.cols)
        for i in range(val):
            result *= self
        return result

    def randomize(self):
        for i, col in enumerate(self.matrix):
            for j in range(len(col)):
                self.matrix[i][j] = random.random() * 2 - 1

    def __mul__(self, num):
        result = Matrix(self.rows, self.cols)
        if isinstance(num, Matrix):
            if(self.rows != num.rows or self.cols != num.cols):
                raise NameError("you can't multiply 2 different matrices")
            for i, col in enumerate(self.matrix):
                for j, number in enumerate(col):
                    result.matrix[i][j] = number * num.matrix[i][j]
        else:
            for i, col in enumerate(self.matrix):
                for j, number in enumerate(col):
                    result.matrix[i][j] = number * num
        return result

    def __rmul__(self, num):
        return self * num

    def __add__(self, num):
        result = Matrix(self.rows, self.cols)
        if isinstance(num, Matrix):
            if(self.rows != num.rows or self.cols != num.cols):
                raise NameError("you can't add two different matrices")
            for i, col in enumerate(self.matrix):
                for j, number in enumerate(col):
                    result.matrix[i][j] = number + num.matrix[i][j]
        else:
            for i, col in enumerate(self.matrix):
                for j, number in enumerate(col):
                    result.matrix[i][j] = number + num
        return result

    def __radd__(self, num):
        return self + num
    def __sub__(self, num):
        return self + (-num)
    def __neg__(self):
        return -1 * self

    def toArray(self):
        arr = [];
        for i, col in enumerate(self.matrix):
            for number in col:
                arr.append(number)
        return arr;

    def map(self, func):
        for i, col in enumerate(self.matrix):
            for j, number in enumerate(col):
                self.matrix[i][j] = func(number)

    @classmethod
    def multiply(cls, ma, mb):
        a = ma
        b = mb
        if(ma.cols != mb.rows):
            raise NameError("you can't multyply 2 different matrixes")
        c = cls(a.rows, b.cols)
        for i in range(a.rows):
            for j in range(b.cols):
                s = 0
                for k in range(a.cols):
                    s += a.matrix[i][k] * b.matrix[k][j]
                c.matrix[i][j] = s
        return c

    @classmethod
    def fromArray(cls, arr):
        m = cls(len(arr), 1)
        for i, number in enumerate(arr):
            m.matrix[i][0] = number
        return m

    @classmethod
    def mapMatrix(cls, m, func):
        result = cls(m.rows, m.cols)
        for i, col in enumerate(m.matrix):
            for j, number in enumerate(col):
                result.matrix[i][j] = func(number)
        return result

    @classmethod
    def transpose(cls, m):
        result = cls(m.cols, m.rows)
        for i, col in enumerate(m.matrix):
            for j, number in enumerate(col):
                result.matrix[j][i] = number
        return result
