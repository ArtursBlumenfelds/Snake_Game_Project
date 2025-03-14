import pygame
import random
import csv

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400  # Window size
CELL_SIZE = 20            # Snake cell size
WHITE, GREEN, RED, BLACK, BLUE, YELLOW, BACKGROUND_COLOR, DETAIL_COLOR = (
    (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0), (0, 0, 255), (255, 255, 0), (50, 168, 82), (45, 155, 75)
)
FONT = pygame.font.Font(None, 36)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT + 30))  # Adjusted to prevent score tab overlap
pygame.display.set_caption("Snake Game")

# File to store scores
SCORES_FILE = "scores.csv"

# Function to save score with username
def save_score(username, score):
    with open(SCORES_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, score])

# Function to load scores
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

# Function to display text
def draw_text(text, x, y, color=WHITE):
    label = FONT.render(text, True, color)
    screen.blit(label, (x, y))

# Function to draw detailed background
def draw_background():
    screen.fill(BACKGROUND_COLOR)
    for i in range(0, WIDTH, CELL_SIZE * 2):
        for j in range(30, HEIGHT + 30, CELL_SIZE * 2):
            pygame.draw.rect(screen, DETAIL_COLOR, (i, j, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, DETAIL_COLOR, (i + CELL_SIZE, j + CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to get username
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

# Main game function
def game():
    clock = pygame.time.Clock()
    snake = [(100, 100)]
    direction = (CELL_SIZE, 0)
    food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(30, HEIGHT + 30, CELL_SIZE))
    score = 0

    running = True
    while running:
        draw_background()

        # Event handling
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

        # Move snake
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Check for collision with itself or walls
        if new_head in snake or not (0 <= new_head[0] < WIDTH and 30 <= new_head[1] < HEIGHT + 30):
            username = get_username()
            save_score(username, score)
            break

        snake.insert(0, new_head)

        # Check if food is eaten
        if new_head == food:
            score += 10
            food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(30, HEIGHT + 30, CELL_SIZE))
        else:
            snake.pop()

        # Draw snake and food with better visuals
        for segment in snake:
            pygame.draw.rect(screen, BLUE, (*segment, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, RED, (food[0] + CELL_SIZE // 2, food[1] + CELL_SIZE // 2), CELL_SIZE // 2)
        pygame.draw.rect(screen, GREEN, (food[0] + CELL_SIZE // 4, food[1], CELL_SIZE // 2, CELL_SIZE // 4))

        # Display score in a top bar
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 30))
        draw_text(f"Score: {score}", 10, 5, WHITE)

        pygame.display.flip()
        clock.tick(10)

# Function to display scores
def show_scores():
    screen.fill(BLACK)
    scores = load_scores()
    draw_text("High Scores:", 200, 50, YELLOW)
    for i, (username, score) in enumerate(scores):
        draw_text(f"{i + 1}. {username}: {score} points", 200, 100 + i * 30, WHITE)
    draw_text("Press SPACE to start", 150, 300, GREEN)
    pygame.display.flip()

    # Wait for space key to start game
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Start game loop
while True:
    show_scores()
    game()