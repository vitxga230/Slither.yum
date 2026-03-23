import pygame
import random
import sys
import time
import math

# ================= INIT =================
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 25
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slither.Yum")
clock = pygame.time.Clock()
speed = 10  # FPS for the game loop

# ================= COLORS =================
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
BLUE = (0, 120, 255)
RED = (220, 40, 40)
GREY = (120, 120, 120)
LIGHT_GREY = (190, 190, 190)

# ================= FONTS =================
TITLE_FONT = pygame.font.Font("Minecraftia.ttf", 64)
MENU_FONT = pygame.font.Font("Minecraftia.ttf", 24)
GAME_FONT = pygame.font.Font("Minecraftia.ttf", 22)
COUNT_FONT = pygame.font.Font("Minecraftia.ttf", 96)

# ================= SOUNDS =================
try:
    munch_sound = pygame.mixer.Sound("munch.wav")
    buzz_sound = pygame.mixer.Sound("buzz.wav")
    celebration_sound = pygame.mixer.Sound("celebration.wav")
    pygame.mixer.music.load("bg_music.mp3")
except:
    print("⚠️ Missing sound files")

# ================= GLOBAL VARIABLES =================
snake = [(100, 50), (75, 50), (50, 50)]
direction = "RIGHT"
score = 0
healthy_eaten = 0
food_types = {
    "healthy": {"color": BLUE, "points": 5},
    "junk": {"color": RED, "points": -5}
}
food_list = []

# ================= FUNCTIONS =================
def random_position():
    return (
        random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
        random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE
    )

def draw_snake(snk):
    for seg in snk:
        pygame.draw.rect(screen, GREEN, (*seg, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, DARK_GREEN, (*seg, CELL_SIZE, CELL_SIZE), 2)

def move_snake():
    global score, healthy_eaten
    x, y = snake[0]
    if direction == "UP": y -= CELL_SIZE
    if direction == "DOWN": y += CELL_SIZE
    if direction == "LEFT": x -= CELL_SIZE
    if direction == "RIGHT": x += CELL_SIZE

    x %= WIDTH
    y %= HEIGHT
    new_head = (x, y)
    snake.insert(0, new_head)

    for i, (pos, kind) in enumerate(food_list):
        if new_head == pos:
            score += food_types[kind]["points"]
            if kind == "healthy":
                healthy_eaten += 1
                munch_sound.play()
            else:
                buzz_sound.play()
            food_list.pop(i)
            return
    snake.pop()

def spawn_food():
    healthy_count = sum(1 for _, k in food_list if k == "healthy")
    junk_count = sum(1 for _, k in food_list if k == "junk")

    while healthy_count < 2:
        food_list.append((random_position(), "healthy"))
        healthy_count += 1
    while junk_count < 2:
        food_list.append((random_position(), "junk"))
        junk_count += 1

def draw_food():
    for pos, kind in food_list:
        pygame.draw.rect(screen, food_types[kind]["color"], (*pos, CELL_SIZE, CELL_SIZE))

def mc_button(rect, text):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]

    color = GREY
    border = LIGHT_GREY
    offset = 0

    if rect.collidepoint(mouse):
        color = LIGHT_GREY
        border = WHITE
        offset = 2
        if click:
            offset = 5

    pygame.draw.rect(screen, color, rect.move(0, offset))
    pygame.draw.rect(screen, border, rect.move(0, offset), 3)

    label = MENU_FONT.render(text, True, BLACK)
    screen.blit(label, (rect.centerx - label.get_width()//2, rect.centery - label.get_height()//2 + offset))

    return rect.collidepoint(mouse) and click

# ================= TITLE SCREEN =================
def title_screen():
    demo_snake = [(200, 360), (175, 360), (150, 360)]
    demo_dir = "RIGHT"
    hover_time = 0
    move_timer = 0
    start_btn = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 120, 240, 60)

    while True:
        screen.fill(BLACK)
        move_timer += 1
        if move_timer % 8 == 0:
            x, y = demo_snake[0]
            if demo_dir == "RIGHT": x += CELL_SIZE
            elif demo_dir == "LEFT": x -= CELL_SIZE
            elif demo_dir == "UP": y -= CELL_SIZE
            elif demo_dir == "DOWN": y += CELL_SIZE

            x %= WIDTH
            y %= HEIGHT
            if random.randint(0, 30) == 0:
                demo_dir = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            demo_snake.insert(0, (x, y))
            demo_snake.pop()
        draw_snake(demo_snake)

        hover_time += 0.05
        float_y = math.sin(hover_time) * 8
        slither = TITLE_FONT.render("Slither.", True, BLUE)
        yum = TITLE_FONT.render("Yum", True, RED)
        total_width = slither.get_width() + yum.get_width()
        x_base = WIDTH//2 - total_width//2
        y_base = 140 + float_y
        screen.blit(slither, (x_base, y_base))
        screen.blit(yum, (x_base + slither.get_width(), y_base))

        if mc_button(start_btn, "START"):
            return

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(60)

# ================= INSTRUCTIONS =================
def instructions_screen():
    next_btn = pygame.Rect(WIDTH - 190, HEIGHT - 80, 160, 50)
    while True:
        screen.fill(BLACK)
        title = MENU_FONT.render("How to Play Slither.Yum", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))
        lines = [
            "Firstly, you need to make sure you avoid eating",
            "the red food, or else you lose points.",
            "You'll have exactly 1 minute to eat all",
            "the blue food and aim to gather as much",
            "points as possible.",
            "Goodluck!!!"
        ]
        for i, line in enumerate(lines):
            txt = MENU_FONT.render(line, True, WHITE)
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 160 + i*40))
        if mc_button(next_btn, "NEXT"):
            return
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(60)

