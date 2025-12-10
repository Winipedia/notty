"""visual game."""

import itertools
from types import ModuleType
from typing import cast

import pygame

from notty import resources
from notty.src.computer_action_selection import computer_chooses_action
from notty.src.consts import (
    APP_HEIGHT,
    APP_WIDTH,
    INITIAL_HAND_SIZE,
    MAX_HAND_SIZE,
    MAX_PLAYERS,
    MIN_PLAYERS,
    TOTAL_CARDS,
)
from notty.src.visual.action_board import Action, ActionBoard
from notty.src.visual.base import Visual
from notty.src.visual.card import VisualCard
from notty.src.visual.card_selector import CardSelector
from notty.src.visual.cards_selector import CardsSelector
from notty.src.visual.deck import VisualDeck
from notty.src.visual.number_selector import NumberSelector
from notty.src.visual.player import VisualPlayer
from notty.src.visual.player_selector import PlayerSelector


class VisualGame(Visual):
    """visual game class."""

    def __init__(
        self,
        screen: pygame.Surface,
        players: list[VisualPlayer],
    ) -> None:
        """Initialize a visual game.

        Args:
            players: List of players.
            screen: The pygame display surface.
        """
        super().__init__(0, 0, APP_HEIGHT, APP_WIDTH, screen)
        self.num_players = len(players)
        if not MIN_PLAYERS <= self.num_players <= MAX_PLAYERS:
            msg = f"""
            Game requires {MIN_PLAYERS}-{MAX_PLAYERS} players,
            got {self.num_players}
"""
            raise ValueError(msg)

        self.players = players
        self.deck = VisualDeck(screen=self.screen)
        self.current_player_index = 0
        self.winner: VisualPlayer | None = None

        # Track which actions have been used how many times
        self.actions_used: dict[str, int] = dict.fromkeys(Action.get_all_actions(), 0)

        # Create action board for human player
        self.action_board = self._create_action_board()

        # Track last computer action time (in milliseconds)
        self.last_computer_action_time = 0
        self.computer_action_delay = 1000  # 1 second in milliseconds

        self.setup()

    def draw(self) -> None:
        """Draw the game."""
        super().draw()
        self.deck.draw()
        for player in self.players:
            player.draw()
        self.draw_current_player_border()
        self.action_board.draw()

    def draw_current_player_border(self) -> None:
        """Draw a black rectangle around the current player's hand."""
        current_player = self.get_current_player()
        hand = current_player.hand

        # Draw a black rectangle border around the hand
        border_width = 5
        border_padding = 10

        pygame.draw.rect(
            self.screen,
            (0, 0, 0),  # Black color
            (
                hand.x - border_padding,
                hand.y - border_padding,
                hand.width + 2 * border_padding,
                hand.height + 2 * border_padding,
            ),
            border_width,
        )

    def get_png_name(self) -> str:
        """Get the png for the visual element."""
        return "icon"

    def get_png_pkg(self) -> ModuleType:
        """Get the png for the visual element."""
        return resources

    def setup(self) -> None:
        """Set up the game by shuffling deck and dealing initial cards."""
        # Shuffle deck before dealing
        self.deck.shuffle()

    def _create_action_board(self) -> "ActionBoard":
        """Create action board for the human player.

        Returns:
            ActionBoard instance if there's a human player, None otherwise.
        """
        # Find the human player index
        for i, player in enumerate(self.players):
            if player.is_human:
                return ActionBoard(self.screen, i, self)

        msg = "No human player found"
        raise ValueError(msg)

    def get_current_player(self) -> VisualPlayer:
        """Get the current player whose turn it is.

        Returns:
            The current player.
        """
        return self.players[self.current_player_index]

    def can_computer_act(self) -> bool:
        """Check if enough time has passed for computer to take an action.

        Returns:
            True if computer can act (1 second has passed since last action).
        """
        current_time = pygame.time.get_ticks()
        return (
            current_time - self.last_computer_action_time >= self.computer_action_delay
        )

    def mark_computer_action(self) -> None:
        """Mark that the computer has taken an action."""
        self.last_computer_action_time = pygame.time.get_ticks()

    def get_other_players(self) -> list[VisualPlayer]:
        """Get all players except the current player.

        Returns:
            List of other players.
        """
        return [p for i, p in enumerate(self.players) if i != self.current_player_index]

    def get_next_player(self) -> VisualPlayer:
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

        # check all player shave not more than MAX_HAND_SIZE cards
        for player in self.players:
            if player.hand.size() > MAX_HAND_SIZE:
                msg = "Hand size exceeded"
                raise ValueError(msg)
        # check total number of cards is 90
        total_cards = (
            sum(player.hand.size() for player in self.players) + self.deck.size()
        )
        if total_cards != TOTAL_CARDS:
            msg = "Total number of cards is not 90"
            raise ValueError(msg)

    def check_win_condition(self) -> bool:
        """Check if any player has won (empty hand).

        Returns:
            True if game is over, False otherwise.
        """
        for player in self.players:
            if player.hand.is_empty():
                self.winner = player
                return True
        return False

    def calculate_reward(self, player_index: int, action: str) -> float:
        """Calculate reward for Q-learning agent.

        Args:
            player_index: Index of the player who took the action.
            action: The action that was taken.

        Returns:
            Reward value for the action.
        """
        player = self.players[player_index]

        # Big reward for winning
        if player.hand.is_empty():
            return 100.0

        # Reward for discarding cards (reduces hand size)
        if action == Action.DISCARD_GROUP:
            return 10.0

        # Small penalty for drawing cards (increases hand size)
        if action in [Action.DRAW_MULTIPLE, Action.DRAW_DISCARD_DRAW]:
            return -0.5

        # Neutral for steal (takes from opponent)
        if action == Action.STEAL:
            return 0.5

        # Small penalty for passing (not making progress)
        if action == Action.NEXT_TURN:
            return -1.0

        # Default small penalty to encourage action
        return -0.1

    def player_can_pass(self) -> bool:
        """Check if current player can pass.

        Returns:
            True if action is available.
        """
        # player can always pass
        return True

    def player_passes(self) -> bool:
        """VisualPlayer passes.

        Returns:
            True if action was successful.
        """
        if not self.player_can_pass():
            msg = "Cannot pass"
            raise ValueError(msg)

        self.next_turn()
        return True

    def play_for_me(self) -> bool:
        """Let the computer play for the human player.

        Returns:
            True if action was successful.
        """
        current_player = self.get_current_player()
        # make current player a computer player
        current_player.is_human = False
        # play for the computer player
        computer_chooses_action(self)
        # make current player a human player
        current_player.is_human = True
        return True

    def player_can_draw_multiple(self) -> bool:
        """Check if current player can draw cards.

        Returns:
            True if action is available.
        """
        return (
            self.actions_used[Action.DRAW_MULTIPLE] < 1
            and not self.deck.is_empty()
            and not self.get_current_player().hand.hand_is_full()
        )

    def player_draws_multiple(self, count: int | None = None) -> bool:
        """VisualPlayer draws cards.

        Args:
            count: Number of cards to draw.

        Returns:
            True if action was successful.
        """
        if not self.player_can_draw_multiple():
            msg = "Cannot draw cards"
            raise ValueError(msg)

        if count is None:
            count = self.request_number_from_player()

        cards = self.deck.draw_cards(count)
        self.get_current_player().hand.add_cards(cards)
        self.actions_used[Action.DRAW_MULTIPLE] += 1
        return True

    def request_number_from_player(self) -> int:
        """Request a number from the player.

        Returns:
            The number requested.
        """
        current_player = self.get_current_player()
        if current_player.is_human:
            # Calculate how many cards can fit in the hand
            available_space = MAX_HAND_SIZE - current_player.hand.size()
            # Also limit by deck size
            max_drawable = min(available_space, self.deck.size(), 3)
            # Show number selector dialog for human player
            selector = NumberSelector(self.screen, max_number=max_drawable)
            return cast("int", (selector.show()))
        # For computer players, choose randomly
        msg = "Should not be reached"
        raise ValueError(msg)

    def player_can_steal(self) -> bool:
        """Check if current player can steal a card.

        Returns:
            True if action is available.
        """
        return (
            self.actions_used[Action.STEAL] < 1
            and any(not p.hand.is_empty() for p in self.get_other_players())
            and not self.get_current_player().hand.hand_is_full()
        )

    def player_steals(self, target_player: VisualPlayer | None = None) -> bool:
        """VisualPlayer steals a card from another player.

        Args:
            target_player: VisualPlayer to steal from.

        Returns:
            True if action was successful.
        """
        if not self.player_can_steal():
            msg = "Cannot steal card"
            raise ValueError(msg)

        if target_player is None:
            target_player = self.request_player_from_player()

        current_player = self.get_current_player()
        # target player shuffles their hand before giving up a card
        target_player.hand.shuffle()
        card = target_player.hand.cards.pop()
        current_player.hand.add_card(card)
        self.actions_used[Action.STEAL] += 1
        return True

    def request_player_from_player(self) -> VisualPlayer:
        """Request a player from the player.

        Returns:
            The player requested.
        """
        current_player = self.get_current_player()
        if current_player.is_human:
            # Show player selector dialog for human player

            other_players = self.get_other_players()
            selector = PlayerSelector(self.screen, other_players)
            return cast("VisualPlayer", (selector.show()))
        msg = "Should not be reached"
        raise ValueError(msg)

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
        """VisualPlayer draws one card and discards another.

        Returns:
            True if action was successful.
        """
        if not self.player_can_draw_discard_draw():
            msg = "Cannot do draw in action draw and discard"
            raise ValueError(msg)

        current_player = self.get_current_player()
        card = self.deck.draw_card()
        current_player.hand.add_card(card, draw_discard_draw=True)
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

    def player_draw_discard_discards(self, card: VisualCard | None = None) -> bool:
        """VisualPlayer discards two cards.

        Returns:
            True if action was successful.
        """
        if not self.player_can_draw_discard_discard():
            msg = "Cannot do discard in action draw and discard"
            raise ValueError(msg)

        if card is None:
            card = self.request_card_from_player()

        current_player = self.get_current_player()
        current_player.hand.remove_card(card)
        self.deck.add_card(card)
        self.actions_used[Action.DRAW_DISCARD_DISCARD] += 1
        return True

    def request_card_from_player(self) -> VisualCard:
        """Request a card from the player.

        Returns:
            The card requested.
        """
        current_player = self.get_current_player()
        if current_player.is_human:
            # Show card selector dialog for human player

            available_cards = current_player.hand.cards
            selector = CardSelector(self.screen, available_cards)
            return cast("VisualCard", (selector.show()))
        msg = "Should not be reached"
        raise ValueError(msg)

    def card_group_is_valid(self, cards: list[VisualCard]) -> bool:
        """Check if a group of cards is valid.

        Args:
            cards: List of cards to check.

        Returns:
            True if group is valid.
        """
        is_valid = False

        # order cards by number
        cards.sort(key=lambda card: card.number)

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

    def can_discard_group(self) -> bool:
        """Check if current player can discard a group of cards.

        Returns:
            True if action is available.
        """
        # go through all card combinations and check if any are valid
        for i in range(3, 5):
            for cards in itertools.combinations(
                self.get_current_player().hand.cards, i
            ):
                if self.card_group_is_valid(list(cards)):
                    return True
        return False

    def get_discardable_groups(self) -> list[list[VisualCard]]:
        """Get all discardable groups.

        Returns:
            List of discardable groups.
        """
        current_player = self.get_current_player()
        cards = current_player.hand.cards
        discardable_groups: list[list[VisualCard]] = []
        for i in range(3, len(cards) + 1):
            for cards_ in itertools.combinations(cards, i):
                if self.card_group_is_valid(list(cards_)):
                    discardable_groups.append(list(cards_))  # noqa: PERF401

        return discardable_groups

    def player_discards_group(self, cards: list[VisualCard] | None = None) -> bool:
        """VisualPlayer discards a group of cards.

        Args:
            cards: List of cards to discard.

        Returns:
            True if action was successful.
        """
        if cards is None:
            cards = self.request_cards_from_player()

        if not self.card_group_is_valid(cards):
            return False

        current_player = self.get_current_player()
        current_player.hand.remove_cards(cards)
        self.deck.add_cards(cards)
        return True

    def request_cards_from_player(self) -> list[VisualCard]:
        """Request cards from the player.

        Returns:
            The cards requested.
        """
        current_player = self.get_current_player()
        if current_player.is_human:
            # Show cards selector dialog for human player

            available_cards = current_player.hand.cards
            # Pass the validation function to check if selected cards form a valid group
            selector = CardsSelector(
                self.screen, available_cards, self.card_group_is_valid
            )
            return selector.show()
        msg = "Should not be reached"
        raise ValueError(msg)

    @classmethod
    def distribute_starting_cards(cls, game: "VisualGame") -> None:
        """Distribute starting cards to players."""
        for player in game.players:
            cards = game.deck.draw_cards(INITIAL_HAND_SIZE)
            player.hand.add_cards(cards)

    def all_players_have_no_cards(self) -> bool:
        """Check if all players have no cards."""
        return all(player.hand.is_empty() for player in self.players)

    def action_is_possible(self, action: str) -> bool:  # noqa: PLR0911
        """Check if an action is possible.

        Args:
            action: The action to check.

        Returns:
            True if action is possible.
        """
        # "Play for Me" is handled separately in the action board
        if action == Action.PLAY_FOR_ME:
            return True
        # make any button False except Draw discard discard
        # if Draw discard draw is 1 and Draw discard discard is 0
        if (
            self.actions_used[Action.DRAW_DISCARD_DRAW] == 1
            and self.actions_used[Action.DRAW_DISCARD_DISCARD] == 0
        ):
            return action == Action.DRAW_DISCARD_DISCARD
        if action == Action.DRAW_MULTIPLE:
            return self.player_can_draw_multiple()
        if action == Action.STEAL:
            return self.player_can_steal()
        if action == Action.DRAW_DISCARD_DRAW:
            return self.player_can_draw_discard_draw()
        if action == Action.DRAW_DISCARD_DISCARD:
            return self.player_can_draw_discard_discard()
        if action == Action.DISCARD_GROUP:
            return self.can_discard_group()
        if action == Action.NEXT_TURN:
            return self.player_can_pass()
        msg = f"Unknown action: {action}"
        raise ValueError(msg)

    def get_all_possible_actions(self) -> list[str]:
        """Get all possible actions.

        Returns:
            List of possible actions.
        """
        return [
            action
            for action in Action.get_all_actions()
            if self.action_is_possible(action)
        ]

    def do_action(  # noqa: PLR0911
        self,
        action: str,
        count: int | None = None,
        card: VisualCard | None = None,
        cards: list[VisualCard] | None = None,
        target_player: VisualPlayer | None = None,
    ) -> bool:
        """Do an action.

        Args:
            action: The action to do.
            count: Number of cards to draw (for draw multiple action).
            card: Card to discard (for draw discard discard action).
            cards: Cards to discard (for discard group action).
            target_player: Player to steal from (for steal action).

        Returns:
            True if action was successful.
        """
        if action == Action.PLAY_FOR_ME:
            return self.play_for_me()
        if action == Action.DRAW_MULTIPLE:
            return self.player_draws_multiple(count=count)
        if action == Action.STEAL:
            return self.player_steals(target_player=target_player)
        if action == Action.DRAW_DISCARD_DRAW:
            return self.player_draw_discard_draws()
        if action == Action.DRAW_DISCARD_DISCARD:
            return self.player_draw_discard_discards(card=card)
        if action == Action.DISCARD_GROUP:
            return self.player_discards_group(cards=cards)
        if action == Action.NEXT_TURN:
            return self.player_passes()
        msg = f"Unknown action: {action}"
        raise ValueError(msg)
