"""Number selector dialog for choosing how many cards to draw."""

import pygame

from notty.src.consts import ANTI_ALIASING, APP_HEIGHT, APP_WIDTH


class NumberButton:
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
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.number = number
        self.enabled = enabled
        self.hovered = False

    def is_clicked(self, mouse_x: int, mouse_y: int) -> bool:
        """Check if the button was clicked.

        Args:
            mouse_x: Mouse x coordinate.
            mouse_y: Mouse y coordinate.

        Returns:
            True if the button was clicked.
        """
        if not self.enabled:
            return False
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
        if not self.enabled:
            self.hovered = False
            return
        self.hovered = (
            self.x <= mouse_x <= self.x + self.width
            and self.y <= mouse_y <= self.y + self.height
        )

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


class NumberSelector:
    """Dialog for selecting a number (1, 2, or 3)."""

    def __init__(self, screen: pygame.Surface, max_number: int = 3) -> None:
        """Initialize the number selector.

        Args:
            screen: The pygame display surface.
            max_number: Maximum number that can be selected (1-3).
        """
        self.screen = screen
        self.max_number = min(max(1, max_number), 3)  # Clamp between 1 and 3
        self.buttons: list[NumberButton] = []
        self._setup_buttons()

    def _setup_buttons(self) -> None:
        """Set up the number buttons."""
        # Scale button size proportionally to APP dimensions
        button_width = int(APP_WIDTH * 0.08)  # 8% of screen width
        button_height = int(APP_HEIGHT * 0.12)  # 12% of screen height
        button_spacing = int(APP_WIDTH * 0.015)  # 1.5% of screen width

        # Center the buttons horizontally
        total_width = 3 * button_width + 2 * button_spacing
        start_x = (APP_WIDTH - total_width) // 2
        y = APP_HEIGHT // 2 - button_height // 2

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

    def show(self) -> int:
        """Show the number selector and wait for user input.

        Returns:
            The selected number (1, 2, or 3).
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
                            return button.number

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
        """Draw the number selector dialog."""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((APP_WIDTH, APP_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Draw dialog background - scale proportionally
        dialog_width = int(APP_WIDTH * 0.35)  # 35% of screen width
        dialog_height = int(APP_HEIGHT * 0.30)  # 30% of screen height
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
        title_text = font.render("How many cards?", ANTI_ALIASING, (255, 255, 255))
        title_rect = title_text.get_rect(
            center=(APP_WIDTH // 2, dialog_y + int(APP_HEIGHT * 0.06))
        )
        self.screen.blit(title_text, title_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
