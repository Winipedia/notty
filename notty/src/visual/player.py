"""visual player."""

import random
from importlib import resources
from types import ModuleType
from typing import ClassVar

import pygame

from notty.resources.visuals import hand, players
from notty.src.consts import (
    APP_HEIGHT,
    APP_WIDTH,
    CARD_HEIGHT,
    CARD_WIDTH,
    HAND_HEIGHT,
    HAND_WIDTH,
    MAX_HAND_SIZE,
    MAX_PLAYERS,
    NUM_HAND_COLUMNS,
    NUM_HAND_ROWS,
    PLAYER_HEIGHT,
    PLAYER_WIDTH,
)
from notty.src.visual.base import Visual
from notty.src.visual.card import VisualCard


class VisualHand(Visual):
    """Represents a player's hand of cards.

    Manages the collection of cards and enforces the 20-card limit.
    """

    def __init__(self, player: "VisualPlayer") -> None:
        """Initialize an empty hand."""
        self.player = player
        # x, y are dependent on players position
        x, y = player.x, player.y
        # make x is the same but y must be 5 times above the player
        y -= NUM_HAND_ROWS * CARD_HEIGHT
        super().__init__(
            x,
            y,
            HAND_HEIGHT,
            HAND_WIDTH,
            player.screen,
        )
        self.cards: list[VisualCard] = []

    def draw(self) -> None:
        """Draw the hand."""
        super().draw()
        for card in self.cards:
            card.draw()

    def get_png_name(self) -> str:
        """Get the png for the visual element."""
        return "hand"

    def get_png_pkg(self) -> ModuleType:
        """Get the png for the visual element."""
        return hand

    def hand_is_full(self) -> bool:
        """Check if the hand is full.

        Returns:
            True if hand has reached the maximum number of cards.
        """
        return self.size() >= MAX_HAND_SIZE

    def add_card(self, card: VisualCard, *, draw_discard_draw: bool = False) -> bool:
        """Add a card to the hand.

        Args:
            card: The card to add.
            draw_discard_draw: True if this is a draw and discard action.
                This is needed because in the draw and discard action, the player
                can draw even if hand is full.

        Returns:
            True if the card was added, False if hand is full.
        """
        if self.size() >= MAX_HAND_SIZE and not draw_discard_draw:
            msg = "Hand is full"
            raise ValueError(msg)
        self.cards.append(card)
        self.order_cards()
        return True

    def add_cards(self, cards: list[VisualCard]) -> dict[VisualCard, bool]:
        """Add multiple cards to the hand.

        Args:
            cards: List of cards to add.

        Returns:
            A dictionary mapping each card to a boolean indicating whether it was added.
        """
        cards_added: dict[VisualCard, bool] = {}
        for card in cards:
            cards_added[card] = self.add_card(card)
        return cards_added

    def remove_card(self, card: VisualCard) -> bool:
        """Remove a specific card from the hand.

        Args:
            card: The card to remove.

        Returns:
            True if the card was removed, False if card not in hand.
        """
        if card in self.cards:
            self.cards.remove(card)
            # reposition all cards in hand
            self.order_cards()
            return True
        return False

    def order_cards(self) -> None:
        """Order the cards in the hand."""
        self.cards.sort(key=lambda card: (card.color, card.number))
        for i, card in enumerate(self.cards):
            row = i // NUM_HAND_COLUMNS
            col = i % NUM_HAND_COLUMNS
            card_x = self.x + col * CARD_WIDTH
            card_y = self.y + row * CARD_HEIGHT
            card.move(card_x, card_y)

    def remove_cards(self, cards: list[VisualCard]) -> dict[VisualCard, bool]:
        """Remove multiple cards from the hand.

        Args:
            cards: List of cards to remove.

        Returns:
            A dictionary mapping each card to a boolean showing whether it was removed.
        """
        cards_removed: dict[VisualCard, bool] = {}
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


class VisualPlayer(Visual):
    """Visual player."""

    ACTIVE_PLAYERS: ClassVar[list["VisualPlayer"]] = []

    TYPE_HUMAN = "human"
    TYPE_COMPUTER = "computer"

    def __init__(
        self,
        name: str,
        *,
        is_human: bool = False,
        screen: pygame.Surface,
    ) -> None:
        """Initialize a visual player."""
        VisualPlayer.ACTIVE_PLAYERS.append(self)
        self.name = name
        self.is_human = is_human
        x, y = self.get_coordinates()
        super().__init__(x, y, PLAYER_HEIGHT, PLAYER_WIDTH, screen)
        self.hand = VisualHand(player=self)

    def draw(self) -> None:
        """Draw the player."""
        super().draw()
        self.hand.draw()

    def get_png_name(self) -> str:
        """Get the png for the visual element."""
        return self.name

    def get_png_pkg(self) -> ModuleType:
        """Get the png for the visual element."""
        return players

    def get_coordinates(self) -> tuple[int, int]:
        """Get the coordinates for the player."""
        # make all xy dependent on APP_WIDTH and APP_HEIGHT
        y = APP_HEIGHT - PLAYER_HEIGHT
        # make position dependent on number of players
        # and index of player
        num_players = MAX_PLAYERS

        index = VisualPlayer.ACTIVE_PLAYERS.index(self)

        # Divide screen into equal spaces and center each player in their space
        player_space_width = APP_WIDTH // num_players

        # Center the player in their allocated space
        x = index * player_space_width

        return x, y

    @classmethod
    def get_all_player_names(cls) -> list[str]:
        """Get all player names."""
        # use importlib resources to gte all files in players package
        # that end with .png

        return [
            f.name.removesuffix(".png")
            for f in resources.files(players).iterdir()
            if f.name.endswith(".png")
        ]
