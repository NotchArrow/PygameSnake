import random
from enum import Enum

import pygame


class Direction(Enum):
    NORTH = pygame.Vector2(0, -1)
    EAST = pygame.Vector2(1, 0)
    SOUTH = pygame.Vector2(0, 1)
    WEST = pygame.Vector2(-1, 0)


class Snake:
    def __init__(self, position, direction, length, keys, color):
        self.positions = [position]
        self.direction = direction
        self.old_direction = direction
        self.length = length
        self.keys = keys  # [up, down, left, right]
        self.color = color
        self.dt = 0  # iterable for movement
        self.speed = 8  # move every x frames
        self.alive = True

    def takeInput(self, key):
        if key == self.keys[0] and self.direction != Direction.SOUTH:
            self.direction = Direction.NORTH
        elif key == self.keys[1] and self.direction != Direction.NORTH:
            self.direction = Direction.SOUTH
        elif key == self.keys[2] and self.direction != Direction.EAST:
            self.direction = Direction.WEST
        elif key == self.keys[3] and self.direction != Direction.WEST:
            self.direction = Direction.EAST

    def updatePos(self, game):
        if self.alive:
            if self.dt % self.speed == 0 or self.direction != self.old_direction:
                self.dt = 0

                self.positions.insert(0, self.positions[0].copy())
                self.positions[0] += self.direction.value * game.GRID

                self.positions[0] = pygame.Vector2(self.positions[0].x % game.SCREEN_SIZE[0],
                                                   self.positions[0].y % game.SCREEN_SIZE[1])
                self.positions = self.positions[0:self.length]

            self.old_direction = self.direction
            self.dt += 1

    def checkCollisions(self, game):
        headPos = self.positions[0]

        if headPos in self.positions[1:]:
            self.alive = False

        for snake in game.snakes:
            if snake != self and headPos in snake.positions:
                self.alive = False
                snake.length += self.length

        for apple in game.apples:
            if apple.position == self.positions[0]:
                if apple.golden:
                    self.length += 5
                    game.score += 5
                    if self.speed > 1:
                        self.speed -= 1
                else:
                    self.length += 1
                    game.score += 1
                apple.move(game)

    def draw(self, game):
        for seg, pos in enumerate(self.positions):
            gradient = 50 * seg ** .5
            segColor = (max(self.color[0] * .5, self.color[0] - gradient),
                        max(self.color[1] * .5, self.color[1] - gradient),
                        max(self.color[2] * .5, self.color[2] - gradient))

            pygame.draw.rect(game.screen, segColor, pygame.Rect(pos.x, pos.y, game.GRID, game.GRID))


class Apple:
    def __init__(self, game):
        self.position = pygame.Vector2(random.randrange(game.SCREEN_WIDTH) * game.GRID,
                                       random.randrange(game.SCREEN_HEIGHT) * game.GRID)
        self.shrink = 0.8
        self.golden = False
        self.goldenChance = .1

    def move(self, game):
        validLocation = False
        while not validLocation:
            self.position = pygame.Vector2(random.randrange(game.SCREEN_WIDTH) * game.GRID, random.randrange(game.SCREEN_HEIGHT) * game.GRID)
            validLocation = True
            for snake in game.snakes:
                if self.position in snake.positions:
                    validLocation = False

        self.golden = random.random() < self.goldenChance

    def delGolden(self, game):
        if self.golden:
            pos = self.position
            positions = []
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x != 0 or y != 0:
                        positions.append(pygame.Vector2(
                            (pos.x + x * game.GRID) % game.SCREEN_SIZE[0],
                            (pos.y + y * game.GRID) % game.SCREEN_SIZE[1]))

            filled = 0
            snakeBonus = []
            for position in positions:
                for snake in game.snakes:
                    if position in snake.positions:
                        filled += 1
                        snakeBonus.append(snake)
                        break
            if filled >= 7:
                for snake in snakeBonus:
                    snake.length += 1
                self.move(game)

    def draw(self, game):
        size = game.GRID * self.shrink
        offset = (game.GRID - size) / 2

        if self.golden:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)

        pygame.draw.rect(game.screen, color, pygame.Rect(self.position.x + offset, self.position.y + offset, size, size))


class SnakeGame:
    def __init__(self, GRID, SCREEN_WIDTH, SCREEN_HEIGHT, appleCount, snakeCount, snakeData):
        pygame.init()
        self.GRID = GRID
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SCREEN_SIZE = (self.SCREEN_WIDTH * self.GRID, self.SCREEN_HEIGHT * self.GRID)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)

        self.appleCount = appleCount
        self.apples = []
        self.snakeCount = snakeCount
        self.snakes = []
        self.snakeData = snakeData
        self.score = 0

    def run(self):
        clock = pygame.time.Clock()
        running = True

        for i, data in enumerate(self.snakeData):
            if i < self.snakeCount:
                if i % 2 == 0:
                    direction = Direction.EAST
                else:
                    direction = Direction.WEST
                self.snakes.append(Snake(pygame.Vector2(self.GRID * i, self.GRID * i), direction, 3,
                                         data[0], data[1]))
        for i in range(self.appleCount):
            self.apples.append(Apple(self))

        while running:
            self.screen.fill((0, 0, 0))
            pygame.display.set_caption(f"Snake | Score: {self.score}")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    for snake in self.snakes:
                        snake.takeInput(event.key)

            for snake in self.snakes:
                snake.updatePos(self)

            for snake in self.snakes:
                snake.checkCollisions(self)

            for snake in self.snakes:
                if not snake.alive:
                    self.snakes.remove(snake)

            for snake in self.snakes:
                snake.draw(self)

            for apple in self.apples:
                apple.delGolden(self)
                apple.draw(self)

            if len(self.snakes) == 0:
                running = False

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


snakeGame = SnakeGame(
    30, 24, 24,
    1, 1,

    [([pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d], (0, 255, 0)),
     ([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], (200, 200, 0)),
     ([pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l], (200, 0, 200)),
     ([pygame.K_t, pygame.K_g, pygame.K_f, pygame.K_h], (200, 200, 200))]
)
snakeGame.run()
