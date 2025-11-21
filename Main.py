import pygame
import random
import time
from enum import Enum

class Direction (Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class Snake:
    def __init__(self, position, direction, length, keys, color):
        self.position = position
        self.positions = []
        self.direction = direction
        self.old_direction = direction
        self.length = length
        self.keys = keys # [up, down, left, right]
        self.color = color
        self.dt = 0 # iterable for movement
        self.speed = 8 # move every x frames
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

    def tick(self, snakes, apples):
        if self.alive:
            if self.dt % self.speed == 0 or self.direction != self.old_direction:
                self.dt = 0
                if self.direction == Direction.NORTH:
                    self.position += pygame.Vector2(0, -GRID)
                elif self.direction == Direction.EAST:
                    self.position += pygame.Vector2(GRID, 0)
                elif self.direction == Direction.SOUTH:
                    self.position += pygame.Vector2(0, GRID)
                elif self.direction == Direction.WEST:
                    self.position += pygame.Vector2(-GRID, 0)

                self.position = pygame.Vector2(self.position.x % (SCREEN_WIDTH * GRID), self.position.y % (SCREEN_HEIGHT * GRID))

                for snake in snakes:
                    if self.position in snake.positions:
                        snakes.remove(self)
                        self.alive = False

                for apple in apples:
                    if apple.position == self.position:
                        self.length += 1
                        apple.move(snakes)

                self.positions.insert(0, pygame.Vector2(int(self.position.x) % (SCREEN_WIDTH * GRID), int(self.position.y) % (SCREEN_HEIGHT * GRID)))
                self.positions = self.positions[0:self.length]

            for seg, pos in enumerate(self.positions):
                gradient = 50 * seg ** .5
                segColor = (max(self.color[0] * .5, self.color[0] - gradient),
                            max(self.color[1] * .5, self.color[1] - gradient),
                            max(self.color[2] * .5, self.color[2] - gradient))
                pygame.draw.rect(screen, segColor, pygame.Rect(pos.x, pos.y, GRID, GRID))

            self.old_direction = self.direction
            self.dt += 1

class Apple:
    def __init__(self):
        self.position = pygame.Vector2(random.randrange(SCREEN_WIDTH) * GRID, random.randrange(SCREEN_HEIGHT) * GRID)
        self.shrink = 0.8

    def move(self, snakes):
        validLocation = False
        while not validLocation:
            self.position = pygame.Vector2(random.randrange(SCREEN_WIDTH) * GRID, random.randrange(SCREEN_HEIGHT) * GRID)
            validLocation = True
            for snake in snakes:
                if self.position in snake.positions:
                    validLocation = False

    def draw(self):
        size = GRID * self.shrink
        offset = (GRID - size) / 2
        pygame.draw.rect(screen, "red", pygame.Rect(self.position.x + offset, self.position.y + offset, size, size))

class SnakeGame:
    def __init__(self, appleCount, snakeCount, snakeData):
        self.appleCount = appleCount
        self.snakeCount = snakeCount
        self.snakeData = snakeData

    def run(self):
        global running
        clock = pygame.time.Clock()
        running = True

        snakes = []
        for i, data in enumerate(self.snakeData):
            if i < self.snakeCount:
                snakes.append(Snake(pygame.Vector2(GRID * i, GRID * i), Direction.EAST, 3,
                    data[0], data[1]))
        apples = []
        for i in range(self.appleCount):
            apples.append(Apple())

        while running:
            screen.fill((0, 0, 0))
            pygame.display.set_caption("Snake")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    for snake in snakes:
                        snake.takeInput(event.key)

            for snake in snakes:
                snake.tick(snakes, apples)
            for apple in apples:
                apple.draw()

            if len(snakes) == 0:
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            waiting = False
                break

            pygame.display.flip()
            clock.tick(60)

pygame.init()
GRID = 50
SCREEN_WIDTH = 16
SCREEN_HEIGHT = 16
SCREEN_SIZE = (SCREEN_WIDTH * GRID, SCREEN_HEIGHT * GRID)
screen = pygame.display.set_mode(SCREEN_SIZE)
running = True

while running:
    screen.fill((40, 40, 40))
    CLOCK = pygame.time.Clock()

    for EVENT in pygame.event.get():
        if EVENT.type == pygame.QUIT:
            running = False
        if EVENT.type == pygame.MOUSEBUTTONDOWN:
            game = SnakeGame(1, 3,
                    [([pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d], (0, 255, 0)),
                     ([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], (200, 200, 0)),
                     ([pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l], (200, 0, 200))])
            game.run()

    pygame.display.flip()
    CLOCK.tick(60)
'''
snake1 = Snake(pygame.Vector2(2 * GRID, 2 * GRID), Direction.EAST, 3,
               [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d])

apple1 = Apple(pygame.Vector2(5 * GRID, 5 * GRID))
apple2 = Apple(pygame.Vector2(8 * GRID, 5 * GRID))
apple3 = Apple(pygame.Vector2(9 * GRID, 5 * GRID))
applesList = [apple1, apple2, apple3]
'''

'''
player_direction = Direction.EAST
length = 3
score = 0
high_score = 0
start_time = time.time()
apple_pos = pygame.Vector2(random.randrange(SCREEN_WIDTH) * GRID, random.randrange(SCREEN_HEIGHT) * GRID)
dt = 0

player2_pos = pygame.Vector2(START_X * GRID + (2 * GRID), START_Y * GRID + (2 * GRID))
player2_positions = []
player2_direction = Direction.WEST
length2 = 3
dt2 = 0


while running:
    screen.fill((20, 20, 20))
    pygame.display.set_caption(f"Snake: SPACE to start | Score: {score} | Highscore: {high_score}")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_pressed()[0] or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            player_pos = pygame.Vector2(START_X * GRID, START_Y * GRID)
            player_positions = []
            player_direction = Direction.EAST
            length = 3
            score = 0
            start_time = time.time()
            apple_pos = pygame.Vector2(random.randrange(SCREEN_WIDTH) * GRID, random.randrange(SCREEN_HEIGHT) * GRID)
            playing = True
            dt = 0
            if multiplayer:
                player2_pos = pygame.Vector2(START_X * GRID + (2 * GRID), START_Y * GRID + (2 * GRID))
                player2_positions = []
                player2_direction = Direction.WEST
                length2 = 3
                dt2 = 0


    while playing:
        screen.fill("black")
        time_elapsed = int(time.time() - start_time)
        mins, secs = divmod(time_elapsed, 60)
        pygame.display.set_caption(f"Snake: Playing for {mins}:{secs:02d} | Score: {score} | Highscore: {high_score}")

        old_direction = player_direction
        old_direction2 = player2_direction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and player_direction != Direction.SOUTH:
                    player_direction = Direction.NORTH
                elif event.key == pygame.K_d and player_direction != Direction.WEST:
                    player_direction = Direction.EAST
                elif event.key == pygame.K_s and player_direction != Direction.NORTH:
                    player_direction = Direction.SOUTH
                elif event.key == pygame.K_a and player_direction != Direction.EAST:
                    player_direction = Direction.WEST
                if multiplayer:
                    if event.key == pygame.K_UP and player2_direction != Direction.SOUTH:
                        player2_direction = Direction.NORTH
                    elif event.key == pygame.K_RIGHT and player2_direction != Direction.WEST:
                        player2_direction = Direction.EAST
                    elif event.key == pygame.K_DOWN and player2_direction != Direction.NORTH:
                        player2_direction = Direction.SOUTH
                    elif event.key == pygame.K_LEFT and player2_direction != Direction.EAST:
                        player2_direction = Direction.WEST

        if dt % 8 == 0 or player_direction != old_direction:
            dt = 0
            if player_direction == Direction.NORTH:
                player_pos += pygame.Vector2(0, -GRID)
            elif player_direction == Direction.EAST:
                player_pos += pygame.Vector2(GRID, 0)
            elif player_direction == Direction.SOUTH:
                player_pos += pygame.Vector2(0, GRID)
            elif player_direction == Direction.WEST:
                player_pos += pygame.Vector2(-GRID, 0)

            player_pos = pygame.Vector2(player_pos.x % (SCREEN_WIDTH * GRID), player_pos.y % (SCREEN_HEIGHT * GRID))

            if player_pos in player_positions or player_pos in player2_positions:
                playing = False
            elif player_pos == apple_pos or apple_pos in player_positions:
                apple_pos = pygame.Vector2(random.randrange(SCREEN_WIDTH) * GRID, random.randrange(SCREEN_HEIGHT) * GRID)
                while apple_pos in player_positions or apple_pos in player2_positions:
                    apple_pos = pygame.Vector2(random.randrange(SCREEN_WIDTH) * GRID, random.randrange(SCREEN_HEIGHT) * GRID)
                length += 1
                score += 1
                if score > high_score:
                    high_score = score

            player_positions.insert(0, pygame.Vector2(int(player_pos.x) % (SCREEN_WIDTH * GRID), int(player_pos.y) % (SCREEN_HEIGHT * GRID)))
            player_positions = player_positions[0:length]

        for i, position in enumerate(player_positions):
            if i == 0:
                color = (0, 150, 0)
            else:
                color = (0 ,255, 0)
            pygame.draw.rect(screen, color, pygame.Rect(position.x, position.y, GRID, GRID))


        if multiplayer:
            if dt2 % 8 == 0 or player2_direction != old_direction2:
                dt2 = 0
                if player2_direction == Direction.NORTH:
                    player2_pos += pygame.Vector2(0, -GRID)
                elif player2_direction == Direction.EAST:
                    player2_pos += pygame.Vector2(GRID, 0)
                elif player2_direction == Direction.SOUTH:
                    player2_pos += pygame.Vector2(0, GRID)
                elif player2_direction == Direction.WEST:
                    player2_pos += pygame.Vector2(-GRID, 0)

                player2_pos = pygame.Vector2(player2_pos.x % (SCREEN_WIDTH * GRID), player2_pos.y % (SCREEN_HEIGHT * GRID))

                if player2_pos in player2_positions or player2_pos in player_positions:
                    playing = False
                elif player2_pos == apple_pos or apple_pos in player2_positions:
                    apple_pos = pygame.Vector2(random.randrange(SCREEN_WIDTH) * GRID, random.randrange(SCREEN_HEIGHT) * GRID)
                    while apple_pos in player_positions or apple_pos in player2_positions:
                        apple_pos = pygame.Vector2(random.randrange(SCREEN_WIDTH) * GRID, random.randrange(SCREEN_HEIGHT) * GRID)
                    length2 += 1
                    score += 1
                    if score > high_score:
                        high_score = score

                player2_positions.insert(0, pygame.Vector2(int(player2_pos.x) % (SCREEN_WIDTH * GRID), int(player2_pos.y) % (SCREEN_HEIGHT * GRID)))
                player2_positions = player2_positions[0:length2]

            for i, position in enumerate(player2_positions):
                if i == 0:
                    color = (0, 150, 0)
                else:
                    color = (0, 255, 0)
                pygame.draw.rect(screen, color, pygame.Rect(position.x, position.y, GRID, GRID))

        pygame.draw.rect(screen, "red", pygame.Rect(apple_pos.x, apple_pos.y, GRID, GRID))

        pygame.display.flip()
        clock.tick(60)
        dt += 1
        dt2 += 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
'''