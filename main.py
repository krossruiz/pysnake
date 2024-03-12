import pygame
import numpy as np
from enum import Enum
from collections import deque

#when working with python files, remember to use "conda init powershell"
#in the terminal to enable Intellisense

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
 
# initialize pygame
pygame.init()
#MUST be same number twice, aka a square
SCREEN_SIZE = (500, 500)
#MUST be same number twice, aka a square
PLAY_GRID_SIZE = (20,20)

PLAY_SQUARE_WIDTH = int(SCREEN_SIZE[0] / PLAY_GRID_SIZE[0])
SNAKE_INIT_CELL_COUNT = 4

class Directions(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

SNAKE_INIT_DIRECTION = Directions.LEFT

# create a window
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("pygame Test")

def gridPosAfterMove(direction, startCellIndicies):
    if direction == Directions.UP:
        return (startCellIndicies[0], startCellIndicies[1] - 1)
    if direction == Directions.DOWN:
        return (startCellIndicies[0], startCellIndicies[1] + 1)
    if direction == Directions.LEFT:
        return (startCellIndicies[0] - 1, startCellIndicies[1])
    if direction == Directions.RIGHT:
        return (startCellIndicies[0] + 1, startCellIndicies[1])

def gridIndiciesInBounds(indicies):
    if (indicies[0] > -1 \
        and indicies[0] < PLAY_GRID_SIZE[0] \
        and indicies[1] > -1 \
        and indicies[1] < PLAY_GRID_SIZE[1]):
        return True
    else:
        return False

class Snake:
    def __init__(self, bodyCellCount):
        self.active = True
        self.initBodyCellCount = bodyCellCount
        self.headDirection = SNAKE_INIT_DIRECTION
        self.nextHeadDirection = SNAKE_INIT_DIRECTION
        self.bodyCellQueue = deque()
        self.initSnakeBody(bodyCellCount)

    def reset(self):
        self.headDirection = SNAKE_INIT_DIRECTION
        self.nextHeadDirection = SNAKE_INIT_DIRECTION
        self.bodyCellQueue.clear()
        self.initSnakeBody(self.initBodyCellCount)
        self.active = True

    def trySetHeadDirection(self, tryDirection):
        if self.headDirection == Directions.UP and tryDirection == Directions.DOWN:
            return
        if self.headDirection == Directions.DOWN and tryDirection == Directions.UP:
            return
        if self.headDirection == Directions.LEFT and tryDirection == Directions.RIGHT:
            return
        if self.headDirection == Directions.RIGHT and tryDirection == Directions.LEFT:
            return   
        self.nextHeadDirection = tryDirection

    def getHeadIndicies(self):
        return self.bodyCellQueue[len(self.bodyCellQueue) - 1].getGridCellIndicies()
    
    def isHeadIntersectingBody(self):
        headIndicies = self.getHeadIndicies()
        for cellIndex in range(len(self.bodyCellQueue)-1):
            if headIndicies == self.bodyCellQueue[cellIndex].getGridCellIndicies():
                return True
        return False


    def getBodyCellQueue(self):
        return self.bodyCellQueue
    
    def getBodyCellIndicies(self):
        bodyCellIndicies = []
        for cellIndex in range(len(self.bodyCellQueue)):
            bodyCellIndicies.append(\
                self.bodyCellQueue[cellIndex].getGridCellIndicies()\
            )
        return bodyCellIndicies
    
    def initSnakeBody(self, bodyCellCount):
        midGridCellIndicies = (int(PLAY_GRID_SIZE[0] / 2), int(PLAY_GRID_SIZE[1] / 2))
        for cellIndex in range(bodyCellCount):
            self.bodyCellQueue.append(SnakeBodyCell((midGridCellIndicies[0], midGridCellIndicies[1] + cellIndex)))
    def advanceSnake(self, incrementLength):
        self.headDirection = self.nextHeadDirection
        if self.active == False:
            return
        snakeHeadIndicies = self.bodyCellQueue[len(self.bodyCellQueue)-1].getGridCellIndicies()
        newSnakeHeadIndicies = gridPosAfterMove(self.headDirection, snakeHeadIndicies)

        if snake.isHeadIntersectingBody():
            print("Snake Collided with self and is now inactive.")
            self.active = False
            return

        if incrementLength:
            if (gridIndiciesInBounds(newSnakeHeadIndicies)):
                self.bodyCellQueue.append(SnakeBodyCell(newSnakeHeadIndicies))
        else:
            if (gridIndiciesInBounds(newSnakeHeadIndicies)):
                self.bodyCellQueue.popleft()
                self.bodyCellQueue.append(SnakeBodyCell(newSnakeHeadIndicies))
            else:
                print("Snake Collided with grid bounds and is now inactive.")
                self.active = False

class SnakeBodyCell:

    def __init__(self, gridCellIndicies):
        self.gridCellIndicies = gridCellIndicies
    def getGridCellIndicies(self):
        return self.gridCellIndicies
    def draw(self):
        pygame.draw.rect(screen, BLACK, \
                         pygame.Rect(PLAY_SQUARE_WIDTH * self.gridCellIndicies[0], \
                                    PLAY_SQUARE_WIDTH * self.gridCellIndicies[1], \
                                    PLAY_SQUARE_WIDTH, PLAY_SQUARE_WIDTH))

class RewardCell:
    def __init__(self):
        pass
    def getGridCellIndicies(self):
        return self.gridCellIndicies
    def setRandomGridIndicies(self, excludeIndicies):
        print("rewardCell setRandomIndicies() called")
        # Convert the exclude_list to a set for faster lookup
        excludeSet = set(excludeIndicies)
        while True:
            # Generate a random index
            i = np.random.randint(PLAY_GRID_SIZE[0])
            j = np.random.randint(PLAY_GRID_SIZE[1])

            # If the index is not in the exclude set, return it
            if (i, j) not in excludeIndicies:
                self.gridCellIndicies = (i, j)
                return

    def draw(self):
        pygame.draw.rect(screen, RED, \
                        pygame.Rect(PLAY_SQUARE_WIDTH * self.gridCellIndicies[0], \
                                    PLAY_SQUARE_WIDTH * self.gridCellIndicies[1], \
                                    PLAY_SQUARE_WIDTH, PLAY_SQUARE_WIDTH)
                        )


snake = Snake(SNAKE_INIT_CELL_COUNT)
rewardCell = RewardCell()
rewardCell.setRandomGridIndicies(snake.getBodyCellIndicies())
clock = pygame.time.Clock()
gameSpeedCounter = 0
gameSpeedTime = 100

def resetGame():
    print("Game reset.")
    snake.reset()
    rewardCell.setRandomGridIndicies(snake.getBodyCellIndicies())
    global gameSpeedCounter
    gameSpeedCounter = 0

# clock is used to set a max fps


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                resetGame()
            if event.key == pygame.K_LEFT:
                print("LEFT DOWN")
                snake.trySetHeadDirection(Directions.LEFT)
            if event.key == pygame.K_RIGHT:
                print("RIGHT DOWN")
                snake.trySetHeadDirection(Directions.RIGHT)
            if event.key == pygame.K_UP:
                print("UP DOWN")
                snake.trySetHeadDirection(Directions.UP)
            if event.key == pygame.K_DOWN:
                print("DOWN DOWN")
                snake.trySetHeadDirection(Directions.DOWN)

    #clear the screen
    screen.fill(WHITE)

    # draw to the screen
    # YOUR CODE HERE]
    rewardCell.draw()
    for bodyCell in snake.getBodyCellQueue():
        bodyCell.draw()
    gameSpeedCounter += clock.get_time()
    if gameSpeedCounter > gameSpeedTime:
        # print(str(gameSpeedTime) + "ms")
        incrementLength = False
        snakeHeadIndicies = snake.getHeadIndicies()
        rewardCellIndicies = rewardCell.getGridCellIndicies()
        if  rewardCellIndicies == snakeHeadIndicies:
            incrementLength = True
            rewardCell.setRandomGridIndicies(snake.getBodyCellIndicies())
        snake.advanceSnake(incrementLength)
        gameSpeedCounter = 0
 
    # flip() updates the screen to make our changes visible
    pygame.display.flip()
     
    # how many updates per second
    clock.tick(60)
 
pygame.quit()