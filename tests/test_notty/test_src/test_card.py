"""Test card module."""

from notty.src.card import Card, Color, Number


class TestColor:
    """Test Color class."""

    def test_get_all_colors(self) -> None:
        """Test getting all colors."""
        colors = Color.get_all_colors()
        for color in ["red", "green", "yellow", "black", "blue"]:
            assert color in colors


class TestNumber:
    """Test Number class."""

    def test_get_all_numbers(self) -> None:
        """Test getting all numbers."""
        numbers = Number.get_all_numbers()
        for i in range(1, 10):
            assert i in numbers


class TestCard:
    """Test Card class."""

    def test___delattr__(self) -> None:
        """Test card is frozen (cannot delete attributes)."""
        Card("red", 5)

    def test___eq__(self) -> None:
        """Test card equality."""
        card1 = Card("red", 5)
        card2 = Card("red", 5)
        assert card1 == card2

        card3 = Card("blue", 5)
        assert card1 != card3

    def test___hash__(self) -> None:
        """Test card is hashable."""
        card = Card("red", 5)
        assert isinstance(hash(card), int)

    def test___init__(self) -> None:
        """Test card initialization."""
        card = Card("red", 5)
        assert card.color == "red"
        expected = 5
        assert card.number == expected

    def test___setattr__(self) -> None:
        """Test card is frozen (cannot set attributes)."""
        Card("red", 5)

    def test___post_init__(self) -> None:
        """Test card validation."""
        Card("red", 5)

    def test___str__(self) -> None:
        """Test card string representation."""
        card = Card("red", 5)
        assert str(card) == "red 5"

    def test___repr__(self) -> None:
        """Test card repr."""
        card = Card("red", 5)
        assert "Card" in repr(card)
