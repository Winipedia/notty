"""Game class for the Notty game."""

import itertools

from notty.src.card import Card
from notty.src.deck import Deck
from notty.src.player import Player


class Action:
    """Represents an action in the Notty game."""

    DRAW = "draw"
    STEAL = "steal"
    DRAW_DISCARD_DRAW = "draw_discard_draw"
    DRAW_DISCARD_DISCARD = "draw_discard_discard"

    @classmethod
    def get_all_actions(cls) -> set[str]:
        """Get all actions."""
        return {cls.DRAW, cls.STEAL, cls.DRAW_DISCARD_DRAW, cls.DRAW_DISCARD_DISCARD}


class Game:
    """Represents a Notty game session.

    Manages the game state, players, deck, and turn-taking.
    """

    MIN_PLAYERS = 2
    MAX_PLAYERS = 3
    INITIAL_HAND_SIZE = 4

    def __init__(self, players: list[Player]) -> None:
        """Initialize a new game.

        Args:
            players: List of 2-3 players.

        Raises:
            ValueError: If number of players is not 2 or 3.
        """
        self.num_players = len(players)
        if not self.MIN_PLAYERS <= self.num_players <= self.MAX_PLAYERS:
            msg = f"""
            Game requires {self.MIN_PLAYERS}-{self.MAX_PLAYERS} players,
            got {self.num_players}
"""
            raise ValueError(msg)

        self.players = players
        self.deck = Deck()
        self.current_player_index = 0
        self.winner: Player | None = None
        self.game_over = False

        # Track which actions have been used how many times
        self.actions_used: dict[str, int] = dict.fromkeys(Action.get_all_actions(), 0)

        self.setup()

    def setup(self) -> None:
        """Set up the game by shuffling deck and dealing initial cards."""
        # Shuffle deck before dealing
        self.deck.shuffle()

        # Deal initial cards to each player
        for player in self.players:
            cards = self.deck.draw_multiple(self.INITIAL_HAND_SIZE)
            player.hand.add_cards(cards)

    def get_current_player(self) -> Player:
        """Get the current player whose turn it is.

        Returns:
            The current player.
        """
        return self.players[self.current_player_index]

    def get_other_players(self) -> list[Player]:
        """Get all players except the current player.

        Returns:
            List of other players.
        """
        return [p for i, p in enumerate(self.players) if i != self.current_player_index]

    def get_next_player(self) -> Player:
        """Get the next player.

        Returns:
            The next player.
        """
        return self.players[(self.current_player_index + 1) % len(self.players)]

    def get_next_player_index(self) -> int:
        """Get the index of the next player.

        Returns:
            The index of the next player.
        """
        return (self.current_player_index + 1) % len(self.players)

    def next_turn(self) -> None:
        """Move to the next player's turn."""
        self.current_player_index = self.get_next_player_index()

        # Reset action tracking for new turn
        self.actions_used = dict.fromkeys(Action.get_all_actions(), False)

    def check_win_condition(self) -> bool:
        """Check if any player has won (empty hand).

        Returns:
            True if game is over, False otherwise.
        """
        for player in self.players:
            if player.hand.is_empty():
                self.winner = player
                self.game_over = True
                return True
        return False

    def player_can_pass(self) -> bool:
        """Check if current player can pass.

        Returns:
            True if action is available.
        """
        # player can always pass
        return True

    def player_passes(self) -> bool:
        """Player passes.

        Returns:
            True if action was successful.
        """
        if not self.player_can_pass():
            msg = "Cannot pass"
            raise ValueError(msg)

        self.next_turn()
        return True

    def player_can_draw_multiple(self) -> bool:
        """Check if current player can draw cards.

        Returns:
            True if action is available.
        """
        return (
            self.actions_used[Action.DRAW] < 1
            and not self.deck.is_empty()
            and not self.get_current_player().hand.hand_is_full()
        )

    def player_draws_multiple(self, count: int) -> bool:
        """Player draws cards.

        Args:
            count: Number of cards to draw.

        Returns:
            True if action was successful.
        """
        if not self.player_can_draw_multiple():
            msg = "Cannot draw cards"
            raise ValueError(msg)

        cards = self.deck.draw_multiple(count)
        self.get_current_player().hand.add_cards(cards)
        self.actions_used[Action.DRAW] += 1
        return True

    def player_can_steal(self) -> bool:
        """Check if current player can steal a card.

        Returns:
            True if action is available.
        """
        return self.actions_used[Action.STEAL] < 1 and any(
            not p.hand.is_empty() for p in self.get_other_players()
        )

    def player_steals(self, target_player: Player) -> bool:
        """Player steals a card from another player.

        Args:
            target_player: Player to steal from.

        Returns:
            True if action was successful.
        """
        if not self.player_can_steal():
            msg = "Cannot steal card"
            raise ValueError(msg)

        current_player = self.get_current_player()
        # target player shuffles their hand before giving up a card
        target_player.hand.shuffle()
        card = target_player.hand.cards.pop()
        # draw_discard_draw is True in case hand is full
        current_player.hand.add_card(card, draw_discard_draw=True)
        self.actions_used[Action.STEAL] += 1
        return True

    def player_can_draw_discard_draw(self) -> bool:
        """Check if current player can draw and discard a card.

        Returns:
            True if action is available.
        """
        #  can draw even with full hand bc discard must happen after
        return (
            self.actions_used[Action.DRAW_DISCARD_DRAW] < 1 and not self.deck.is_empty()
        )

    def player_draw_discard_draws(self) -> bool:
        """Player draws one card and discards another.

        Returns:
            True if action was successful.
        """
        if not self.player_can_draw_discard_draw():
            msg = "Cannot do draw in action draw and discard"
            raise ValueError(msg)

        current_player = self.get_current_player()
        card = self.deck.draw()
        current_player.hand.add_card(card)
        self.actions_used[Action.DRAW_DISCARD_DRAW] += 1
        return True

    def player_can_draw_discard_discard(self) -> bool:
        """Check if current player can draw and discard two cards.

        Returns:
            True if action is available.
        """
        return (
            self.actions_used[Action.DRAW_DISCARD_DISCARD] < 1
            and self.actions_used[Action.DRAW_DISCARD_DRAW] == 1
        )

    def player_draw_discard_discards(self, card: Card) -> bool:
        """Player discards two cards.

        Returns:
            True if action was successful.
        """
        if not self.player_can_draw_discard_discard():
            msg = "Cannot do discard in action draw and discard"
            raise ValueError(msg)

        current_player = self.get_current_player()
        current_player.hand.remove_card(card)
        self.deck.add_card(card)
        self.actions_used[Action.DRAW_DISCARD_DISCARD] += 1
        return True

    def card_group_is_valid(self, cards: list[Card]) -> bool:
        """Check if a group of cards is valid.

        Args:
            cards: List of cards to check.

        Returns:
            True if group is valid.
        """
        is_valid = False

        numbers = [card.number for card in cards]
        colors = [card.color for card in cards]
        one_color = len(set(colors)) == 1
        unique_colors = len(set(colors)) == len(colors)
        consecutive_numbers = all(b - a == 1 for a, b in itertools.pairwise(numbers))
        one_number = len(set(numbers)) == 1

        # A sequence of at least three cards of the same colour
        # with consecutive numbers (e.g. blue 4, blue 5 and blue 6)
        min_cards = 3
        if len(cards) >= min_cards and one_color and consecutive_numbers:
            is_valid = True

        # A set of at least four cards of the same number
        # but different colours (e.g. blue 4, green 4 and red 4).
        # Note that no repeated colours are allowed in this type of group
        # (e.g. blue 4, red 4 and blue 4 is not a valid group)
        min_cards = 4
        if len(cards) >= min_cards and unique_colors and one_number:
            is_valid = True

        return is_valid

    def player_discards_group(self, cards: list[Card]) -> bool:
        """Player discards a group of cards.

        Args:
            cards: List of cards to discard.

        Returns:
            True if action was successful.
        """
        if not self.card_group_is_valid(cards):
            return False

        current_player = self.get_current_player()
        current_player.hand.remove_cards(cards)
        self.deck.add_cards(cards)
        return True

    def __str__(self) -> str:
        """Return a string representation of the game."""
        return f"{self.__class__.__name__}({len(self.players)}) players"

    def __repr__(self) -> str:
        """Return a detailed string representation of the game."""
        return f"{self.__class__.__name__}(players={[p.name for p in self.players]})"