# ================= COUNTDOWN =================
def countdown():
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        num = COUNT_FONT.render(str(i), True, WHITE)
        screen.blit(num, (WIDTH//2 - num.get_width()//2, HEIGHT//2 - 60))
        pygame.display.update()
        pygame.time.delay(1000)

# ================= END SCREEN =================
def end_screen():
    global score, healthy_eaten, snake, direction, food_list
    pygame.mixer.stop()
    pygame.mixer.music.stop()
    celebration_sound.play()
    try_again_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50)

    while True:
        screen.fill(BLACK)
        end1 = MENU_FONT.render(f"Final Score: {score}", True, WHITE)
        end2 = MENU_FONT.render(f"Healthy Food Eaten: {healthy_eaten}", True, WHITE)
        screen.blit(end1, (WIDTH//2 - end1.get_width()//2, HEIGHT//2 - 40))
        screen.blit(end2, (WIDTH//2 - end2.get_width()//2, HEIGHT//2 + 10))
        if mc_button(try_again_btn, "Try Again?"):
            score = 0
            healthy_eaten = 0
            snake = [(100, 50), (75, 50), (50, 50)]
            direction = "RIGHT"
            food_list.clear()
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.4)
            instructions_screen()
            countdown()
            return
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(60)

# ================= GAME SESSION LOOP =================
while True:
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.4)
    title_screen()
    instructions_screen()
    countdown()

    snake = [(100, 50), (75, 50), (50, 50)]
    direction = "RIGHT"
    food_list.clear()
    score = 0
    healthy_eaten = 0

    start_time = time.time()
    running = True

    while running:
        elapsed = time.time() - start_time
        bg_color = WHITE if elapsed >= 50 else BLACK
        screen.fill(bg_color)

        spawn_food()
        draw_food()
        draw_snake(snake)

        score_text = GAME_FONT.render(f"Score: {score}", True, GREEN)
        time_text = GAME_FONT.render(f"Time: {max(0, 60-int(elapsed))}", True, GREEN)
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (10, 40))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and direction != "DOWN": direction = "UP"
                if e.key == pygame.K_DOWN and direction != "UP": direction = "DOWN"
                if e.key == pygame.K_LEFT and direction != "RIGHT": direction = "LEFT"
                if e.key == pygame.K_RIGHT and direction != "LEFT": direction = "RIGHT"

        move_snake()
        pygame.display.update()
        clock.tick(speed)

        if elapsed >= 60:
            running = False

    end_screen()