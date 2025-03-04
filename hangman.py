import pygame
import random

# Initialize Pygame
pygame.init()

# Window dimensions
window_width = 700
window_height = 800
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Hangman Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 40)
input_font = pygame.font.Font(None, 30)

# Load the sound :
sound_winner = pygame.mixer.Sound('sounds/You_Win_Perfect.wav')
sound_loser = pygame.mixer.Sound('sounds/you_lost.wav')

# Load hangman images
hangman_images = [
    pygame.image.load("images/hangman_1.png"),
    pygame.image.load("images/hangman_2.png"),
    pygame.image.load("images/hangman_3.png"),
    pygame.image.load("images/hangman_4.png"),
    pygame.image.load("images/hangman_5.png"),
    pygame.image.load("images/hangman_6.png"),
    pygame.image.load("images/hangman_7.png"),
]

# Azerty keyboard layout
keyboard_layout = [
    "AZERTYUIOP",
    "QSDFGHJKLM",
    "WXCVBN"
]

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_keyboard(proposed_letters, guessed_letters, wrong_letters):
    start_x = window_width // 2 - 200
    start_y = window_height - 250
    key_size = 40
    key_gap = 10

    # Function to draw the keyboard on the screen
    for row_idx, row in enumerate(keyboard_layout):
        for col_idx, letter in enumerate(row):
            x = start_x + col_idx * (key_size + key_gap)
            y = start_y + row_idx * (key_size + key_gap)
            key_rect = pygame.Rect(x, y, key_size, key_size)

            # Set the key color based on the guess status
            if letter.lower() in guessed_letters:
                color = GREEN  # Correctly guessed letter
            elif letter.lower() in wrong_letters:
                color = RED  # Incorrectly guessed letter
            else:
                color = BLUE  # Default color for unguessed letters

            # Draw the button (rectangle)
            pygame.draw.rect(screen, color, key_rect)
            pygame.draw.rect(screen, BLACK, key_rect, 2)  # Border to make the keys look more defined

            # Draw the letter inside the key
            draw_text(letter.upper(), font, BLACK, screen, x + key_size // 2, y + key_size // 2)


# Function to display the main menu
def show_menu():
    screen.fill(WHITE)
    draw_text("--- Hangman Game ---", font, BLACK, screen, window_width // 2, window_height // 4)
    draw_text("1. Play", font, BLACK, screen, window_width // 2, window_height // 2 - 80)
    draw_text("2. Add a word", font, BLACK, screen, window_width // 2, window_height // 2 - 40)
    draw_text("3. View scores", font, BLACK, screen, window_width // 2, window_height // 2)
    draw_text("4. Delete all scores", font, BLACK, screen, window_width // 2, window_height // 2 + 40)
    draw_text("5. Quit", font, BLACK, screen, window_width // 2, window_height // 2 + 80)
    pygame.display.update()

# choose main option
def choose_menu():
    word_file = "words.txt"
    score_file = "scores.txt"

    while True:
        show_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    play_game(word_file, score_file)
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    add_word(word_file)
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    view_scores(score_file)
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    confirm_delete_scores(score_file)
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5 or event.key == pygame.K_RETURN:
                    confirm_quit()  # Call the confirmation dialog function 
                else:
                    print("Choose a valid option")

# Function to display the difficulty selection screen
def show_difficulty_screen():
    screen.fill(WHITE)
    draw_text("Select Difficulty:", font, BLACK, screen, window_width // 2, window_height // 4)
    draw_text("1. Easy", font, BLACK, screen, window_width // 2, window_height // 2 - 30)
    draw_text("2. Medium", font, BLACK, screen, window_width // 2, window_height // 2)
    draw_text("3. Hard", font, BLACK, screen, window_width // 2, window_height // 2 + 30)
    pygame.display.update()

# Function to choose difficulty
def choose_difficulty():
    show_difficulty_screen()
    difficulty = None
    while difficulty is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_e:
                    difficulty = "easy"
                elif event.key == pygame.K_2 or event.key == pygame.K_m:
                    difficulty = "medium"
                elif event.key == pygame.K_3 or event.key == pygame.K_h:
                    difficulty = "hard"
    return difficulty

# Function to get the player's name
def get_player_name():
    input_box = pygame.Rect(0, 0, 200, 40) 
    input_box.center = (window_width // 2, window_height // 2) 
    #input_box = pygame.Rect(window_width // 2 - 100, window_height // 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)

    while True:
        screen.fill(WHITE)
        draw_text("Enter your name:", font, BLACK, screen, window_width // 2, window_height // 3)
        pygame.draw.rect(screen, color, input_box, 2)
        draw_text(text, font, BLACK, screen, window_width // 2, window_height // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                    color = color_active
                else:
                    active = False
                    color = color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

# Function to load words from a file
def load_words(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: The file '{file}' was not found.")
        return []

# Function to choose a word based on difficulty
def choose_word(words, difficulty):
    if difficulty == "easy":
        filtered_words = [word for word in words if len(word) <= 6]
    elif difficulty == "medium":
        filtered_words = [word for word in words if 7 <= len(word) <= 9]
    elif difficulty == "hard":
        filtered_words = [word for word in words if len(word) > 9]
    else:
        filtered_words = words

    return random.choice(filtered_words)

# Function to update score in the score file
def update_score(score_file, player_name, score):
    # Read the existing scores from the file
    try:
        with open(score_file, 'r', encoding='utf-8') as f:
            scores = f.readlines()
    except FileNotFoundError:
        scores = []

    player_found = False

    # Check if the player already exists in the scores list
    for i, line in enumerate(scores):
        name, player_score = line.strip().split(": ")
        if name == player_name:
            # If the player is found, update their score
            new_score = int(player_score) + score
            scores[i] = f"{name}: {new_score}\n"
            player_found = True
            break

    # If the player is not found, add a new entry
    if not player_found:
        scores.append(f"{player_name}: {score}\n")

    # Write the updated scores back to the file
    with open(score_file, 'w', encoding='utf-8') as f:
        f.writelines(scores)

# Function to view the scores
def view_scores(score_file):
    screen.fill(WHITE)
    draw_text("Scores:", font, BLACK, screen, window_width // 2, 50)
    
    try:
        with open(score_file, 'r', encoding='utf-8') as f:
            scores = f.readlines()
            if not scores:
                draw_text("No scores available.", font, BLACK, screen, window_width // 2, window_height // 3)
            else:
                y_offset = 100
                for score in scores:
                    draw_text(score.strip(), font, BLACK, screen, window_width // 2, y_offset)
                    y_offset += 40
    except FileNotFoundError:
        draw_text(f"Error: {score_file} not found.", font, RED, screen, window_width // 2, window_height // 3)

    draw_text("Press any key to return.", font, BLACK, screen, window_width // 2, window_height - 50)
    pygame.display.update()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting_for_key = False

# Function to add a word to the word file
def add_word(word_file):
    input_box = pygame.Rect(0, 0, 200, 40) 
    input_box.center = (window_width // 2, window_height // 2) 
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)

    while True:
        screen.fill(WHITE)
        draw_text("Enter a new word:", font, BLACK, screen, window_width // 2, window_height // 3)
        pygame.draw.rect(screen, color, input_box, 2)
        draw_text(text, font, BLACK, screen, window_width // 2, window_height // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                    color = color_active
                else:
                    active = False
                    color = color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        with open(word_file, 'a', encoding='utf-8') as f:
                            f.write(f"{text}\n")
                        screen.fill(WHITE)
                        draw_text(f"Added word: {text}", font, GREEN, screen, window_width // 2, window_height // 2 + 40)
                        pygame.display.update()
                        pygame.time.delay(1000)
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

# Function to display the delete scores confirmation screen
def confirm_delete_scores(score_file):
    screen.fill(WHITE)
    draw_text("Do you really want to delete all scores?", font, BLACK, screen, window_width // 2, window_height // 3)
    draw_text("Press Y to confirm or N to cancel.", font, BLACK, screen, window_width // 2, window_height // 2)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # User confirms delete
                    with open(score_file, 'w', encoding='utf-8') as f:
                        f.truncate(0)  # Empty the file
                    screen.fill(WHITE)
                    draw_text("All scores deleted!", font, GREEN, screen, window_width // 2, window_height // 2)
                    pygame.display.update()
                    pygame.time.delay(2000)  # Show message for 2 seconds
                    return
                elif event.key == pygame.K_n:  # User cancels delete
                    screen.fill(WHITE)
                    draw_text("Scores not deleted.", font, RED, screen, window_width // 2, window_height // 2)
                    pygame.display.update()
                    pygame.time.delay(2000)  # Show message for 2 seconds
                    return

# Function to delete all scores
def delete_scores(score_file):
    print("Do you really want to delete all scores? (y/n): ")
    confirm = input().strip().lower()  # Ask for confirmation from the user
    
    if confirm == 'y':
        with open(score_file, 'w', encoding='utf-8') as f:
            f.truncate(0)  # Empty the file
        print("All scores deleted.")
    elif confirm == 'n':
        print("Scores not deleted.")
    else:
        print("Invalid choice. Please enter 'y' or 'n'.")

# Function to display the delete scores confirmation screen
def confirm_delete_scores(score_file):
    screen.fill(WHITE)
    draw_text("Do you really want to delete all scores?", font, BLACK, screen, window_width // 2, window_height // 3)
    draw_text("Press Y to confirm or N to cancel.", font, BLACK, screen, window_width // 2, window_height // 2)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # User confirms delete
                    with open(score_file, 'w', encoding='utf-8') as f:
                        f.truncate(0)  # Empty the file
                    screen.fill(WHITE)
                    draw_text("All scores deleted!", font, GREEN, screen, window_width // 2, window_height // 2)
                    pygame.display.update()
                    pygame.time.delay(2000)  # Show message for 2 seconds
                    return
                elif event.key == pygame.K_n:  # User cancels delete
                    screen.fill(WHITE)
                    draw_text("Scores not deleted.", font, RED, screen, window_width // 2, window_height // 2)
                    pygame.display.update()
                    pygame.time.delay(2000)  # Show message for 2 seconds
                    return

# Function to display the quit confirmation screen
def confirm_quit():
    screen.fill(WHITE)
    draw_text("Do you really want to quit?", font, BLACK, screen, window_width // 2, window_height // 3)
    draw_text("Press Y to confirm or N to cancel.", font, BLACK, screen, window_width // 2, window_height // 2)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # User confirms quit
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_n:  # User cancels quit
                    return  # Exit the confirmation screen and return to the menu

# Function to play game (the main loop of the game)
def play_game(word_file, score_file):
    words = load_words(word_file)
    if not words:
        print("No words available. Please add words to the file.")
        return

    difficulty = choose_difficulty()
    player_name = get_player_name()
    word_to_guess = choose_word(words, difficulty)
    guessed_letters = set()
    wrong_letters = set()  # Track incorrect guesses
    proposed_letters = set()  # Track all selected letters (both correct and incorrect)
    remaining_attempts = 6
    score = 0

    while remaining_attempts > 0:
        screen.fill(WHITE)

        # Draw player name and score
        draw_text(f"Player: {player_name}", font, BLACK, screen, window_width - 150, 30)
        draw_text(f"Score: {score}", font, BLACK, screen, window_width - 150, 70)

        # Draw hangman image
        screen.blit(hangman_images[6 - remaining_attempts], (window_width // 2 - 100, window_height // 4))

        # Draw the word to guess, showing guessed letters or underscores
        word_display = ' '.join([letter if letter.lower() in guessed_letters else '_' for letter in word_to_guess])
        draw_text(f"Word: {word_display}", font, BLACK, screen, window_width // 2, window_height // 2 + 40)

        # Draw the keyboard with updated colors for correct/incorrect letters
        draw_keyboard(proposed_letters, guessed_letters, wrong_letters)
        pygame.display.update()

        # Handle events
        selected_letter = None
        while selected_letter is None:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if pygame.K_a <= event.key <= pygame.K_z:
                        selected_letter = chr(event.key).upper()
                    elif event.key == pygame.K_RETURN:  # Check for Enter key to return to menu
                        return  # Return to the menu by exiting the current game loop

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    start_x = window_width // 2 - 200
                    start_y = window_height - 250
                    key_size = 40
                    key_gap = 10
                    for row_idx, row in enumerate(keyboard_layout):
                        for col_idx, letter in enumerate(row):
                            x = start_x + col_idx * (key_size + key_gap)
                            y = start_y + row_idx * (key_size + key_gap)
                            key_rect = pygame.Rect(x, y, key_size, key_size)
                            if key_rect.collidepoint(mouse_x, mouse_y):
                                selected_letter = letter.upper()
                                break

        if selected_letter in proposed_letters:
            continue

        proposed_letters.add(selected_letter)

        if selected_letter.lower() in word_to_guess.lower():
            guessed_letters.add(selected_letter.lower())  # Correct guess
            score += 10
        else:
            remaining_attempts -= 1
            score -= 10
            wrong_letters.add(selected_letter.lower())  # Incorrect guess

        # Check if the word is fully guessed
        if all(letter.lower() in guessed_letters for letter in word_to_guess.lower()):
            # Redraw everything before exiting the loop
            screen.fill(WHITE)
            draw_text(f"Player: {player_name}", font, BLACK, screen, window_width - 150, 30)
            draw_text(f"Score: {score}", font, BLACK, screen, window_width - 150, 70)
            screen.blit(hangman_images[6 - remaining_attempts], (window_width // 2 - 100, window_height // 4))
            word_display = ' '.join([letter if letter.lower() in guessed_letters else '_' for letter in word_to_guess])
            draw_text(f"Word: {word_display}", font, BLACK, screen, window_width // 2, window_height // 2 + 40)
            draw_keyboard(proposed_letters, guessed_letters, wrong_letters)
            draw_text(f"Congrats! You guessed the word: {word_to_guess}", font, GREEN, screen, window_width // 2, window_height // 2 + 100)
            sound_winner.play()
            pygame.time.wait(int(sound_winner.get_length() * 1000))
            pygame.display.update()
            pygame.time.delay(2000)
        
            break
    
    else:
        # Show the final hangman image
        screen.fill(WHITE)
        screen.blit(hangman_images[-1], (window_width // 2 - 100, window_height // 4))
        draw_text(f"You lost! The word was: {word_to_guess}", font, RED, screen, window_width // 2, window_height // 2 + 100)
        sound_loser.play()
        pygame.time.wait(int(sound_loser.get_length() * 1000))
        pygame.display.update()
        pygame.time.delay(2000)


    update_score(score_file, player_name, score)


try :
    if __name__ == "__main__":
        word_file = "words.txt"
        score_file = "score.txt"
        choose_menu()  
except KeyboardInterrupt :
    print(f"Exiting .....")
