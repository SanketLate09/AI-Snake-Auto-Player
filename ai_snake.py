import pygame
import random
import heapq

# ==========================================================
# AI MINI PROJECT — AI SNAKE AUTO PLAYER
# ==========================================================
#
# UNIT I — Intelligent Agents
# ----------------------------------------------------------
# Snake acts as a Goal-Based Intelligent Agent.
#
# Environment → Grid world
# Agent → Snake
# Goal → Reach food safely
#
# State Representation:
# State = (x, y) position of snake head
#
# Operators:
# Move Up, Down, Left, Right
#
# Performance Measure:
# Maximize food eaten without collision
#
# Environment Type:
# - Fully Observable
# - Deterministic
# - Static
# - Discrete
#
# ----------------------------------------------------------
#
# UNIT II — Search Techniques
# ----------------------------------------------------------
# A* Search algorithm is used to compute the optimal path
# from the snake's head to the food.
#
# A* Evaluation Function:
# f(n) = g(n) + h(n)
#
# g(n) = cost from start node
# h(n) = heuristic estimate to goal
#
# Heuristic used:
# Manhattan Distance
#
# ----------------------------------------------------------
#
# UNIT III — Constraint Satisfaction
# ----------------------------------------------------------
# Constraints applied:
#
# 1. Snake cannot collide with walls
# 2. Snake cannot collide with its body
# 3. Movement limited within grid
#
# These constraints convert navigation into
# a constrained state-space search problem.
# ==========================================================

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 20

ROWS = WIDTH // CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Snake Auto Player")

clock = pygame.time.Clock()

WHITE = (255,255,255)
GREEN = (0,200,0)
RED = (200,0,0)
BLACK = (0,0,0)


# ----------------------------------------------------------
# UNIT II — Heuristic Function
# Manhattan Distance
# ----------------------------------------------------------
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ----------------------------------------------------------
# UNIT II — A* SEARCH ALGORITHM
# ----------------------------------------------------------
def astar(start, goal, snake_body):

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}

    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:

        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:

            neighbor = (current[0] + dx, current[1] + dy)

            # UNIT III — Constraint: body collision
            if neighbor in snake_body:
                continue

            # UNIT III — Constraint: wall boundaries
            if not (0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < ROWS):
                continue

            temp_g = g_score[current] + 1

            if neighbor not in g_score or temp_g < g_score[neighbor]:

                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + heuristic(neighbor, goal)

                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []


# ----------------------------------------------------------
# Food generation
# ----------------------------------------------------------
def spawn_food(snake):

    while True:
        food = (
            random.randint(0, ROWS - 1),
            random.randint(0, ROWS - 1)
        )

        if food not in snake:
            return food


# Initial snake
snake = [(5,5),(4,5),(3,5)]

food = spawn_food(snake)

path = []

running = True

while running:

    clock.tick(8)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    head = snake[0]

    # ----------------------------------------------------------
    # UNIT II — AI decision using A* Search
    # ----------------------------------------------------------
    if not path:
        path = astar(head, food, snake)

    if path:
        next_move = path.pop(0)
    else:
        next_move = head


    # UNIT III — Wall collision constraint
    if not (0 <= next_move[0] < ROWS and 0 <= next_move[1] < ROWS):
        running = False


    snake.insert(0, next_move)


    # Food eaten
    if next_move == food:
        food = spawn_food(snake)
        path = []
    else:
        snake.pop()


    # ----------------------------------------------------------
    # UNIT III — Body collision constraint
    # ----------------------------------------------------------
    new_head = snake[0]

    if new_head in snake[1:]:
        running = False


    # Drawing environment
    screen.fill(BLACK)


    # Draw snake
    for segment in snake:
        pygame.draw.rect(
            screen,
            GREEN,
            (segment[0]*CELL, segment[1]*CELL, CELL, CELL)
        )


    # Draw food
    pygame.draw.rect(
        screen,
        RED,
        (food[0]*CELL, food[1]*CELL, CELL, CELL)
    )


    pygame.display.update()


pygame.quit()