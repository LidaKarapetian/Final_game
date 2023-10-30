"""
Rock, Paper, Scissors Game
This script implements a Rock, Paper, Scissors game using the Pygame library.
"""
import sys
import subprocess

def install_module(module_name):
    """
    Install a Python module using pip.
    Args (module_name): The name of the module to install.
    """
    try:
        subprocess.run(["pip", "install", module_name], check=True)
        print(f"Successfully installed the '{module_name}' module.")
    except subprocess.CalledProcessError as error:
        print(f"Error installing the '{module_name}' module: {error}")

try:
    import pygame
except ModuleNotFoundError:
    print("The 'pygame' module is not installed. Installing it now...")
    install_module("pygame")
    import pygame

try:
    import random
except ModuleNotFoundError:
    print("The 'random' module is not installed. Installing it now...")
    install_module("random")
    import random

WIDTH, HEIGHT = 1250, 900
WHITE = (255, 255, 255)
CHOICES = ["rock", "paper", "scissors"]
OUTCOMES = {
    ("rock", "scissors"): "Rock smashes scissors! You win!",
    ("paper", "rock"): "Paper covers rock! You win!",
    ("scissors", "paper"): "Scissors cuts paper! You win!",
}

pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock, Paper, Scissors")

try:
    ROCK_IMG = pygame.image.load("rock.jpg")
    PAPER_IMG = pygame.image.load("paper.jpg")
    SCISSORS_IMG = pygame.image.load("scissors.jpg")
    BACKGROUND_IMG = pygame.image.load("background.jpg")
    BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))
except pygame.error as exception:
    print(f"Error loading image: {exception}")
    pygame.quit()
    sys.exit()

COMPUTER_IMAGES = {
    "rock": ROCK_IMG,
    "paper": PAPER_IMG,
    "scissors": SCISSORS_IMG
}

def draw_text(text, x_coordinate, y_coordinate, font_size=36, color=WHITE):
    """
    Display text on the game window.
    Args:
        text : The text to display.
        x_coordinate : The x-coordinate of the text.
        y_coordinate : The y-coordinate of the text.
        font_size : The font size of the text. Default is 36.
        color : The text color as an (R, G, B) tuple. Default is WHITE.
    """
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x_coordinate, y_coordinate)
    WINDOW.blit(text_surface, text_rect)

def start_screen():
    """
        Display the start screen for the Rock, Paper, Scissors game.
        Allows the user to start the game or exit.
    """
    start_button_rect = pygame.Rect(470, 700, 200, 50)
    exit_button_rect = pygame.Rect(470, 800, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return
                if exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        WINDOW.blit(BACKGROUND_IMG, (0, 0))

        draw_text("Welcome to Rock, Paper, Scissors!", 330, 120, font_size=50)

        pygame.draw.rect(WINDOW, (0, 255, 0), start_button_rect)
        draw_text("Start Game", 500, 710, font_size=38)

        pygame.draw.rect(WINDOW, (255, 0, 0), exit_button_rect)
        draw_text("Exit Game", 500, 810, font_size=38)

        if start_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(WINDOW, (0, 255, 0), start_button_rect)
        if exit_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(WINDOW, (200, 0, 0), exit_button_rect)

        pygame.display.flip()

def computer_choice_screen(user_action, computer_action):
    """
        Display the computer's choice and the user's choice on the screen.
    """
    result_window = pygame.display.set_mode((WIDTH, HEIGHT))

    result_window.fill((255, 255, 255))

    draw_text(f"You have chosen: {user_action}", 100, 100, color=(0, 0, 0), font_size=50)

    draw_text(f"Computer chose: {computer_action}", 800, 100, color=(0, 0, 0), font_size=50)

    button_width = 200
    button_height = 50
    button_x = 525

    your_choice_image = COMPUTER_IMAGES.get(user_action)
    if your_choice_image:
        result_window.blit(your_choice_image, (100, 200))

    computer_choice_image = COMPUTER_IMAGES.get(computer_action)
    if computer_choice_image:
        result_window.blit(computer_choice_image, (800, 200))

    pygame.draw.rect(result_window, (0, 0, 0), (button_x, 700, button_width, button_height))
    draw_text("Show Result", button_x + 20, 710, font_size=38)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (470 <= event.pos[0] <= 670) and (700 <= event.pos[1] <= 750):
                    return

def game_result(user_action, computer_action):
    """
    Display the game result, showing the user's and computer's choices, and the outcome.
    Args:
        user_action : The user's choice ("rock", "paper", "scissors").
        computer_action : The computer's choice.
    """
    result_window = pygame.display.set_mode((WIDTH, HEIGHT))
    if user_action == computer_action:
        background_img = pygame.image.load("goodResult.jpg")
    else:
        background_img = pygame.image.load("badResult.jpg")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    result_window.blit(background_img, (0, 0))

    draw_text(f"You chose {user_action}", 500, 100, color=(255, 255, 255))
    draw_text(f"Computer chose {computer_action}", 470, 140, color=(255, 255, 255))

    if user_action == computer_action:
        draw_text(f"Both players selected {user_action}. It's a tie!", 400, 180, color=(255, 255, 255))
    elif (user_action, computer_action) in OUTCOMES:
        draw_text(OUTCOMES[(user_action, computer_action)], 450, 200, color=(255, 255, 255))
    else:
        draw_text("Your choice doesn't exist. You lose", 400, 200, color=(0, 0, 0))

    draw_text("Play again? (y/n):", 500, 780, color=(0, 0, 0))
    pygame.display.flip()

    continue_game = None

    while continue_game is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    continue_game = True
                if event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()

    if continue_game:
        main()

def play_game():
    """
    This function manages the core game play logic for the Rock, Paper, Scissors game.
    """
    
    user_action = None
    computer_action = random.choice(CHOICES)

    WINDOW.fill((255, 255, 255))
    draw_text("You have to choose one of them:", 310, 100, color=(255, 211, 155), font_size=60)

    image_spacing = 50
    image_x = 0

    WINDOW.blit(ROCK_IMG, (image_x, 200))
    image_x += ROCK_IMG.get_width() + image_spacing
    WINDOW.blit(PAPER_IMG, (image_x, 200))
    image_x += PAPER_IMG.get_width() + image_spacing
    WINDOW.blit(SCISSORS_IMG, (image_x, 200))

    rock_rect = pygame.Rect(0, 200, ROCK_IMG.get_width(), ROCK_IMG.get_height())
    paper_rect = pygame.Rect(ROCK_IMG.get_width() + image_spacing, 200, PAPER_IMG.get_width(), PAPER_IMG.get_height())
    scissors_rect = pygame.Rect(2 * (ROCK_IMG.get_width() + image_spacing), 200, SCISSORS_IMG.get_width(), SCISSORS_IMG.get_height())

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_x, click_y = event.pos
                if rock_rect.collidepoint(click_x, click_y):
                    user_action = "rock"
                elif paper_rect.collidepoint(click_x, click_y):
                    user_action = "paper"
                elif scissors_rect.collidepoint(click_x, click_y):
                    user_action = "scissors"

        if user_action:
            break

    computer_choice_screen(user_action, computer_action)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (470 <= event.pos[0] <= 670) and (700 <= event.pos[1] <= 750):
                    game_result(user_action, computer_action)
                    return

def main():
    """
        Main function to run the Rock, Paper, Scissors game.
    """
    start_screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        play_game()

if __name__ == "__main__":
    main()
