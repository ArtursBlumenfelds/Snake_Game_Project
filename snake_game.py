import pygame
import random
import csv
import subprocess

pygame.init()

# constants
WIDTH, HEIGHT = 400, 400
CELL_SIZE = 20
WHITE, GREEN, RED, BLACK, BLUE, YELLOW, BACKGROUND_COLOR = (
    (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0), (0, 0, 255), (255, 255, 0), (0, 128, 0)
)
FONT = pygame.font.Font(None, 36)

# screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# file to store scores
SCORES_FILE = "scores.csv"

def open_score_manager():
    subprocess.Popen(["python", "score_manager.py"])

def save_score(username, score):
    with open(SCORES_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, score])

def load_scores():
    try:
        with open(SCORES_FILE, "r") as file:
            reader = csv.reader(file)
            scores = []
            for row in reader:
                if len(row) == 2:
                    try:
                        scores.append((row[0], int(row[1])))
                    except ValueError:
                        continue
        return sorted(scores, key=lambda x: x[1], reverse=True)[:5]
    except FileNotFoundError:
        return []

def draw_text(text, x, y, color=WHITE):
    label = FONT.render(text, True, color)
    screen.blit(label, (x, y))

def draw_background():
    screen.fill(BACKGROUND_COLOR)

def draw_eyes(head_pos, direction):
    x, y = head_pos
    cx, cy = x + CELL_SIZE // 2, y + CELL_SIZE // 2
    offset = 5

    if direction == (CELL_SIZE, 0):  # right
        eye1 = (cx + offset, cy - 4)
        eye2 = (cx + offset, cy + 4)
    elif direction == (-CELL_SIZE, 0):  # left
        eye1 = (cx - offset, cy - 4)
        eye2 = (cx - offset, cy + 4)
    elif direction == (0, CELL_SIZE):  # down
        eye1 = (cx - 4, cy + offset)
        eye2 = (cx + 4, cy + offset)
    elif direction == (0, -CELL_SIZE):  # up
        eye1 = (cx - 4, cy - offset)
        eye2 = (cx + 4, cy - offset)
    else:
        return

    pygame.draw.circle(screen, WHITE, eye1, 2)
    pygame.draw.circle(screen, WHITE, eye2, 2)


def get_username():
    username = ""
    active = True
    while active:
        screen.fill(BLACK)
        draw_text("Enter your name: " + username, 100, 150, YELLOW)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.unicode.isalnum():
                    username += event.unicode
    return username

def game():
    clock = pygame.time.Clock()
    snake = [(100, 100)]
    direction = (CELL_SIZE, 0)
    food = (random.randrange(0, (WIDTH // CELL_SIZE)-1) * CELL_SIZE, random.randrange(1, (HEIGHT // CELL_SIZE)) * CELL_SIZE)
    score = 0

    running = True
    while running:
        draw_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if new_head in snake or not (0 <= new_head[0] < WIDTH and 30 <= new_head[1] < HEIGHT):
            username = get_username()
            save_score(username, score)
            break

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(40, HEIGHT, CELL_SIZE))
            while food in snake:
                food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(40, HEIGHT, CELL_SIZE))
        else:
            snake.pop()

        for i, segment in enumerate(snake):
            pygame.draw.rect(screen, BLUE, (*segment, CELL_SIZE, CELL_SIZE))
            if i == 0:  # head
                draw_eyes(segment, direction)

        pygame.draw.circle(screen, RED, (food[0] + CELL_SIZE // 2, food[1] + CELL_SIZE // 2), CELL_SIZE // 2)

        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 40))
        draw_text(f"Score: {score}", 10, 5, WHITE)

        pygame.display.flip()
        clock.tick(10)

def show_scores():
    screen.fill(BLACK)
    scores = load_scores()
    draw_text("High Scores:", 200, 50, YELLOW)
    for i, (username, score) in enumerate(scores):
        draw_text(f"{i + 1}. {username}: {score} points", 200, 100 + i * 30, WHITE)
    draw_text("Press SPACE to start", 120, 300, GREEN)
    draw_text("Press M to open Score Manager", 60, 340, YELLOW)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_m:
                    open_score_manager()

while True:
    show_scores()
    game()
