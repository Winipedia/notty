"""Winner display dialog for showing the game winner."""

from typing import TYPE_CHECKING

import pygame
from pyrig.dev.artifacts.resources.resource import get_resource_path

from notty.dev.artifacts.resources.visuals import players
from notty.src.consts import ANTI_ALIASING, APP_HEIGHT, APP_WIDTH

if TYPE_CHECKING:
    from notty.src.visual.player import VisualPlayer


class WinnerDisplay:
    """Dialog for displaying the winner of the game."""

    def __init__(self, screen: pygame.Surface, winner: "VisualPlayer") -> None:
        """Initialize the winner display.

        Args:
            screen: The pygame display surface.
            winner: The winning player object.
        """
        self.screen = screen
        self.winner = winner
        self.winner_name = winner.name

        # Load and scale the winner's image
        png_path = get_resource_path(winner.name + ".png", players)
        img = pygame.image.load(png_path)
        self.winner_image = pygame.transform.scale(img, (200, 200))

    def show(self) -> None:
        """Show the winner display and wait for user to click to continue.

        This displays a congratulations message and waits for the user to
        click anywhere to dismiss the dialog and start a new game.
        """
        clock = pygame.time.Clock()

        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Any click dismisses the dialog
                    return
                if event.type == pygame.KEYDOWN:
                    # Any key press dismisses the dialog
                    return

            # Draw
            self._draw()

            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS

    def _draw(self) -> None:
        """Draw the winner display dialog."""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((APP_WIDTH, APP_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Draw dialog background
        dialog_width = 600
        dialog_height = 500
        dialog_x = (APP_WIDTH - dialog_width) // 2
        dialog_y = (APP_HEIGHT - dialog_height) // 2

        # Draw background with gradient effect (using solid color for simplicity)
        pygame.draw.rect(
            self.screen,
            (20, 60, 20),  # Dark green background
            (dialog_x, dialog_y, dialog_width, dialog_height),
        )

        # Draw dialog border with gold color
        pygame.draw.rect(
            self.screen,
            (255, 215, 0),  # Gold border
            (dialog_x, dialog_y, dialog_width, dialog_height),
            5,
        )

        # Draw inner border for extra emphasis
        pygame.draw.rect(
            self.screen,
            (200, 200, 100),  # Lighter gold
            (dialog_x + 10, dialog_y + 10, dialog_width - 20, dialog_height - 20),
            2,
        )

        # Draw "WINNER!" title
        title_font = pygame.font.Font(None, 96)
        title_text = title_font.render("WINNER!", ANTI_ALIASING, (255, 215, 0))
        title_rect = title_text.get_rect(center=(APP_WIDTH // 2, dialog_y + 60))
        self.screen.blit(title_text, title_rect)

        # Draw winner image with gold border
        image_size = 200
        image_x = (APP_WIDTH - image_size) // 2
        image_y = dialog_y + 140

        # Draw gold border around image
        border_padding = 10
        pygame.draw.rect(
            self.screen,
            (255, 215, 0),  # Gold border
            (
                image_x - border_padding,
                image_y - border_padding,
                image_size + 2 * border_padding,
                image_size + 2 * border_padding,
            ),
            5,
        )

        # Draw the winner's image
        self.screen.blit(self.winner_image, (image_x, image_y))

        # Draw winner name below image
        name_font = pygame.font.Font(None, 56)
        name_text = name_font.render(self.winner_name, ANTI_ALIASING, (255, 255, 255))
        name_rect = name_text.get_rect(
            center=(APP_WIDTH // 2, image_y + image_size + 40)
        )
        self.screen.blit(name_text, name_rect)

        # Draw instruction to continue
        instruction_font = pygame.font.Font(None, 36)
        instruction_text = instruction_font.render(
            "Click anywhere to continue", ANTI_ALIASING, (180, 180, 180)
        )
        instruction_rect = instruction_text.get_rect(
            center=(APP_WIDTH // 2, dialog_y + dialog_height - 40)
        )
        self.screen.blit(instruction_text, instruction_rect)
