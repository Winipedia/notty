"""Card selector dialog for choosing which card to discard."""

from typing import TYPE_CHECKING

import pygame

from notty.src.consts import ANTI_ALIASING, APP_HEIGHT, APP_WIDTH

if TYPE_CHECKING:
    from notty.src.visual.card import VisualCard


class CardButton:
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
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.card = card
        self.card_image = card_image
        self.hovered = False

    def is_clicked(self, mouse_x: int, mouse_y: int) -> bool:
        """Check if the button was clicked.

        Args:
            mouse_x: Mouse x coordinate.
            mouse_y: Mouse y coordinate.

        Returns:
            True if the button was clicked.
        """
        return (
            self.x <= mouse_x <= self.x + self.width
            and self.y <= mouse_y <= self.y + self.height
        )

    def update_hover(self, mouse_x: int, mouse_y: int) -> None:
        """Update hover state based on mouse position.

        Args:
            mouse_x: Mouse x coordinate.
            mouse_y: Mouse y coordinate.
        """
        self.hovered = (
            self.x <= mouse_x <= self.x + self.width
            and self.y <= mouse_y <= self.y + self.height
        )

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


class CardSelector:
    """Dialog for selecting a card to discard."""

    def __init__(
        self, screen: pygame.Surface, available_cards: list["VisualCard"]
    ) -> None:
        """Initialize the card selector.

        Args:
            screen: The pygame display surface.
            available_cards: List of cards that can be selected.
        """
        self.screen = screen
        self.available_cards = available_cards
        self.buttons: list[CardButton] = []
        self._setup_buttons()

    def _setup_buttons(self) -> None:
        """Set up the card buttons."""
        # Scale card size proportionally to APP dimensions
        card_width = int(APP_WIDTH * 0.05)  # 5% of screen width
        card_height = int(APP_HEIGHT * 0.11)  # 11% of screen height
        card_spacing = int(APP_WIDTH * 0.008)  # 0.8% of screen width
        max_cards_per_row = 10

        # Calculate how many rows we need
        num_cards = len(self.available_cards)
        num_rows = (num_cards + max_cards_per_row - 1) // max_cards_per_row

        # Calculate starting position
        start_y = APP_HEIGHT // 2 - (num_rows * (card_height + card_spacing)) // 2

        # Create buttons for each card
        for i, card in enumerate(self.available_cards):
            row = i // max_cards_per_row
            col = i % max_cards_per_row
            cards_in_row = min(max_cards_per_row, num_cards - row * max_cards_per_row)
            row_width = cards_in_row * card_width + (cards_in_row - 1) * card_spacing
            start_x = (APP_WIDTH - row_width) // 2

            x = start_x + col * (card_width + card_spacing)
            y = start_y + row * (card_height + card_spacing)

            # Scale card image
            card_image = pygame.transform.scale(card.png, (card_width, card_height))
            button = CardButton(x, y, card_width, card_height, card, card_image)
            self.buttons.append(button)

    def show(self) -> "VisualCard":
        """Show the card selector and wait for user input.

        Returns:
            The selected card.
        """
        clock = pygame.time.Clock()

        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.is_clicked(mouse_x, mouse_y):
                            return button.card

            # Update hover state
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for button in self.buttons:
                button.update_hover(mouse_x, mouse_y)

            # Draw
            self._draw()

            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS

    def _draw(self) -> None:
        """Draw the card selector dialog."""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((APP_WIDTH, APP_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Draw dialog background - scale proportionally
        dialog_width = int(APP_WIDTH * 0.61)  # 61% of screen width
        dialog_height = int(APP_HEIGHT * 0.48)  # 48% of screen height
        dialog_x = (APP_WIDTH - dialog_width) // 2
        dialog_y = (APP_HEIGHT - dialog_height) // 2

        pygame.draw.rect(
            self.screen,
            (40, 40, 40),
            (dialog_x, dialog_y, dialog_width, dialog_height),
        )

        # Draw dialog border
        pygame.draw.rect(
            self.screen,
            (200, 200, 200),
            (dialog_x, dialog_y, dialog_width, dialog_height),
            3,
        )

        # Draw title - scale font size
        font_size = int(APP_HEIGHT * 0.06)  # 6% of screen height
        font = pygame.font.Font(None, font_size)
        title_text = font.render(
            "Choose a card to discard", ANTI_ALIASING, (255, 255, 255)
        )
        title_rect = title_text.get_rect(
            center=(APP_WIDTH // 2, dialog_y + int(APP_HEIGHT * 0.05))
        )
        self.screen.blit(title_text, title_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
