"""Main entrypoint for the project."""

import logging
import sys

import pygame

from notty.src.computer_action_selection import (
    computer_chooses_action,
    save_qlearning_agent,
)
from notty.src.consts import APP_HEIGHT, APP_NAME, APP_WIDTH
from notty.src.player_selection import get_players
from notty.src.visual.game import VisualGame
from notty.src.visual.winner_display import WinnerDisplay


def main() -> None:
    """Start the notty game."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    pygame.init()

    try:
        run()
    finally:
        # Save Q-Learning agent before exiting
        save_qlearning_agent()
        pygame.quit()


def run() -> None:
    """Run the game."""
    screen = get_screen()
    players = get_players(screen)

    game = VisualGame(screen, players)
    # run the event loop
    run_event_loop(game)


def get_screen() -> pygame.Surface:
    """Create the game window.

    Args:
        app_width: Width of the window.
        app_height: Height of the window.
    """
    screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
    # set the title
    pygame.display.set_caption(APP_NAME)
    return screen


def simulate_first_shuffle_and_deal() -> None:
    """Simulate the first shuffle and deal.

    Args:
        screen: The pygame display surface.
        game: The game instance.
        background: The background image surface.
        app_width: Width of the window.
        app_height: Height of the window.
    """


def run_event_loop(game: VisualGame) -> None:
    """Run the main event loop.

    Args:
        screen: The pygame display surface.
        game: The game instance.
        background: The background image surface.
        app_width: Width of the window.
        app_height: Height of the window.
    """
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game.all_players_have_no_cards():
                VisualGame.distribute_starting_cards(game)
                continue
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                game.action_board.handle_click(mouse_x, mouse_y)
                continue

        computer_chooses_action(game)

        game.draw()

        # Check for winner
        if game.check_win_condition():
            # Draw one final time to show the winning state
            game.draw()
            pygame.display.flip()

            # Show winner and reset game
            show_winner(game)
            break

        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS


def show_winner(game: VisualGame) -> None:
    """Show the winner display and reset the game.

    Args:
        game: The game instance.
    """
    if game.winner is None:
        return

    # Show winner display
    winner_display = WinnerDisplay(game.screen, game.winner)
    winner_display.show()


if __name__ == "__main__":
    main()
