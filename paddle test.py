import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paddle Test")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
clock = pygame.time.Clock()

# Paddle
paddle = pygame.Rect(250, 350, 100, 10)
paddle_speed = 7

running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.x += paddle_speed

    pygame.draw.rect(screen, BLUE, paddle)
    pygame.display.flip()

pygame.quit()
