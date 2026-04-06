"""Number selector dialog for choosing how many cards to draw."""

import pygame

from notty.src.consts import ANTI_ALIASING, APP_HEIGHT, APP_WIDTH
from notty.src.visual.base_selector import BaseSelector, SelectableButton


class NumberButton(SelectableButton[int]):
    """Represents a clickable number button."""

    def __init__(  # noqa: PLR0913
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        number: int,
        *,
        enabled: bool = True,
    ) -> None:
        """Initialize a number button.

        Args:
            x: X coordinate of the button.
            y: Y coordinate of the button.
            width: Width of the button.
            height: Height of the button.
            number: The number this button represents.
            enabled: Whether the button is enabled (clickable).
        """
        # NumberButton doesn't use images, so pass None
        super().__init__(
            x, y, width, height, number, None, enabled=enabled, selectable=False
        )
        self.number = number

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the button.

        Args:
            screen: The pygame display surface.
        """
        # Determine button color based on state
        if not self.enabled:
            bg_color = (100, 100, 100)  # Gray for disabled
            text_color = (150, 150, 150)  # Light gray text
            border_color = (70, 70, 70)
        elif self.hovered:
            bg_color = (100, 200, 255)  # Light blue for hover
            text_color = (0, 0, 0)  # Black text
            border_color = (50, 150, 255)
        else:
            bg_color = (50, 150, 50)  # Green
            text_color = (255, 255, 255)  # White text
            border_color = (30, 100, 30)

        # Draw button background
        pygame.draw.rect(screen, bg_color, (self.x, self.y, self.width, self.height))

        # Draw button border
        pygame.draw.rect(
            screen, border_color, (self.x, self.y, self.width, self.height), 3
        )

        # Draw button text - scale font size based on button height
        font_size = int(self.height * 0.7)  # 70% of button height
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(str(self.number), ANTI_ALIASING, text_color)
        text_rect = text_surface.get_rect(
            center=(self.x + self.width // 2, self.y + self.height // 2)
        )
        screen.blit(text_surface, text_rect)


class NumberSelector(BaseSelector[int]):
    """Dialog for selecting a number (1, 2, or 3)."""

    def __init__(self, screen: pygame.Surface, max_number: int = 3) -> None:
        """Initialize the number selector.

        Args:
            screen: The pygame display surface.
            max_number: Maximum number that can be selected (1-3).
        """
        self.max_number = min(max(1, max_number), 3)  # Clamp between 1 and 3
        # Create items list [1, 2, 3]
        items = list(range(1, 4))
        super().__init__(
            screen,
            title="How many cards do you want to draw?",
            items=items,
            max_selections=1,
        )

    def _get_button_dimensions(self) -> tuple[int, int, int]:
        """Get button dimensions (width, height, spacing).

        Returns:
            Tuple of (button_width, button_height, button_spacing).
        """
        button_width = int(APP_WIDTH * 0.08)  # 8% of screen width
        button_height = int(APP_HEIGHT * 0.12)  # 12% of screen height
        button_spacing = int(APP_WIDTH * 0.015)  # 1.5% of screen width
        return button_width, button_height, button_spacing

    def _get_dialog_dimensions(self) -> tuple[int, int]:
        """Get dialog dimensions.

        Returns:
            Tuple of (dialog_width, dialog_height).
        """
        dialog_width = int(APP_WIDTH * 0.35)  # 35% of screen width
        dialog_height = int(APP_HEIGHT * 0.30)  # 30% of screen height
        return dialog_width, dialog_height

    def _setup_buttons(self) -> None:
        """Set up the number buttons."""
        # Get button dimensions
        button_width, button_height, button_spacing = self._get_button_dimensions()

        # Center the buttons horizontally
        total_width = 3 * button_width + 2 * button_spacing
        start_x = int((APP_WIDTH - total_width) // 2)
        y = int(APP_HEIGHT // 2 - button_height // 2)

        # Create buttons for 1, 2, 3
        for i in range(3):
            number = i + 1
            x = start_x + i * (button_width + button_spacing)
            # Disable buttons that exceed max_number
            enabled = number <= self.max_number
            button = NumberButton(
                x, y, button_width, button_height, number, enabled=enabled
            )
            self.buttons.append(button)
