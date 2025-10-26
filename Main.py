import pygame
import random
import time
from enum import Enum


pygame.init()

GRID = 25
SCREEN_WIDTH = 16
SCREEN_HEIGHT = 16
SCREEN_SIZE = (SCREEN_WIDTH * GRID, SCREEN_HEIGHT * GRID)
START_X = 2
START_Y = 2

screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True
playing = False

player_pos = pygame.Vector2(START_X * GRID, START_Y * GRID)
player_positions = []
class Direction (Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
player_direction = Direction.EAST
length = 3
score = 0
high_score = 0
start_time = time.time()
apple_pos = pygame.Vector2(random.randrange(SCREEN_WIDTH) * GRID, random.randrange(SCREEN_HEIGHT) * GRID)


while running:
    screen.fill((20, 20, 20))
    pygame.display.set_caption(f"Snake: SPACE to start | Score: {score} | Highscore: {high_score}")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_pos = pygame.Vector2(START_X * GRID, START_Y * GRID)
                player_positions = []
                player_direction = Direction.EAST
                length = 3
                score = 0
                start_time = time.time()
                apple_pos = pygame.Vector2(random.randrange(SCREEN_WIDTH) * GRID, random.randrange(SCREEN_HEIGHT) * GRID)
                playing = True


    while playing:
        screen.fill("black")
        time_elapsed = int(time.time() - start_time)
        mins, secs = divmod(time_elapsed, 60)
        pygame.display.set_caption(f"Snake: Playing for {mins}:{secs:02d} | Score: {score} | Highscore: {high_score}")

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

        if player_direction == Direction.NORTH:
            player_pos += pygame.Vector2(0, -GRID)
        elif player_direction == Direction.EAST:
            player_pos += pygame.Vector2(GRID, 0)
        elif player_direction == Direction.SOUTH:
            player_pos += pygame.Vector2(0, GRID)
        elif player_direction == Direction.WEST:
            player_pos += pygame.Vector2(-GRID, 0)

        player_pos = pygame.Vector2(player_pos.x % (SCREEN_WIDTH * GRID), player_pos.y % (SCREEN_HEIGHT * GRID))

        if player_pos in player_positions:
            playing = False
        elif player_pos == apple_pos:
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

        pygame.draw.rect(screen, "red", pygame.Rect(apple_pos.x, apple_pos.y, GRID, GRID))

        pygame.display.flip()
        fps = 8
        clock.tick(fps)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()