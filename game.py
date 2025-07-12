import sys
import random
import pygame

from players import NBA_PLAYERS, SHOT_TYPES

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NBA Shot Challenge")

# Fonts
TITLE_FONT = pygame.font.SysFont("Arial", 48, bold=True)
TEXT_FONT = pygame.font.SysFont("Arial", 28)
SMALL_FONT = pygame.font.SysFont("Arial", 22)

# Game states
STATE_SELECT = "select"
STATE_PLAY = "play"

CLOCK = pygame.time.Clock()
FPS = 60

BACKGROUND_COLOR = (30, 30, 30)
WHITE = (255, 255, 255)

KEY_MAPPINGS = [
    pygame.K_1,
    pygame.K_2,
    pygame.K_3,
    pygame.K_4,
    pygame.K_5,
    pygame.K_6,
    pygame.K_7,
    pygame.K_8,
    pygame.K_9,
]


def draw_text(text, font, color, x, y, center=False):
    """Render text on the screen at (x, y)."""
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    SCREEN.blit(img, rect)


def select_player_screen():
    """Handle player selection UI and return selected player's name or None."""
    SCREEN.fill(BACKGROUND_COLOR)
    draw_text("Select Your Player", TITLE_FONT, WHITE, WIDTH // 2, 60, center=True)

    for idx, name in enumerate(NBA_PLAYERS.keys(), start=1):
        y_pos = 140 + (idx - 1) * 40
        key_name = str(idx)
        color = WHITE
        draw_text(f"[{key_name}] {name}", TEXT_FONT, color, 120, y_pos)

    draw_text("Press number key to choose player", SMALL_FONT, WHITE, WIDTH // 2, HEIGHT - 60, center=True)

    pygame.display.flip()

    # Event loop for selection
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # Map numeric keys to indices
                if event.key in KEY_MAPPINGS:
                    idx = KEY_MAPPINGS.index(event.key) + 1
                    if 1 <= idx <= len(NBA_PLAYERS):
                        return list(NBA_PLAYERS.keys())[idx - 1]
        CLOCK.tick(FPS)


def attempt_shot(player_name, shot_key):
    """Return (success: bool, points_awarded: int)."""
    prob = NBA_PLAYERS[player_name][shot_key]
    result = random.random() < prob
    points = SHOT_TYPES[shot_key]["points"] if result else 0
    return result, points


def play_game(player_name):
    score = 0
    last_message = ""
    message_timer = 0  # frames remaining to display message

    shot_keys = ["3pt", "dunk", "free_throw", "layup"]
    key_binding = {
        pygame.K_1: "3pt",
        pygame.K_2: "dunk",
        pygame.K_3: "free_throw",
        pygame.K_4: "layup",
    }

    running = True
    while running:
        SCREEN.fill(BACKGROUND_COLOR)

        # Draw UI
        draw_text(f"Player: {player_name}", TEXT_FONT, WHITE, 40, 20)
        draw_text(f"Score: {score}", TEXT_FONT, WHITE, WIDTH - 200, 20)

        # Shot instructions
        for i, shot in enumerate(shot_keys, start=1):
            color = SHOT_TYPES[shot]["color"]
            label = SHOT_TYPES[shot]["label"]
            draw_text(f"[{i}] {label}", TEXT_FONT, color, 60, 120 + (i - 1) * 40)

        draw_text("Press R to reset score  |  Esc to quit", SMALL_FONT, WHITE, WIDTH // 2, HEIGHT - 40, center=True)

        # Display result message
        if message_timer > 0:
            draw_text(last_message, TITLE_FONT, WHITE, WIDTH // 2, HEIGHT // 2, center=True)
            message_timer -= 1

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    score = 0
                if event.key in key_binding:
                    shot_type = key_binding[event.key]
                    success, pts = attempt_shot(player_name, shot_type)
                    if success:
                        score += pts
                        last_message = f"{SHOT_TYPES[shot_type]['label']}! +{pts}"
                    else:
                        last_message = f"Missed {SHOT_TYPES[shot_type]['label']}!"
                    message_timer = FPS  # message lasts 1 second

        CLOCK.tick(FPS)

    # End of play session
    pygame.quit()
    sys.exit()


def main():
    while True:
        selected = select_player_screen()
        play_game(selected)


if __name__ == "__main__":
    main()