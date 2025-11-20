"""Deck class for the Notty game."""

import random

from notty.src.card import Card, Color, Number


class Deck:
    """Represents the deck of cards in the Notty game.

    The deck contains 90 cards total:
    - 5 colors * 9 numbers * 2 duplicates = 90 cards
    """

    NUM_DUPLICATES = 2

    def __init__(self) -> None:
        """Initialize the deck with all 90 cards."""
        self.cards: list[Card] = []
        self._initialize_deck()

    def _initialize_deck(self) -> None:
        """Create all 90 cards (2 of each color-number combination)."""
        self.cards = []
        for color in Color.get_all_colors():
            for number in Number.get_all_numbers():
                for _ in range(self.NUM_DUPLICATES):
                    self.cards.append(Card(color, number))

    def shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def draw(self) -> Card:
        """Draw the top card from the deck.

        Returns:
            The top card, or raises ValueError if deck is empty.
        """
        if not self.cards:
            msg = "Cannot draw from an empty deck"
            raise ValueError(msg)
        return self.cards.pop()

    def draw_multiple(self, count: int) -> list[Card]:
        """Draw multiple cards from the deck.

        Args:
            count: Number of cards to draw.

        Returns:
            List of drawn cards (may be fewer than requested if deck runs out).
        """
        drawn_cards: list[Card] = []
        for _ in range(count):
            if self.is_empty():
                break
            card = self.draw()
            drawn_cards.append(card)
        return drawn_cards

    def add_cards(self, cards: list[Card]) -> None:
        """Add cards back to the deck (used when discarding).

        Args:
            cards: List of cards to add back to the deck.
        """
        for card in cards:
            self.add_card(card)

    def add_card(self, card: Card) -> None:
        """Add a single card back to the deck (used when discarding).

        Args:
            card: Card to add back to the deck.
        """
        self.cards.append(card)

    def is_empty(self) -> bool:
        """Check if the deck is empty.

        Returns:
            True if the deck has no cards, False otherwise.
        """
        return len(self.cards) == 0

    def size(self) -> int:
        """Get the number of cards in the deck.

        Returns:
            Number of cards currently in the deck.
        """
        return len(self.cards)

    def __len__(self) -> int:
        """Return the number of cards in the deck."""
        return len(self.cards)

    def __str__(self) -> str:
        """Return a string representation of the deck."""
        return f"{self.__class__.__name__}({len(self.cards)} cards)"

    def __repr__(self) -> str:
        """Return a detailed string representation of the deck."""
        return f"{self.__class__.__name__}(cards={len(self.cards)})"
