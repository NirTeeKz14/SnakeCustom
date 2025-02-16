import pygame
import time
import random

pygame.init()
pygame.mixer.init()

music_folder = 'C:/Users/Killian/Desktop/Projets/Snake/music/'

# Loading the music
try:
    pygame.mixer.music.load(music_folder + 'Snake.io Music.mp3')
except pygame.error as e:
    print(f"Music loading error: {e}")

# Defining colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

key_up = pygame.K_UP
key_down = pygame.K_DOWN
key_left = pygame.K_LEFT
key_right = pygame.K_RIGHT

# Screen dimensions
screen_width = 800
screen_height = 600
block_size = 20

game_window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('SnakeCustom')

clock = pygame.time.Clock()
score_font = pygame.font.SysFont("bahnschrift", 35)

def show_score(score):
    score_text = score_font.render("Score :" + str(score), True, black)
    game_window.blit(score_text, [0, 0])

def load_keys():
    try:
        with open ("keys.txt","r") as file:
            lines = file.read(). splitlines()
            return int(lines[0]), int(lines[1]), int(lines[2]), int(lines[3])
    except FileNotFoundError:
        return pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT
    
def save_keys(up, down, left, right):
    with open("keys.txt", "w") as file:
        file.write(f"{up}\n{down}\n{left}\n{right}")

def change_keys(message):
    display_message(message, white)
    pygame.display.update()
    wait_for_key = True
    while wait_for_key:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return event.key
            
def key_settings_menu():
    global key_up, key_down, key_left, key_right
    in_settings = True
    while in_settings:
        game_window.fill((30,30,30))

        title_surface = score_font.render("Key Configuration", True, (0, 255, 0))
        game_window.blit(title_surface, (screen_width / 2 - title_surface.get_width() / 2, 100))

        up_surface = score_font.render(f"Up Key : {pygame.key.name(key_up)}", True, white)
        down_surface = score_font.render(f"Down Key : {pygame.key.name(key_down)}", True, white)
        left_surface = score_font.render(f"Left Key : {pygame.key.name(key_left)}", True, white)
        right_surface = score_font.render(f"Right Key : {pygame.key.name(key_right)}", True, white)

        game_window.blit(up_surface, (screen_width / 2 - up_surface.get_width() / 2, 250))
        game_window.blit(down_surface, (screen_width / 2 - down_surface.get_width() / 2, 300))
        game_window.blit(left_surface, (screen_width / 2 - left_surface.get_width() / 2, 350))
        game_window.blit(right_surface, (screen_width / 2 - right_surface.get_width() / 2, 400))

        game_window.blit(score_font.render("Press Space to configure a key", True, (255, 255, 0)),
                         (screen_width / 2 - 300, 450))
        
        game_window.blit(score_font.render("Press S to save and return", True, (255, 255, 0)),
                         (screen_width / 2 - 300, 500))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    key_up = change_keys("Press a new key for 'Up'")
                    key_down = change_keys("Press a new key for 'Down'")
                    key_left = change_keys("Press a new key for 'Left'")
                    key_right = change_keys("Press a new key for 'Right'")
                elif event.key == pygame.K_s:
                    save_keys(key_up, key_down, key_left, key_right)
                    in_settings = False

# Load the highest score and levels
def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

