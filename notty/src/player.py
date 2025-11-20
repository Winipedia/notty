"""Player and Hand classes for the Notty game."""

import random

from notty.src.card import Card


class Hand:
    """Represents a player's hand of cards.

    Manages the collection of cards and enforces the 20-card limit.
    """

    MAX_CARDS = 20

    def __init__(self) -> None:
        """Initialize an empty hand."""
        self.cards: list[Card] = []

    def hand_is_full(self) -> bool:
        """Check if the hand is full.

        Returns:
            True if hand has reached the maximum number of cards.
        """
        return self.size() >= self.MAX_CARDS

    def add_card(self, card: Card, *, draw_discard_draw: bool = False) -> bool:
        """Add a card to the hand.

        Args:
            card: The card to add.
            draw_discard_draw: True if this is a draw and discard action.
                This is needed because in the draw and discard action, the player
                can draw even if hand is full.

        Returns:
            True if the card was added, False if hand is full.
        """
        if self.size() >= self.MAX_CARDS and not draw_discard_draw:
            return False
        self.cards.append(card)
        self.shuffle()
        return True

    def add_cards(self, cards: list[Card]) -> dict[Card, bool]:
        """Add multiple cards to the hand.

        Args:
            cards: List of cards to add.

        Returns:
            A dictionary mapping each card to a boolean indicating whether it was added.
        """
        cards_added: dict[Card, bool] = {}
        for card in cards:
            cards_added[card] = self.add_card(card)
        return cards_added

    def remove_card(self, card: Card) -> bool:
        """Remove a specific card from the hand.

        Args:
            card: The card to remove.

        Returns:
            True if the card was removed, False if card not in hand.
        """
        if card in self.cards:
            self.cards.remove(card)
            return True
        return False

    def remove_cards(self, cards: list[Card]) -> dict[Card, bool]:
        """Remove multiple cards from the hand.

        Args:
            cards: List of cards to remove.

        Returns:
            A dictionary mapping each card to a boolean showing whether it was removed.
        """
        cards_removed: dict[Card, bool] = {}
        for card in cards:
            cards_removed[card] = self.remove_card(card)
        return cards_removed

    def is_empty(self) -> bool:
        """Check if the hand is empty.

        Returns:
            True if hand has no cards.
        """
        return self.size() == 0

    def size(self) -> int:
        """Get the number of cards in the hand.

        Returns:
            Number of cards in hand.
        """
        return len(self.cards)

    def shuffle(self) -> None:
        """Shuffle the cards in the hand."""
        random.shuffle(self.cards)

    def __len__(self) -> int:
        """Return the number of cards in the hand."""
        return self.size()

    def __str__(self) -> str:
        """Return a string representation of the hand."""
        return f"{self.__class__.__name__}({self.size()} cards)"

    def __repr__(self) -> str:
        """Return a detailed string representation of the hand."""
        return f"{self.__class__.__name__}(cards={[str(card) for card in self.cards]})"


class Player:
    """Represents a player in the Notty game.

    Each player has a hand of cards and can be either human or computer-controlled.
    """

    TYPE_HUMAN = "human"
    TYPE_COMPUTER = "computer"

    def __init__(self, name: str, *, is_human: bool = False) -> None:
        """Initialize a player.

        Args:
            name: The player's name.
            is_human: True if this is a human player, False for computer.
        """
        self.name = name
        self.is_human = is_human
        self.hand = Hand()

    def __str__(self) -> str:
        """Return a string representation of the player."""
        player_type = self.TYPE_HUMAN if self.is_human else self.TYPE_COMPUTER
        return f"{player_type} Player: {self.name} ({len(self.hand)} cards)"

    def __repr__(self) -> str:
        """Return a detailed string representation of the player."""
        return f"{self.__class__.__name__}(name={self.name}, is_human={self.is_human})"
