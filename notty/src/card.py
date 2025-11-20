"""Card class for the Notty game."""

from dataclasses import dataclass


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


@dataclass(frozen=True)
class Card:
    """Represents a single card in the Notty game.

    Each card has a color and a number.
    Colors: red, green, yellow, black, blue
    Numbers: 1-9
    """

    color: str
    number: int

    def __post_init__(self) -> None:
        """Validate card attributes."""
        if self.color not in Color.get_all_colors():
            msg = (
                f"Invalid color: {self.color}. Must be one of {Color.get_all_colors()}"
            )
            raise ValueError(msg)

        if self.number not in Number.get_all_numbers():
            msg = f"Invalid number: {self.number}. Must be between 1 and 9"
            raise ValueError(msg)

    def __str__(self) -> str:
        """Return a string representation of the card."""
        return f"{self.color} {self.number}"

    def __repr__(self) -> str:
        """Return a detailed string representation of the card."""
        return f"{self.__class__.__name__}({self.color}, {self.number})"
