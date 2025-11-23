"""Card selector dialog for choosing which card to discard."""

from typing import TYPE_CHECKING

import pygame

from notty.src.consts import APP_HEIGHT, APP_WIDTH
from notty.src.visual.base_selector import BaseSelector, SelectableButton

if TYPE_CHECKING:
    from notty.src.visual.card import VisualCard


class CardButton(SelectableButton["VisualCard"]):
    """Represents a clickable card button."""

    def __init__(  # noqa: PLR0913
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        card: "VisualCard",
        card_image: pygame.Surface,
    ) -> None:
        """Initialize a card button.

        Args:
            x: X coordinate of the button.
            y: Y coordinate of the button.
            width: Width of the button.
            height: Height of the button.
            card: The card this button represents.
            card_image: The image of the card.
        """
        super().__init__(
            x, y, width, height, card, card_image, enabled=True, selectable=False
        )
        self.card = card
        self.card_image = card_image

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the button.

        Args:
            screen: The pygame display surface.
        """
        # Determine border color based on state
        if self.hovered:
            border_color = (100, 200, 255)  # Light blue for hover
            border_width = 5
        else:
            border_color = (255, 255, 255)  # White
            border_width = 3

        # Draw border
        border_padding = 5
        pygame.draw.rect(
            screen,
            border_color,
            (
                self.x - border_padding,
                self.y - border_padding,
                self.width + 2 * border_padding,
                self.height + 2 * border_padding,
            ),
            border_width,
        )

        # Draw card image
        screen.blit(self.card_image, (self.x, self.y))


class CardSelector(BaseSelector["VisualCard"]):
    """Dialog for selecting a card to discard."""

    def __init__(
        self, screen: pygame.Surface, available_cards: list["VisualCard"]
    ) -> None:
        """Initialize the card selector.

        Args:
            screen: The pygame display surface.
            available_cards: List of cards that can be selected.
        """
        super().__init__(
            screen,
            title="Choose a card to discard",
            items=available_cards,
            max_selections=1,
        )

    def _get_button_dimensions(self) -> tuple[int, int, int]:
        """Get button dimensions (width, height, spacing).

        Returns:
            Tuple of (button_width, button_height, button_spacing).
        """
        card_width = int(APP_WIDTH * 0.05)  # 5% of screen width
        card_height = int(APP_HEIGHT * 0.11)  # 11% of screen height
        card_spacing = int(APP_WIDTH * 0.008)  # 0.8% of screen width
        return card_width, card_height, card_spacing

    def _get_dialog_dimensions(self) -> tuple[int, int]:
        """Get dialog dimensions.

        Returns:
            Tuple of (dialog_width, dialog_height).
        """
        dialog_width = int(APP_WIDTH * 0.61)  # 61% of screen width
        dialog_height = int(APP_HEIGHT * 0.48)  # 48% of screen height
        return dialog_width, dialog_height

    def _setup_buttons(self) -> None:
        """Set up the card buttons."""
        # Get button dimensions
        card_width, card_height, card_spacing = self._get_button_dimensions()
        max_cards_per_row = 10

        # Calculate how many rows we need
        num_cards = len(self.items)
        num_rows = (num_cards + max_cards_per_row - 1) // max_cards_per_row

        # Calculate starting position
        start_y = int(APP_HEIGHT // 2 - (num_rows * (card_height + card_spacing)) // 2)

        # Create buttons for each card
        for i, card in enumerate(self.items):
            row = i // max_cards_per_row
            col = i % max_cards_per_row
            cards_in_row = min(max_cards_per_row, num_cards - row * max_cards_per_row)
            row_width = cards_in_row * card_width + (cards_in_row - 1) * card_spacing
            start_x = int((APP_WIDTH - row_width) // 2)

            x = start_x + col * (card_width + card_spacing)
            y = start_y + row * (card_height + card_spacing)

            # Scale card image
            card_image = pygame.transform.scale(card.png, (card_width, card_height))
            button = CardButton(x, y, card_width, card_height, card, card_image)
            self.buttons.append(button)