def load_level():
    try:
        with open("level.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 1

def save_level(level):
    with open("level.txt", "w") as file:
        file.write(str(level))

# Random color for food
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Display the score
def display_score(score, high_score, time_played, level, text_color):
    score_text = score_font.render(f"Score: {score}", True, text_color)
    high_score_text = score_font.render(f"High Score: {high_score}", True, text_color)
    time_text = score_font.render(f"Time: {time_played:.2f} sec", True, text_color)
    level_text = score_font.render(f"Level: {level}", True, text_color)

    game_window.blit(score_text, [330, 0])
    game_window.blit(high_score_text, [555, 0])
    game_window.blit(time_text, [15, 0])
    game_window.blit(level_text, [15, 50])
    

# Calculate speed based on score
def speed(score):
    base_speed = 10
    speed_increase = score // 5
    return base_speed + speed_increase

# Draw the snake
def draw_snake(block_size, snake_list):
    for i, segment in enumerate (snake_list):
        color = (0, 255, 0) if i < len(snake_list) - 1 else (255, 0, 0)
        pygame.draw.rect(game_window, color, [segment[0], segment[1], block_size, block_size])

# Display a message on the screen
def display_message(msg, color, position=None):
    mesg = score_font.render(msg, True, color)
    if position is None:
        position = [screen_width / 6, screen_height / 3]
    game_window.blit(mesg, position)

# Main menu
def main_menu():
    main_active = True
    level = load_level()

    background_image = pygame.image.load('C:/Users/Killian/Desktop/Projets/Snake/img/menu.png')

    crop_rect = pygame.Rect(50, 50, 950, 950)

    cropped_image = background_image.subsurface(crop_rect)

    while main_active:
        game_window.fill((30, 30, 30))
        game_window.blit(cropped_image, (-60, 0))

        title_font = pygame.font.SysFont("comicsansms", 72)
        title_surface = title_font.render("SnakeCustom", True, (0, 255, 0))
        game_window.blit(title_surface, (screen_width / 2 - title_surface.get_width() / 2, 100))

        level_font = pygame.font.SysFont("comicsansms", 36)
        level_surface = level_font.render(f"Level: {level}", True, white)

        play_button = pygame.Rect(screen_width / 2 - 100, 250, 200, 50)
        scores_button = pygame.Rect(screen_width / 2 - 100, 320, 200, 50)
        settings_button = pygame.Rect(screen_width / 2 - 100, 390, 200, 50)
        quit_button = pygame.Rect(screen_width / 2 - 100, 460, 200, 50)

        pygame.draw.rect(game_window, (0, 255, 0), play_button)
        pygame.draw.rect(game_window, (0, 255, 0), scores_button)
        pygame.draw.rect(game_window, (0, 255, 0), settings_button)
        pygame.draw.rect(game_window, (0, 255, 0), quit_button)

        button_font = pygame.font.SysFont("comicsansms", 36)
        game_window.blit(button_font.render("Play", True, (0, 0, 0)), (screen_width / 2 - 45, 255))
        game_window.blit(button_font.render("Score", True, (0, 0, 0)), (screen_width / 2 - 55, 325))
        game_window.blit(button_font.render("Setting", True, (0, 0, 0)), (screen_width / 2 - 60, 395))
        game_window.blit(button_font.render("Quit", True, (0, 0, 0)), (screen_width / 2 - 60, 465))
        game_window.blit(level_surface, (screen_width / 2 - level_surface.get_width() / 2, screen_height / 17.25))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if play_button.collidepoint(mouse_pos):
                    main_active = False
                elif scores_button.collidepoint(mouse_pos):
                    print("Show score here.")
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                elif settings_button.collidepoint(mouse_pos):
                    key_settings_menu()
                    print("Settings clicked")

# Reset the game
def reset_game():
    x1 = screen_width / 2
    y1 = screen_height / 2
    snake_list = []
    snake_length = 1
    return x1, y1, snake_list, snake_length

# Main game function
def game():
    pygame.mixer.music.play(-1)

    game_over = False
    game_close = False

    x1, y1, snake_list, snake_length = reset_game()

    x1_change = 0
    y1_change = 0

    food_x = round(random.randrange(0, screen_width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, screen_height - block_size) / block_size) * block_size

    high_score = load_high_score()
    game_start = pygame.time.get_ticks()

    text_color = white
    level = load_level()

    while not game_over:
        while game_close:
            pygame.mixer.music.stop()
            game_window.fill(black)

            display_message("You lost! Press Q-Quit or C-Continue", red)
            display_score(snake_length - 1, high_score, time_played, level, text_color)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        game()
                        return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == key_left and x1_change == 0:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == key_right and x1_change == 0:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == key_up and y1_change == 0:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == key_down and y1_change == 0:
                    y1_change = block_size
                    x1_change = 0

        x1 += x1_change
        y1 += y1_change

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True 
            snake_list, snake_length = [], 1

        game_window.fill(black)
        pygame.draw.rect(game_window, blue, [food_x, food_y, block_size, block_size])

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(block_size, snake_list)
        time_played = (pygame.time.get_ticks() - game_start) / 1000
        display_score(snake_length - 1, high_score, time_played, level, text_color)

        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, screen_width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, screen_height - block_size) / block_size) * block_size
            snake_length += 1
            level += 1
            save_level(level)
            print(f"Nourriture générée a : {food_x}, {food_y}")

            if snake_length - 1 > high_score:
                high_score =  snake_length - 1
                save_high_score(high_score)

        clock.tick(speed(snake_length - 1))

        pygame.display.update()

    pygame.quit()
    quit()

# Launch the main menu
main_menu()
game()
