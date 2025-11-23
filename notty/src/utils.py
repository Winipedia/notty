"""utils."""

from pathlib import Path

import pygame
from platformdirs import user_data_dir


def get_window_size() -> tuple[int, int]:
    """Get the window size based on screen dimensions.

    Returns:
        Tuple of (width, height) for the window.
    """
    # Get the display info to determine screen size
    pygame.display.init()
    display_info = pygame.display.Info()
    # quit pygame display
    pygame.display.quit()
    screen_width = display_info.current_w
    screen_height = display_info.current_h

    # Use 80% of screen width and 70% of screen height
    factor = 0.8
    app_width = int(screen_width * factor)
    app_height = int(screen_height * factor)

    # Set minimum dimensions to ensure usability
    min_width = 800
    min_height = 500

    app_width = max(app_width, min_width)
    app_height = max(app_height, min_height)

    return app_width, app_height


def get_user_data_dir() -> Path:
    """Get the user data directory for saving game data.

    This works correctly both in development and when packaged with PyInstaller.

    Returns:
        Path to the user data directory.
    """
    # Use platformdirs to get the appropriate user data directory
    data_dir = Path(user_data_dir("Notty", "Notty"))
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_qlearning_save_path() -> Path:
    """Get the path for saving Q-Learning agent data.

    Returns:
        Path to the Q-table save file.
    """
    return get_user_data_dir() / "notty_qtable.pkl"
