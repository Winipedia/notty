"""Test player module."""

from notty.src.card import Card
from notty.src.player import Hand, Player


class TestHand:
    """Test Hand class."""

    def test___init__(self) -> None:
        """Test hand initialization."""
        hand = Hand()
        assert hand.size() == 0

    def test_hand_is_full(self) -> None:
        """Test checking if hand is full."""
        hand = Hand()
        assert not hand.hand_is_full()
        for i in range(20):
            hand.add_card(Card("red", i % 9 + 1))
        assert hand.hand_is_full()

    def test_add_card(self) -> None:
        """Test adding a card."""
        hand = Hand()
        card = Card("red", 5)
        result = hand.add_card(card)
        assert result is True
        assert hand.size() == 1

    def test_add_cards(self) -> None:
        """Test adding multiple cards."""
        hand = Hand()
        cards = [Card("red", 1), Card("blue", 2)]
        results = hand.add_cards(cards)
        assert all(results.values())
        expected = 2
        assert hand.size() == expected

    def test_remove_card(self) -> None:
        """Test removing a card."""
        hand = Hand()
        card = Card("red", 5)
        hand.add_card(card)
        result = hand.remove_card(card)
        assert result is True
        assert hand.size() == 0

    def test_remove_cards(self) -> None:
        """Test removing multiple cards."""
        hand = Hand()
        cards = [Card("red", 1), Card("blue", 2)]
        hand.add_cards(cards)
        results = hand.remove_cards(cards)
        assert all(results.values())
        assert hand.size() == 0

    def test_is_empty(self) -> None:
        """Test checking if hand is empty."""
        hand = Hand()
        assert hand.is_empty()
        hand.add_card(Card("red", 1))
        assert not hand.is_empty()

    def test_size(self) -> None:
        """Test getting hand size."""
        hand = Hand()
        assert hand.size() == 0
        hand.add_card(Card("red", 1))
        assert hand.size() == 1

    def test_shuffle(self) -> None:
        """Test shuffling hand."""
        hand = Hand()
        for i in range(10):
            hand.add_card(Card("red", i % 9 + 1))
        hand.shuffle()
        expected = 10
        assert hand.size() == expected

    def test___len__(self) -> None:
        """Test len() on hand."""
        hand = Hand()
        assert len(hand) == 0

    def test___str__(self) -> None:
        """Test hand string representation."""
        hand = Hand()
        assert "0" in str(hand)

    def test___repr__(self) -> None:
        """Test hand repr."""
        hand = Hand()
        assert "Hand" in repr(hand)


class TestPlayer:
    """Test Player class."""

    def test___init__(self) -> None:
        """Test player initialization."""
        player = Player("Alice", is_human=True)
        assert player.name == "Alice"
        assert player.is_human is True

    def test___str__(self) -> None:
        """Test player string representation."""
        player = Player("Alice", is_human=True)
        assert "Alice" in str(player)

    def test___repr__(self) -> None:
        """Test player repr."""
        player = Player("Alice", is_human=True)
        assert "Player" in repr(player)
