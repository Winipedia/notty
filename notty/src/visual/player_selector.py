"""Player selector dialog for choosing which player to steal from."""

from typing import TYPE_CHECKING

import pygame

from notty.src.consts import ANTI_ALIASING, APP_HEIGHT, APP_WIDTH

if TYPE_CHECKING:
    from notty.src.visual.player import VisualPlayer


class PlayerButton:
    """Represents a clickable player button."""

    def __init__(  # noqa: PLR0913
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        player: "VisualPlayer",
        player_image: pygame.Surface,
    ) -> None:
        """Initialize a player button.

        Args:
            x: X coordinate of the button.
            y: Y coordinate of the button.
            width: Width of the button.
            height: Height of the button.
            player: The player this button represents.
            player_image: The image of the player.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.player = player
        self.player_image = player_image
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
        border_padding = 10
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

        # Draw player image
        screen.blit(self.player_image, (self.x, self.y))

        # Draw player name below the image
        font = pygame.font.Font(None, 36)
        text_color = (100, 200, 255) if self.hovered else (255, 255, 255)
        text_surface = font.render(self.player.name, ANTI_ALIASING, text_color)
        text_rect = text_surface.get_rect(
            center=(self.x + self.width // 2, self.y + self.height + 30)
        )
        screen.blit(text_surface, text_rect)


class PlayerSelector:
    """Dialog for selecting a player to steal from."""

    def __init__(
        self, screen: pygame.Surface, available_players: list["VisualPlayer"]
    ) -> None:
        """Initialize the player selector.

        Args:
            screen: The pygame display surface.
            available_players: List of players that can be selected.
        """
        self.screen = screen
        self.available_players = available_players
        self.buttons: list[PlayerButton] = []
        self._setup_buttons()

    def _setup_buttons(self) -> None:
        """Set up the player buttons."""
        image_size = 150
        button_spacing = 40

        # Calculate total width needed
        num_players = len(self.available_players)
        total_width = num_players * image_size + (num_players - 1) * button_spacing
        start_x = (APP_WIDTH - total_width) // 2
        y = APP_HEIGHT // 2 - image_size // 2

        # Create buttons for each player
        for i, player in enumerate(self.available_players):
            x = start_x + i * (image_size + button_spacing)
            # Load and scale player image
            player_image = pygame.transform.scale(player.png, (image_size, image_size))
            button = PlayerButton(x, y, image_size, image_size, player, player_image)
            self.buttons.append(button)

    def show(self) -> "VisualPlayer":
        """Show the player selector and wait for user input.

        Returns:
            The selected player.
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
                            return button.player

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
        """Draw the player selector dialog."""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((APP_WIDTH, APP_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Draw dialog background
        dialog_width = 600
        dialog_height = 350
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

        # Draw title
        font = pygame.font.Font(None, 48)
        title_text = font.render(
            "Choose a player to steal from", ANTI_ALIASING, (255, 255, 255)
        )
        title_rect = title_text.get_rect(center=(APP_WIDTH // 2, dialog_y + 50))
        self.screen.blit(title_text, title_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
