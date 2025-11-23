"""visual card."""

from importlib import import_module
from types import ModuleType

import pygame

from notty.dev.artifacts.resources.visuals import cards
from notty.src.consts import CARD_HEIGHT, CARD_WIDTH
from notty.src.visual.base import Visual


class Color:
    """Color class for the Notty game."""

    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLACK = "black"
    BLUE = "blue"

    @classmethod
    def get_all_colors(cls) -> set[str]:
        """Get all colors."""
        return {cls.RED, cls.GREEN, cls.YELLOW, cls.BLACK, cls.BLUE}


class Number:
    """Number class for the Notty game."""

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9

    @classmethod
    def get_all_numbers(cls) -> range:
        """Get all numbers."""
        return range(1, 10)


class VisualCard(Visual):
    """Visual card."""

    def __init__(
        self,
        color: str,
        number: int,
        x: int,
        y: int,
        screen: pygame.Surface,
    ) -> None:
        """Initialize a visual card.

        Args:
            color: The color of the card.
            number: The number of the card.
            x: X coordinate. Always represents the top-left corner.
            y: Y coordinate. Always represents the top-left corner.
            height: Height of the visual element.
            width: Width of the visual element.
            screen: The pygame display surface.
        """
        self.color = color
        self.number = number
        super().__init__(x, y, CARD_HEIGHT, CARD_WIDTH, screen)

    def get_png_name(self) -> str:
        """Get the png for the visual element."""
        return f"{self.number}"

    def get_png_pkg(self) -> ModuleType:
        """Get the png for the visual element."""
        card_mod_name = cards.__name__ + "." + self.color
        return import_module(str(card_mod_name))
