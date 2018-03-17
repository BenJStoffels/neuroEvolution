import pygame
import random
from Vector import Vector
from NeuralNetwork import NeuralNetwork as NN

pygame.init()


class SnakeGame:
    def __init__(self, window=False):

        self.length = 0
        self.history = []
        self.lastMove = None
        self.brain = NN([24, 20, 5, 4])
        self.isDead = False
        self.speed = 20
        self.rows = 50
        self.cols = 50
        self.width = self.rows * self.speed
        self.height = self.rows * self.speed
        self.pos = Vector(self.speed * self.cols / 2, self.speed * self.rows / 2)
        self.food = Vector(500, random.randrange(0, self.height, self.speed))
        self.window = False

        if window:
            self.window = True
            self.display_screen = pygame.display.set_mode(
                (self.width, self.height))
            pygame.display.set_caption("Snake game")
            self.clock = pygame.time.Clock()

    def updateHistory(self):
        if self.length != 0:
            if self.length == len(self.history):
                newHis = []
                for i in range(len(self.history) - 1):
                    newHis.append(self.history[i + 1].copy())
                newHis.append(self.pos.copy())
            else:
                newHis = self.history
                newHis.append(self.pos.copy())
            self.history = newHis

    def move(self, dir):
        if dir == "Up":
            if self.lastMove != "Down":
                self.pos.y += self.speed
                self.lastMove = "Up"
            else:
                self.pos.y -= self.speed
                self.lastMove = "Down"
        elif dir == "Down":
            if self.lastMove != "Up":
                self.pos.y -= self.speed
                self.lastMove = "Down"
            else:
                self.pos.y += self.speed
                self.lastMove = "Up"
        elif dir == "Right":
            if self.lastMove != "Left":
                self.pos.x += self.speed
                self.lastMove = "Right"
            else:
                self.pos.x -= self.speed
                self.lastMove = "Left"
        elif dir == "Left":
            if self.lastMove != "Right":
                self.pos.x -= self.speed
                self.lastMove = "Left"
            else:
                self.pos.x += self.speed
                self.lastMove = "Right"
        else:
            if self.lastMove == None:
                self.pos.x += self.speed
                self.lastMove = "Right"
            else:
                self.move(self.lastMove)

    def eats(self):
        return self.pos == self.food

    def hitsWal(self):
        return self.pos.x < 0 or self.pos.x >= self.width or self.pos.y < 0 or self.pos.y >= self.height

    def hitsSnake(self):
        hitting = False
        for v in self.history:
            if self.pos == v:
                hitting = True
                break
        return hitting

    def calculateVision(self):
        vision = []
        tempValues = self.lookInDirection(Vector(-self.speed, 0))
        for num in tempValues:
            vision.append(num)
        tempValues = self.lookInDirection(Vector(-self.speed, -self.speed))
        for num in tempValues:
            vision.append(num)
        tempValues = self.lookInDirection(Vector(0, -self.speed))
        for num in tempValues:
            vision.append(num)
        tempValues = self.lookInDirection(Vector(self.speed, -self.speed))
        for num in tempValues:
            vision.append(num)
        tempValues = self.lookInDirection(Vector(self.speed, 0))
        for num in tempValues:
            vision.append(num)
        tempValues = self.lookInDirection(Vector(self.speed, self.speed))
        for num in tempValues:
            vision.append(num)
        tempValues = self.lookInDirection(Vector(0, self.speed))
        for num in tempValues:
            vision.append(num)
        tempValues = self.lookInDirection(Vector(-self.speed, self.speed))
        for num in tempValues:
            vision.append(num)
        return vision

    def lookInDirection(self, vector):
        visionInDirection = [0, 0, 0]

        position = self.pos.copy()

        foodIsFound = False
        tailIsFound = False

        distance = 0

        position += vector
        distance += 1

        while position.x > 0 and position.y > 0 and position.x <= self.width and position.y <= self.height:
            if not foodIsFound and position == self.food:
                visionInDirection[0] = 1
                foodIsFound = True
            if not tailIsFound:
                for v in self.history:
                    if position == v:
                        tailIsFound = True
                        visionInDirection[1] = 1 / distance

            position += vector
            distance += 1

        visionInDirection[2] = 1 / distance

        return visionInDirection

    def guess(self, vision):
        output_matrix = self.brain.feedforward(vision)
        outputs = output_matrix.toArray()
        guessIndex = outputs.index(max(outputs))
        return ["Up", "Down", "Left", "Right"][guessIndex]

    def update(self):
        self.updateHistory()
        vision = self.calculateVision()
        choice = self.guess(vision)
        print(vision)
        print(choice)
        if choice != None:
            self.move(choice)
        else:
            self.move(self.lastMove)
        if self.hitsWal() or self.hitsSnake():
            print("died ", self.length, " ", self.pos)
            self.isDead = True
        if self.eats():
            self.length += 1
            self.food = Vector(random.randrange(0, self.width, self.speed), random.randrange(0, self.height, self.speed))

    def run(self):
        self.update()

    def getKeyInput(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    return "Left"
                if event.key == pygame.K_RIGHT:
                    return "Right"
                if event.key == pygame.K_UP:
                    return "Down"
                if event.key == pygame.K_DOWN:
                    return "Up"
        return None

    def show(self):
        self.display_screen.fill((0, 0, 0))
        pygame.draw.rect(self.display_screen, (255, 255, 255), [self.pos.x, self.pos.y, self.speed, self.speed])
        for v in self.history:
            pygame.draw.rect(self.display_screen, (255, 255, 255), [v.x, v.y, self.speed, self.speed])
        pygame.draw.rect(self.display_screen, (255, 0, 100), [self.food.x, self.food.y, self.speed, self.speed])
        pygame.display.update()
        self.clock.tick(5)


sg = SnakeGame(True)


while not sg.isDead:
    sg.run()
    if sg.window:
        sg.show()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sg.isDead = True
                break

pygame.quit()
quit()
