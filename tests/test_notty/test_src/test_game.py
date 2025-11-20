"""Test game module."""

from notty.src.card import Card
from notty.src.game import Action, Game
from notty.src.player import Player


class TestAction:
    """Test Action class."""

    def test_get_all_actions(self) -> None:
        """Test getting all actions."""
        actions = Action.get_all_actions()
        expected = {
            Action.DRAW,
            Action.STEAL,
            Action.DRAW_DISCARD_DRAW,
            Action.DRAW_DISCARD_DISCARD,
        }
        assert len(actions) == len(expected)
        assert actions == expected


class TestGame:
    """Test Game class."""

    def test___init__(self) -> None:
        """Test game initialization."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        expected = 2
        assert len(game.players) == expected

    def test_setup(self) -> None:
        """Test game setup."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        expected = 4
        assert game.players[0].hand.size() == expected

    def test_get_current_player(self) -> None:
        """Test getting current player."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        assert game.get_current_player() == players[0]

    def test_get_other_players(self) -> None:
        """Test getting other players."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        others = game.get_other_players()
        assert len(others) == 1

    def test_get_next_player(self) -> None:
        """Test getting next player."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        next_player = game.get_next_player()
        assert next_player == players[1]

    def test_get_next_player_index(self) -> None:
        """Test getting next player index."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        assert game.get_next_player_index() == 1

    def test_next_turn(self) -> None:
        """Test advancing to next turn."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        game.next_turn()
        assert game.current_player_index == 1

    def test_check_win_condition(self) -> None:
        """Test checking win condition."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        assert game.check_win_condition() is False
        # remove all cards from one player
        game.players[0].hand.cards = []
        assert game.check_win_condition() is True

    def test_player_can_pass(self) -> None:
        """Test if player can pass."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        assert game.player_can_pass() is True

    def test_player_passes(self) -> None:
        """Test player passing."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        game.player_passes()
        assert game.current_player_index == 1

    def test_player_can_draw_multiple(self) -> None:
        """Test if player can draw multiple."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        assert game.player_can_draw_multiple() is True

    def test_player_draws_multiple(self) -> None:
        """Test player drawing multiple cards."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        game.player_draws_multiple(2)
        expected = 6
        assert game.players[0].hand.size() == expected

    def test_player_can_steal(self) -> None:
        """Test if player can steal."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        assert game.player_can_steal() is True

    def test_player_steals(self) -> None:
        """Test player stealing."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        game.player_steals(players[1])
        expected = 5
        assert game.players[0].hand.size() == expected

    def test_player_can_draw_discard_draw(self) -> None:
        """Test if player can draw for draw-discard."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        assert game.player_can_draw_discard_draw() is True

    def test_player_draw_discard_draws(self) -> None:
        """Test player drawing for draw-discard."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        game.player_draw_discard_draws()
        expected = 5
        assert game.players[0].hand.size() == expected

    def test_player_can_draw_discard_discard(self) -> None:
        """Test if player can discard for draw-discard."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        game.player_draw_discard_draws()
        assert game.player_can_draw_discard_discard() is True

    def test_player_draw_discard_discards(self) -> None:
        """Test player discarding for draw-discard."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        game.player_draw_discard_draws()
        card = game.players[0].hand.cards[0]
        game.player_draw_discard_discards(card)
        expected = 4
        assert game.players[0].hand.size() == expected

    def test_card_group_is_valid(self) -> None:
        """Test validating card groups."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        cards = [Card("red", 1), Card("red", 2), Card("red", 3)]
        assert game.card_group_is_valid(cards) is True

    def test_player_discards_group(self) -> None:
        """Test player discarding a group."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        cards = [Card("red", 1), Card("red", 2), Card("red", 3)]
        game.players[0].hand.add_cards(cards)
        game.player_discards_group(cards)
        expected = 4
        assert game.players[0].hand.size() == expected

    def test___str__(self) -> None:
        """Test game string representation."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        assert Game.__name__ in str(game)

    def test___repr__(self) -> None:
        """Test game repr."""
        players = [Player("P1", is_human=True), Player("P2", is_human=False)]
        game = Game(players)
        assert "Game" in repr(game)
