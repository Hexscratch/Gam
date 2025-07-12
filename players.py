import pygame

# Dictionary of NBA players and their shot success probabilities.
# Values represent estimated make percentages for various shot types.
NBA_PLAYERS = {
    "Stephen Curry": {
        "3pt": 0.47,
        "dunk": 0.15,
        "free_throw": 0.92,
        "layup": 0.65,
    },
    "LeBron James": {
        "3pt": 0.34,
        "dunk": 0.95,
        "free_throw": 0.74,
        "layup": 0.85,
    },
    "Kevin Durant": {
        "3pt": 0.38,
        "dunk": 0.70,
        "free_throw": 0.89,
        "layup": 0.80,
    },
    "Giannis Antetokounmpo": {
        "3pt": 0.29,
        "dunk": 0.98,
        "free_throw": 0.64,
        "layup": 0.90,
    },
    "James Harden": {
        "3pt": 0.36,
        "dunk": 0.40,
        "free_throw": 0.86,
        "layup": 0.75,
    },
}

# Metadata for each shot type.
SHOT_TYPES = {
    "3pt": {
        "points": 3,
        "color": (255, 215, 0),  # Gold
        "label": "3-Pointer",
    },
    "dunk": {
        "points": 2,
        "color": (255, 0, 0),  # Red
        "label": "Dunk",
    },
    "free_throw": {
        "points": 1,
        "color": (0, 255, 0),  # Green
        "label": "Free Throw",
    },
    "layup": {
        "points": 2,
        "color": (0, 0, 255),  # Blue
        "label": "Layup",
    },
}