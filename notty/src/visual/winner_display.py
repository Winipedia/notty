"""Winner display dialog for showing the game winner."""

from typing import TYPE_CHECKING

import pygame
from pyrig.src.resource import resource_path

from notty.resources.visuals import players
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

        # Load and scale the winner's image - scale proportionally
        png_path = resource_path(winner.name + ".png", players)
        img = pygame.image.load(png_path)
        image_size = int(APP_HEIGHT * 0.24)  # 24% of screen height
        self.winner_image = pygame.transform.scale(img, (image_size, image_size))

        # Button properties - scale proportionally
        self.button_width = int(APP_WIDTH * 0.22)  # 22% of screen width
        self.button_height = int(APP_HEIGHT * 0.07)  # 7% of screen height
        self.button_spacing = int(APP_HEIGHT * 0.024)  # 2.4% of screen height

        # Calculate button positions
        dialog_width = int(APP_WIDTH * 0.52)  # 52% of screen width
        dialog_height = int(APP_HEIGHT * 0.66)  # 66% of screen height
        dialog_x = int((APP_WIDTH - dialog_width) // 2)
        dialog_y = int((APP_HEIGHT - dialog_height) // 2)

        # New Game button
        self.new_game_button_rect = pygame.Rect(
            dialog_x + (dialog_width - self.button_width) // 2,
            dialog_y + dialog_height - int(APP_HEIGHT * 0.17),
            self.button_width,
            self.button_height,
        )

        # Quit button
        self.quit_button_rect = pygame.Rect(
            dialog_x + (dialog_width - self.button_width) // 2,
            dialog_y
            + dialog_height
            - int(APP_HEIGHT * 0.17)
            + self.button_height
            + self.button_spacing,
            self.button_width,
            self.button_height,
        )

        # Hover states
        self.new_game_hovered = False
        self.quit_hovered = False

    def show(self) -> str:
        """Show the winner display and wait for user to click a button.

        This displays a congratulations message and waits for the user to
        click either "Start New Game" or "Quit".

        Returns:
            "new_game" if user clicked Start New Game, "quit" if user clicked Quit.
        """
        clock = pygame.time.Clock()

        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Check if New Game button was clicked
                    if self.new_game_button_rect.collidepoint(mouse_x, mouse_y):
                        return "new_game"

                    # Check if Quit button was clicked
                    if self.quit_button_rect.collidepoint(mouse_x, mouse_y):
                        return "quit"

            # Update hover states
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.new_game_hovered = self.new_game_button_rect.collidepoint(
                mouse_x, mouse_y
            )
            self.quit_hovered = self.quit_button_rect.collidepoint(mouse_x, mouse_y)

            # Draw
            self._draw()

            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS

    def _draw(self) -> None:
        """Draw the winner display dialog."""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((int(APP_WIDTH), int(APP_HEIGHT)))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Draw dialog background - scale proportionally
        dialog_width = int(APP_WIDTH * 0.52)  # 52% of screen width
        dialog_height = int(APP_HEIGHT * 0.66)  # 66% of screen height
        dialog_x = int((APP_WIDTH - dialog_width) // 2)
        dialog_y = int((APP_HEIGHT - dialog_height) // 2)

        # Draw background with gradient effect (using solid color for simplicity)
        pygame.draw.rect(
            self.screen,
            (20, 60, 20),  # Dark green background
            (dialog_x, dialog_y, dialog_width, dialog_height),
        )

        # Draw dialog border with gold color
        border_width = max(3, int(APP_HEIGHT * 0.006))  # 0.6% of screen height, min 3
        pygame.draw.rect(
            self.screen,
            (255, 215, 0),  # Gold border
            (dialog_x, dialog_y, dialog_width, dialog_height),
            border_width,
        )

        # Draw inner border for extra emphasis
        inner_border_offset = int(APP_HEIGHT * 0.012)  # 1.2% of screen height
        pygame.draw.rect(
            self.screen,
            (200, 200, 100),  # Lighter gold
            (
                dialog_x + inner_border_offset,
                dialog_y + inner_border_offset,
                dialog_width - 2 * inner_border_offset,
                dialog_height - 2 * inner_border_offset,
            ),
            max(2, int(APP_HEIGHT * 0.0024)),  # 0.24% of screen height, min 2
        )

        # Draw "WINNER!" title - scale font size
        title_font_size = int(APP_HEIGHT * 0.115)  # 11.5% of screen height
        title_font = pygame.font.Font(None, title_font_size)
        title_text = title_font.render("WINNER!", ANTI_ALIASING, (255, 215, 0))
        title_rect = title_text.get_rect(
            center=(int(APP_WIDTH // 2), dialog_y + int(APP_HEIGHT * 0.07))
        )
        self.screen.blit(title_text, title_rect)

        # Draw winner image with gold border
        image_size = int(APP_HEIGHT * 0.24)  # 24% of screen height
        image_x = int((APP_WIDTH - image_size) // 2)
        image_y = dialog_y + int(APP_HEIGHT * 0.17)

        # Draw gold border around image
        border_padding = int(APP_HEIGHT * 0.012)  # 1.2% of screen height
        pygame.draw.rect(
            self.screen,
            (255, 215, 0),  # Gold border
            (
                image_x - border_padding,
                image_y - border_padding,
                image_size + 2 * border_padding,
                image_size + 2 * border_padding,
            ),
            border_width,
        )

        # Draw the winner's image
        self.screen.blit(self.winner_image, (image_x, image_y))

        # Draw winner name below image - scale font size
        name_font_size = int(APP_HEIGHT * 0.067)  # 6.7% of screen height
        name_font = pygame.font.Font(None, name_font_size)
        name_text = name_font.render(self.winner_name, ANTI_ALIASING, (255, 255, 255))
        name_rect = name_text.get_rect(
            center=(int(APP_WIDTH // 2), image_y + image_size + int(APP_HEIGHT * 0.048))
        )
        self.screen.blit(name_text, name_rect)

        # Draw buttons
        self._draw_button(
            self.new_game_button_rect,
            "Start New Game",
            hovered=self.new_game_hovered,
            normal_color=(50, 150, 50),  # Green
            hover_color=(70, 200, 70),  # Lighter green on hover
        )

        self._draw_button(
            self.quit_button_rect,
            "Quit",
            hovered=self.quit_hovered,
            normal_color=(150, 50, 50),  # Red
            hover_color=(200, 70, 70),  # Lighter red on hover
        )

    def _draw_button(
        self,
        rect: pygame.Rect,
        text: str,
        *,
        hovered: bool,
        normal_color: tuple[int, int, int],
        hover_color: tuple[int, int, int],
    ) -> None:
        """Draw a button with hover effect.

        Args:
            rect: The button rectangle.
            text: The button text.
            hovered: Whether the button is hovered.
            normal_color: The normal button color.
            hover_color: The hover button color.
        """
        # Choose color based on hover state
        color = hover_color if hovered else normal_color

        # Draw button background - scale border radius
        border_radius = int(APP_HEIGHT * 0.012)  # 1.2% of screen height
        pygame.draw.rect(self.screen, color, rect, border_radius=border_radius)

        # Draw button border
        border_color = (255, 215, 0) if hovered else (200, 200, 100)
        border_width = max(2, int(APP_HEIGHT * 0.0036))  # 0.36% of screen height, min 2
        pygame.draw.rect(
            self.screen, border_color, rect, border_width, border_radius=border_radius
        )

        # Draw button text - scale font size
        button_font_size = int(APP_HEIGHT * 0.058)  # 5.8% of screen height
        button_font = pygame.font.Font(None, button_font_size)
        button_text = button_font.render(text, ANTI_ALIASING, (255, 255, 255))
        text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, text_rect)
