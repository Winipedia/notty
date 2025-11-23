"""Player selection screen and player setup."""

import pygame
from pyrig.dev.artifacts.resources.resource import get_resource_path

from notty.dev.artifacts.resources.visuals import players
from notty.src.consts import ANTI_ALIASING, APP_HEIGHT, APP_WIDTH
from notty.src.visual.player import VisualPlayer


def get_players(screen: pygame.Surface) -> list[VisualPlayer]:
    """Get the players with a selection screen to choose who you are."""
    # Show selection screen to choose yourself
    selected_player = show_player_selection_screen(screen)

    # Show opponent selection screen
    opponent_names = show_opponent_selection_screen(screen, selected_player)

    # Create all players
    players_list: list[VisualPlayer] = []

    # Add human player
    players_list.append(VisualPlayer(selected_player, is_human=True, screen=screen))

    players_list.extend(
        VisualPlayer(name, is_human=False, screen=screen) for name in opponent_names
    )

    return players_list


def show_player_selection_screen(screen: pygame.Surface) -> str:
    """Show a screen to select which player you want to be.

    Args:
        screen: The pygame display surface.

    Returns:
        The name of the selected player.
    """
    all_names = VisualPlayer.get_all_player_names()
    selected = _show_selection_screen(
        screen=screen,
        available_names=all_names,
        title="Choose Your Player",
        instruction="Click on a player to select",
        allow_multiple=False,
    )
    return selected[0]


def show_opponent_selection_screen(
    screen: pygame.Surface, human_player: str
) -> list[str]:
    """Show a screen to select 1-2 opponents.

    Args:
        screen: The pygame display surface.
        human_player: The name of the human player to exclude.

    Returns:
        List of selected opponent names.
    """
    all_names = VisualPlayer.get_all_player_names()
    available_names = [name for name in all_names if name != human_player]

    return _show_selection_screen(
        screen=screen,
        available_names=available_names,
        title="Choose Opponents (1-2)",
        instruction="Click to select/deselect • Press ENTER when done",
        allow_multiple=True,
        min_selections=1,
        max_selections=2,
    )


def _show_selection_screen(  # noqa: PLR0913
    screen: pygame.Surface,
    available_names: list[str],
    title: str,
    instruction: str,
    *,
    allow_multiple: bool,
    min_selections: int = 1,
    max_selections: int = 1,
) -> list[str]:
    """Generic selection screen for choosing player(s).

    Args:
        screen: The pygame display surface.
        available_names: List of available player names.
        title: Title text to display.
        instruction: Instruction text to display.
        allow_multiple: Whether multiple selections are allowed.
        min_selections: Minimum number of selections required.
        max_selections: Maximum number of selections allowed.

    Returns:
        List of selected player names.
    """
    # Load player images
    player_images = _load_player_images(available_names)
    image_size = 150

    # Initialize fonts
    pygame.font.init()
    title_font = pygame.font.Font(None, 72)
    instruction_font = pygame.font.Font(None, 36)
    name_font = pygame.font.Font(None, 48)

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    highlight = (100, 200, 255)
    selected_color = (50, 255, 50)

    # Calculate positions
    player_positions = _calculate_positions(available_names, image_size)

    hovered_player = None
    selected_players: list[str] = []
    clock = pygame.time.Clock()

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for x, y, name in player_positions:
                    if _is_within_bounds(mouse_x, mouse_y, x, y, image_size):
                        if allow_multiple:
                            _toggle_selection(selected_players, name, max_selections)
                        else:
                            return [name]
            elif event.type == pygame.KEYDOWN and allow_multiple:
                if (
                    event.key == pygame.K_RETURN
                    and len(selected_players) >= min_selections
                ):
                    return selected_players

        # Update hover state
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered_player = _get_hovered_player(
            mouse_x, mouse_y, player_positions, image_size
        )

        # Draw everything
        _draw_selection_screen(
            screen=screen,
            title=title,
            instruction=instruction,
            player_positions=player_positions,
            player_images=player_images,
            hovered_player=hovered_player,
            selected_players=selected_players,
            image_size=image_size,
            fonts=(title_font, instruction_font, name_font),
            colors=(white, black, highlight, selected_color),
        )

        pygame.display.flip()
        clock.tick(60)


def _load_player_images(
    player_names: list[str], image_size: int = 150
) -> dict[str, pygame.Surface]:
    """Load and scale player images.

    Args:
        player_names: List of player names.
        image_size: Size to scale images to.

    Returns:
        Dictionary mapping player names to their scaled images.
    """
    player_images: dict[str, pygame.Surface] = {}
    for name in player_names:
        png_path = get_resource_path(name + ".png", players)
        img = pygame.image.load(png_path)
        player_images[name] = pygame.transform.scale(img, (image_size, image_size))
    return player_images


