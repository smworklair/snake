import pygame
import sys
import random

pygame.init()

screen_width = 600
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Змейка')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (50, 50, 50)
DARK_GRAY = (30, 30, 30)

snake_colors = [GREEN, BLUE, ORANGE]
current_snake_color = 0
field_colors = [BLACK, GRAY, DARK_GRAY]
current_field_color = 0

clock = pygame.time.Clock()


def reset_game():
    global snake_pos, snake_body, direction, change_to, score, food_pos, food_spawn
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    change_to = direction
    score = 0
    food_pos = [random.randrange(1, (screen_width // 10)) * 10,
                random.randrange(1, (screen_height // 10)) * 10]
    food_spawn = True


reset_game()

font = pygame.font.SysFont('arial', 25)

running = True
game_active = True
paused = False


def draw_interface():

    score_text = font.render(f"Счет: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    settings_text = font.render("1-3:|4-6:", True, WHITE)
    screen.blit(settings_text, (10, screen_height - 40))


def game_step():
    global direction, change_to, score, food_spawn, game_active, paused, current_snake_color, current_field_color, food_pos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

            if not paused:

                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

            if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                current_snake_color = event.key - pygame.K_1

            if event.key in (pygame.K_4, pygame.K_5, pygame.K_6):
                current_field_color = event.key - pygame.K_4

    if paused or not game_active:
        return

    direction = change_to

    if direction == 'UP':
        snake_pos[1] -= 10
    elif direction == 'DOWN':
        snake_pos[1] += 10
    elif direction == 'LEFT':
        snake_pos[0] -= 10
    elif direction == 'RIGHT':
        snake_pos[0] += 10

    if (snake_pos[0] < 0 or snake_pos[0] >= screen_width or
            snake_pos[1] < 0 or snake_pos[1] >= screen_height or
            snake_pos in snake_body[1:]):
        game_active = False
        return

    if snake_pos == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, (screen_width // 10)) * 10,
                    random.randrange(1, (screen_height // 10)) * 10]
    food_spawn = True

    snake_body.insert(0, list(snake_pos))

    screen.fill(field_colors[current_field_color])

    for pos in snake_body:
        pygame.draw.rect(screen, snake_colors[current_snake_color],
                         pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    draw_interface()

    pygame.display.flip()
    clock.tick(15)


while running:
    game_step()

    if not game_active:
        screen.fill(BLACK)
        text = font.render("Потрачено! R для рестарта   ", True, RED)
        screen.blit(text, (screen_width // 2 - 120, screen_height // 2 - 20))
        text2 = font.render("Q Выход", True, RED)
        screen.blit(text2, (screen_width // 2 - 50, screen_height // 2 + 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    game_active = True
                if event.key == pygame.K_q:
                    running = False

pygame.quit()
sys.exit()