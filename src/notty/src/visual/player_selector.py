"""Player selector dialog for choosing which player to steal from."""

from typing import TYPE_CHECKING

import pygame

from notty.src.consts import ANTI_ALIASING, APP_HEIGHT, APP_WIDTH
from notty.src.visual.base_selector import BaseSelector, SelectableButton

if TYPE_CHECKING:
    from notty.src.visual.player import VisualPlayer


class PlayerButton(SelectableButton["VisualPlayer"]):
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
        super().__init__(
            x, y, width, height, player, player_image, enabled=True, selectable=False
        )
        self.player = player
        self.player_image = player_image

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

        # Draw player name below the image - scale font size
        font_size = int(self.height * 0.24)  # 24% of image height
        font = pygame.font.Font(None, font_size)
        text_color = (100, 200, 255) if self.hovered else (255, 255, 255)
        text_surface = font.render(self.player.name, ANTI_ALIASING, text_color)
        text_rect = text_surface.get_rect(
            center=(
                self.x + self.width // 2,
                self.y + self.height + int(self.height * 0.2),
            )
        )
        screen.blit(text_surface, text_rect)


class PlayerSelector(BaseSelector["VisualPlayer"]):
    """Dialog for selecting a player to steal from."""

    def __init__(
        self, screen: pygame.Surface, available_players: list["VisualPlayer"]
    ) -> None:
        """Initialize the player selector.

        Args:
            screen: The pygame display surface.
            available_players: List of players that can be selected.
        """
        super().__init__(
            screen,
            title="Choose a player to steal from",
            items=available_players,
            max_selections=1,
        )

    def _get_button_dimensions(self) -> tuple[int, int, int]:
        """Get button dimensions (width, height, spacing).

        Returns:
            Tuple of (button_width, button_height, button_spacing).
        """
        image_size = int(APP_HEIGHT * 0.18)  # 18% of screen height
        button_spacing = int(APP_WIDTH * 0.03)  # 3% of screen width
        return image_size, image_size, button_spacing

    def _get_dialog_dimensions(self) -> tuple[int, int]:
        """Get dialog dimensions.

        Returns:
            Tuple of (dialog_width, dialog_height).
        """
        dialog_width = int(APP_WIDTH * 0.52)  # 52% of screen width
        dialog_height = int(APP_HEIGHT * 0.42)  # 42% of screen height
        return dialog_width, dialog_height

    def _setup_buttons(self) -> None:
        """Set up the player buttons."""
        # Get button dimensions
        image_size, _, button_spacing = self._get_button_dimensions()

        # Calculate total width needed
        num_players = len(self.items)
        total_width = num_players * image_size + (num_players - 1) * button_spacing
        start_x = int((APP_WIDTH - total_width) // 2)
        y = int(APP_HEIGHT // 2 - image_size // 2)

        # Create buttons for each player
        for i, player in enumerate(self.items):
            x = start_x + i * (image_size + button_spacing)
            # Load and scale player image
            player_image = pygame.transform.scale(player.png, (image_size, image_size))
            button = PlayerButton(x, y, image_size, image_size, player, player_image)
            self.buttons.append(button)
