import sys
import random
import math
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

# Court & play colors
WOOD_COLOR = (185, 145, 100)
LINE_COLOR = (255, 255, 255)

# Defensive play probabilities
BLOCK_PROB = {
    "3pt": 0.05,
    "dunk": 0.20,
    "layup": 0.25,
    "free_throw": 0.0,
}

# Generic steal probability before shot attempt
STEAL_PROB = 0.10

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


# ---------------------------------- Court ---------------------------------- #


def draw_court():
    """Render a simple basketball court."""
    SCREEN.fill(WOOD_COLOR)

    # Boundaries
    margin_x, margin_y = 80, 40
    court_rect = pygame.Rect(margin_x, margin_y, WIDTH - 2 * margin_x, HEIGHT - 2 * margin_y)
    pygame.draw.rect(SCREEN, LINE_COLOR, court_rect, 4)

    # Half-court line
    pygame.draw.line(SCREEN, LINE_COLOR, (WIDTH // 2, margin_y), (WIDTH // 2, HEIGHT - margin_y), 4)

    # Center circle
    pygame.draw.circle(SCREEN, LINE_COLOR, (WIDTH // 2, HEIGHT // 2), 60, 4)

    # The keys (paint)
    key_width, key_height = 160, 180
    left_key_rect = pygame.Rect(margin_x, HEIGHT // 2 - key_height // 2, key_width, key_height)
    right_key_rect = pygame.Rect(WIDTH - margin_x - key_width, HEIGHT // 2 - key_height // 2, key_width, key_height)
    pygame.draw.rect(SCREEN, LINE_COLOR, left_key_rect, 4)
    pygame.draw.rect(SCREEN, LINE_COLOR, right_key_rect, 4)

    # Three-point arcs (approximate with arcs)
    arc_radius = 240
    # Left arc
    left_arc_rect = pygame.Rect(margin_x - arc_radius // 2, HEIGHT // 2 - arc_radius // 2, arc_radius, arc_radius)
    pygame.draw.arc(SCREEN, LINE_COLOR, left_arc_rect, math.radians(300), math.radians(60), 4)
    # Right arc
    right_arc_rect = pygame.Rect(WIDTH - margin_x - arc_radius // 2, HEIGHT // 2 - arc_radius // 2, arc_radius, arc_radius)
    pygame.draw.arc(SCREEN, LINE_COLOR, right_arc_rect, math.radians(120), math.radians(240), 4)


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
    """Simulate a shot, factoring in steals and blocks.

    Returns (outcome: str, points_awarded: int) where outcome ∈ {"steal", "block", "miss", "made"}.
    """
    # Check for steal before shot
    if random.random() < STEAL_PROB:
        return "steal", 0

    # Check for block on the shot attempt
    if random.random() < BLOCK_PROB.get(shot_key, 0):
        return "block", 0

    # Determine if shot is made
    made = random.random() < NBA_PLAYERS[player_name][shot_key]
    if made:
        return "made", SHOT_TYPES[shot_key]["points"]
    else:
        return "miss", 0


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
        draw_court()

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
                    outcome, pts = attempt_shot(player_name, shot_type)

                    if outcome == "made":
                        score += pts
                        last_message = f"{SHOT_TYPES[shot_type]['label']} Made! +{pts}"
                    elif outcome == "miss":
                        last_message = f"Missed {SHOT_TYPES[shot_type]['label']}!"
                    elif outcome == "block":
                        last_message = "Shot Blocked!"
                    elif outcome == "steal":
                        last_message = "Ball Stolen!"

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