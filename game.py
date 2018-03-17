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
        # self.brain = NN([24, 20, 5, 4])
        self.isDead = False
        self.speed = 20
        self.rows = 50
        self.cols = 50
        self.width = self.rows * self.speed
        self.height = self.rows * self.speed
        self.pos = Vector(self.speed * self.cols / 2, self.speed * self.rows / 2)
        self.food = Vector(random.randrange(0, self.width, self.speed), random.randrange(0, self.height, self.speed))
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

    def update(self):
        self.updateHistory()
        choice = self.getKeyInput()
        if choice != None:
            self.move(choice)
        else:
            self.move(self.lastMove)
        if self.hitsWal() or self.hitsSnake():
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
        sg.clock.tick(5)


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
