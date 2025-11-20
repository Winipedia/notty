"""Test deck module."""

from notty.src.card import Card
from notty.src.deck import Deck


class TestDeck:
    """Test Deck class."""

    def test___init__(self) -> None:
        """Test deck initialization."""
        deck = Deck()
        expected = 5 * 9 * 2
        assert deck.size() == expected

    def test__initialize_deck(self) -> None:
        """Test deck has correct cards."""
        deck = Deck()
        expected = 5 * 9 * 2
        assert len(deck.cards) == expected

    def test_shuffle(self) -> None:
        """Test deck shuffle."""
        deck = Deck()
        original = deck.cards.copy()
        deck.shuffle()
        assert deck.cards != original

    def test_draw(self) -> None:
        """Test drawing a card."""
        deck = Deck()
        card = deck.draw()
        assert isinstance(card, Card)
        expected = 5 * 9 * 2 - 1
        assert deck.size() == expected

    def test_draw_multiple(self) -> None:
        """Test drawing multiple cards."""
        deck = Deck()
        cards = deck.draw_multiple(3)
        expected_num_drawn = 3
        assert len(cards) == expected_num_drawn
        expected_remaining = 5 * 9 * 2 - expected_num_drawn
        assert deck.size() == expected_remaining

    def test_add_cards(self) -> None:
        """Test adding multiple cards."""
        deck = Deck()
        cards = deck.draw_multiple(5)
        deck.add_cards(cards)
        expected = 5 * 9 * 2
        assert deck.size() == expected

    def test_add_card(self) -> None:
        """Test adding a single card."""
        deck = Deck()
        card = deck.draw()
        deck.add_card(card)
        expected = 5 * 9 * 2
        assert deck.size() == expected

    def test_is_empty(self) -> None:
        """Test checking if deck is empty."""
        deck = Deck()
        assert not deck.is_empty()
        deck.draw_multiple(90)
        assert deck.is_empty()

    def test_size(self) -> None:
        """Test getting deck size."""
        deck = Deck()
        expected = 5 * 9 * 2
        assert deck.size() == expected

    def test___len__(self) -> None:
        """Test len() on deck."""
        deck = Deck()
        expected = 5 * 9 * 2
        assert len(deck) == expected

    def test___str__(self) -> None:
        """Test deck string representation."""
        deck = Deck()
        assert "90" in str(deck)

    def test___repr__(self) -> None:
        """Test deck repr."""
        deck = Deck()
        assert "Deck" in repr(deck)