def _calculate_positions(
    player_names: list[str], image_size: int
) -> list[tuple[int, int, str]]:
    """Calculate positions for player images.

    Args:
        player_names: List of player names.
        image_size: Size of each image.

    Returns:
        List of (x, y, name) tuples.
    """
    player_spacing = APP_WIDTH // (len(player_names) + 1)
    positions: list[tuple[int, int, str]] = []
    for i, name in enumerate(player_names):
        x = player_spacing * (i + 1) - image_size // 2
        y = APP_HEIGHT // 2 - image_size // 2
        positions.append((x, y, name))
    return positions


def _is_within_bounds(mouse_x: int, mouse_y: int, x: int, y: int, size: int) -> bool:
    """Check if mouse position is within bounds.

    Args:
        mouse_x: Mouse x coordinate.
        mouse_y: Mouse y coordinate.
        x: Element x coordinate.
        y: Element y coordinate.
        size: Element size.

    Returns:
        True if mouse is within bounds.
    """
    return x <= mouse_x <= x + size and y <= mouse_y <= y + size


def _toggle_selection(
    selected_players: list[str], name: str, max_selections: int
) -> None:
    """Toggle player selection.

    Args:
        selected_players: List of currently selected players.
        name: Player name to toggle.
        max_selections: Maximum number of selections allowed.
    """
    if name in selected_players:
        selected_players.remove(name)
    elif len(selected_players) < max_selections:
        selected_players.append(name)


def _get_hovered_player(
    mouse_x: int,
    mouse_y: int,
    player_positions: list[tuple[int, int, str]],
    image_size: int,
) -> str | None:
    """Get the currently hovered player.

    Args:
        mouse_x: Mouse x coordinate.
        mouse_y: Mouse y coordinate.
        player_positions: List of player positions.
        image_size: Size of player images.

    Returns:
        Name of hovered player or None.
    """
    for x, y, name in player_positions:
        if _is_within_bounds(mouse_x, mouse_y, x, y, image_size):
            return name
    return None


def _draw_selection_screen(  # noqa: PLR0913
    screen: pygame.Surface,
    title: str,
    instruction: str,
    player_positions: list[tuple[int, int, str]],
    player_images: dict[str, pygame.Surface],
    hovered_player: str | None,
    selected_players: list[str],
    image_size: int,
    fonts: tuple[pygame.font.Font, pygame.font.Font, pygame.font.Font],
    colors: tuple[tuple[int, int, int], ...],
) -> None:
    """Draw the selection screen.

    Args:
        screen: The pygame display surface.
        title: Title text.
        instruction: Instruction text.
        player_positions: List of player positions.
        player_images: Dictionary of player images.
        hovered_player: Currently hovered player name.
        selected_players: List of selected player names.
        image_size: Size of player images.
        fonts: Tuple of (title_font, instruction_font, name_font).
        colors: Tuple of (white, black, highlight, selected_color).
    """
    title_font, instruction_font, name_font = fonts
    white, black, highlight, selected_color = colors

    # Draw background
    screen.fill(black)

    # Draw title
    title_text = title_font.render(title, ANTI_ALIASING, white)
    title_rect = title_text.get_rect(center=(APP_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)

    # Draw instruction
    instruction_text = instruction_font.render(instruction, ANTI_ALIASING, white)
    instruction_rect = instruction_text.get_rect(center=(APP_WIDTH // 2, 180))
    screen.blit(instruction_text, instruction_rect)

    # Draw player images
    for x, y, name in player_positions:
        # Determine border color
        if name in selected_players:
            border_color = selected_color
            border_width = 5
        elif name == hovered_player:
            border_color = highlight
            border_width = 5
        else:
            border_color = white
            border_width = 2

        # Draw border
        border_padding = 10
        pygame.draw.rect(
            screen,
            border_color,
            (
                x - border_padding,
                y - border_padding,
                image_size + 2 * border_padding,
                image_size + 2 * border_padding,
            ),
            border_width,
        )

        # Draw player image
        screen.blit(player_images[name], (x, y))

        # Draw player name
        color = (
            selected_color
            if name in selected_players
            else (highlight if name == hovered_player else white)
        )
        name_text = name_font.render(name.capitalize(), ANTI_ALIASING, color)
        name_rect = name_text.get_rect(
            center=(x + image_size // 2, y + image_size + 30)
        )
        screen.blit(name_text, name_rect)
