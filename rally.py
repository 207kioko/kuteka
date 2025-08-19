import pygame
import random
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing with Obstacles and Trees")
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
RED = (200, 0, 0)
BLUE = (0, 102, 204)
GREEN = (0, 153, 0)

# Car dimensions
CAR_WIDTH = 50
CAR_HEIGHT = 100

# Font
font = pygame.font.SysFont(None, 40)

# Level settings
LEVELS = {
    "Easy": (4, 7),
    "Medium": (6, 6),
    "Hard": (8, 5),
    "World Class": (10, 4),
    "Legendary": (12, 3)
}

def draw_road(lines, trees_left, trees_right):
    screen.fill(GRAY)

    # Draw trees
    for tree in trees_left + trees_right:
        pygame.draw.circle(screen, GREEN, (tree.x, tree.y), 15)

    # Draw road lines
    for line in lines:
        pygame.draw.rect(screen, WHITE, line)

def draw_player(player):
    pygame.draw.rect(screen, BLUE, player)

def draw_enemies(enemies):
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

def show_game_over():
    screen.fill(GRAY)
    text = font.render("GAME OVER!", True, YELLOW)
    replay = font.render("Press ENTER to play again or ESC to quit", True, WHITE)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 40))
    screen.blit(replay, (WIDTH//2 - replay.get_width()//2, HEIGHT//2 + 10))
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

def show_level_menu():
    screen.fill(GRAY)
    title = font.render("Select Difficulty Level", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

    levels = list(LEVELS.keys())
    instructions = []

    for idx, level in enumerate(levels):
        text = font.render(f"{idx+1}. {level}", True, YELLOW)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 150 + idx * 50))
        instructions.append((pygame.K_1 + idx, level))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                for key, level_name in instructions:
                    if event.key == key:
                        return level_name

def reset_enemy():
    x = random.randint(50, WIDTH - CAR_WIDTH - 50)
    return pygame.Rect(x, -CAR_HEIGHT, CAR_WIDTH, CAR_HEIGHT)

def create_lines():
    return [pygame.Rect(WIDTH//2 - 5, y, 10, 40) for y in range(0, HEIGHT, 80)]

def create_trees(side="left"):
    trees = []
    x_pos = 20 if side == "left" else WIDTH - 20
    for y in range(0, HEIGHT, 80):
        trees.append(pygame.Rect(x_pos, y, 0, 0))  # Just use x and y for drawing
    return trees

def run_game(initial_enemy_speed, seconds_to_increase):
    player = pygame.Rect(WIDTH // 2 - CAR_WIDTH // 2, HEIGHT - CAR_HEIGHT - 10, CAR_WIDTH, CAR_HEIGHT)
    
    # Create multiple enemies
    enemies = [reset_enemy() for _ in range(3)]

    player_speed = 6
    enemy_speed = initial_enemy_speed
    lines = create_lines()
    trees_left = create_trees("left")
    trees_right = create_trees("right")
    speed_increment_timer = 0

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed

        # Move enemies
        for i, enemy in enumerate(enemies):
            enemy.y += enemy_speed
            if enemy.y > HEIGHT:
                enemies[i] = reset_enemy()

        # Move road lines
        for line in lines:
            line.y += enemy_speed
            if line.y > HEIGHT:
                line.y = -40

        # Move trees
        for tree in trees_left + trees_right:
            tree.y += enemy_speed
            if tree.y > HEIGHT:
                tree.y = -40

        # Collision check
        for enemy in enemies:
            if player.colliderect(enemy):
                return show_game_over()

        # Increase difficulty
        speed_increment_timer += 1
        if speed_increment_timer >= FPS * seconds_to_increase:
            enemy_speed += 1
            speed_increment_timer = 0

        # Draw everything
        draw_road(lines, trees_left, trees_right)
        draw_player(player)
        draw_enemies(enemies)
        pygame.display.flip()

# --- Main Loop ---
while True:
    level_selected = show_level_menu()
    speed, interval = LEVELS[level_selected]
    play_again = run_game(speed, interval)
    if not play_again:
        break

pygame.quit()
