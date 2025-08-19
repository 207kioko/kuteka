import pygame
import sys

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Game with Levels")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
GREEN = (0, 255, 0)

clock = pygame.time.Clock()
FPS = 60
font = pygame.font.SysFont(None, 30)

LEVELS = {
    "Easy":       {"paddle_width": 120, "ball_speed": 4, "rows": 3},
    "Medium":     {"paddle_width": 100, "ball_speed": 5, "rows": 4},
    "Hard":       {"paddle_width": 80,  "ball_speed": 6, "rows": 5},
    "World Class":{"paddle_width": 70,  "ball_speed": 7, "rows": 6},
    "Legendary":  {"paddle_width": 60,  "ball_speed": 8, "rows": 7}
}

def draw_text(text, y, center=True):
    rendered = font.render(text, True, WHITE)
    if center:
        x = SCREEN_WIDTH // 2 - rendered.get_width() // 2
    else:
        x = 20
    screen.blit(rendered, (x, y))

def level_selection_screen():
    while True:
        screen.fill(BLACK)
        draw_text("Select Level:", 80)
        levels = list(LEVELS.keys())
        for i, level in enumerate(levels):
            draw_text(f"{i+1}. {level}", 130 + i * 40)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_5:
                    return levels[event.key - pygame.K_1]

def create_bricks(rows):
    bricks = []
    BRICK_WIDTH = 60
    BRICK_HEIGHT = 20
    COLS = 8
    for row in range(rows):
        for col in range(COLS):
            brick = pygame.Rect(col * (BRICK_WIDTH + 10) + 35, row * (BRICK_HEIGHT + 10) + 30, BRICK_WIDTH, BRICK_HEIGHT)
            bricks.append(brick)
    return bricks

def draw(paddle, ball, bricks, score):
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, RED, ball)
    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)
    draw_text(f"Score: {score}", 10, center=False)
    pygame.display.flip()

def game_over_screen(win):
    screen.fill(BLACK)
    message = "YOU WIN!" if win else "GAME OVER!"
    draw_text(message, SCREEN_HEIGHT // 2 - 20)
    draw_text("Press ENTER to play again or ESC to quit", SCREEN_HEIGHT // 2 + 20)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False

def run_game(level_name):
    config = LEVELS[level_name]
    paddle_width = config["paddle_width"]
    ball_speed = config["ball_speed"]
    brick_rows = config["rows"]

    paddle = pygame.Rect((SCREEN_WIDTH - paddle_width) // 2, SCREEN_HEIGHT - 30, paddle_width, 10)
    paddle_speed = 7
    ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 16, 16)
    ball_dx = ball_speed
    ball_dy = -ball_speed
    bricks = create_bricks(brick_rows)
    score = 0

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
            paddle.x += paddle_speed

        # Move ball
        ball.x += ball_dx
        ball.y += ball_dy

        # Wall collision
        if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
            ball_dx *= -1
        if ball.top <= 0:
            ball_dy *= -1
        if ball.bottom >= SCREEN_HEIGHT:
            if game_over_screen(win=False):
                return True
            else:
                return False

        # Paddle collision
        if ball.colliderect(paddle):
            ball_dy *= -1

        # Brick collision
        for brick in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_dy *= -1
                score += 10
                break

        if not bricks:
            if game_over_screen(win=True):
                return True
            else:
                return False

        draw(paddle, ball, bricks, score)

# Main loop with level selector
while True:
    selected_level = level_selection_screen()
    play = run_game(selected_level)
    if not play:
        break
