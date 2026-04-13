"""Shared constants with accessible color palettes."""

from typing import List

# Facility Types
FOOD: str = "Food 🍔"
RESTROOM: str = "Restroom 🚻"
EXIT: str = "Exit 🚪"

FACILITIES: List[str] = [FOOD, RESTROOM, EXIT]

# Simulation Constants
DEFAULT_NUM_USERS: int = 200
DEFAULT_TIME_STEPS: int = 60
DEFAULT_SERVICE_RATE: float = 0.5

# Accessibility-focused Colors (High Contrast)
COLOR_GO_NOW: str = "#1B5E20"  # Dark Green (WCAG Compliant)
COLOR_WAIT: str = "#F57F17"    # Darker Yellow/Orange (WCAG Compliant)
COLOR_TEXT_SECONDARY: str = "#424242"
