"""Computer action selection."""

from collections import Counter
from typing import TYPE_CHECKING

from notty.src.consts import MAX_HAND_SIZE
from notty.src.qlearning_agent import QLearningAgent
from notty.src.utils import get_qlearning_save_path
from notty.src.visual.action_board import Action

if TYPE_CHECKING:
    from notty.src.visual.card import VisualCard
    from notty.src.visual.game import VisualGame
    from notty.src.visual.player import VisualPlayer

# Q-Learning agent container (persists across games)
_qlearning_agent_container: dict[str, QLearningAgent | None] = {"agent": None}


def get_qlearning_agent() -> QLearningAgent:
    """Get or create the Q-Learning agent.

    Returns:
        The Q-Learning agent instance.
    """
    agent = _qlearning_agent_container["agent"]
    if agent is None:
        agent = QLearningAgent(
            alpha=0.1,  # Learning rate
            gamma=0.9,  # Discount factor
            epsilon=0.2,  # Initial exploration rate
            epsilon_decay=0.9995,  # Decay rate
            epsilon_min=0.05,  # Minimum exploration
        )
        _qlearning_agent_container["agent"] = agent
        # Try to load existing Q-table
        save_path = str(get_qlearning_save_path())
        agent.load(save_path)
    return agent


def choose_draw_count(game: "VisualGame") -> int:  # noqa: C901
    """Choose how many cards to draw (1-3) using strategic analysis.

    Strategy:
    - Draw fewer cards if hand is nearly full (approaching 20 card limit)
    - Draw more cards if we have potential to form groups
    - Draw fewer cards if opponents are close to winning
    - Consider deck size to avoid running out

    Args:
        game: The game instance.

    Returns:
        Number of cards to draw (1-3).
    """
    current_player = game.get_current_player()
    hand_size = current_player.hand.size()
    deck_size = game.deck.size()
    cards = current_player.hand.cards

    # Base decision: start with 2 cards (balanced approach)
    draw_count = 2

    # Factor 1: Hand size constraint (max 20 cards)
    # If we're close to the limit, draw fewer cards
    if hand_size >= 18:  # noqa: PLR2004
        draw_count = 1  # Very close to limit
    elif hand_size >= 15:  # noqa: PLR2004
        draw_count = min(draw_count, 2)  # Moderately close
    elif hand_size <= 6:  # noqa: PLR2004
        draw_count = 3  # Very few cards, draw more aggressively

    # Factor 2: Analyze hand potential for forming groups
    # Count cards by color and number to see if we're close to groups
    color_counts = Counter(card.color for card in cards)
    number_counts = Counter(card.number for card in cards)

    # Check if we're close to forming a sequence (3+ consecutive same color)
    sequence_potential = 0
    for color in color_counts:
        color_cards = sorted([c.number for c in cards if c.color == color])
        # Check for consecutive numbers
        for i in range(len(color_cards) - 1):
            if color_cards[i + 1] - color_cards[i] == 1:
                sequence_potential += 1

    # Check if we're close to forming a set (4+ same number different colors)
    set_potential = sum(1 for count in number_counts.values() if count >= 3)  # noqa: PLR2004

    # If we have high potential for groups, draw more to complete them
    total_potential = sequence_potential + set_potential
    if total_potential >= 3:  # noqa: PLR2004
        draw_count = min(draw_count + 1, 3)
    elif total_potential == 0 and hand_size > 10:  # noqa: PLR2004
        # No potential and many cards - be conservative
        draw_count = max(draw_count - 1, 1)

    # Factor 3: Opponent analysis
    # If any opponent has very few cards, we need to be aggressive
    other_players = game.get_other_players()
    min_opponent_hand = (
        min(p.hand.size() for p in other_players) if other_players else 20
    )

    if min_opponent_hand <= 4:  # noqa: PLR2004
        # Opponent is close to winning, be more aggressive
        draw_count = min(draw_count + 1, 3)

    # Factor 4: Deck size consideration
    # If deck is running low, be more conservative
    if deck_size < 10:  # noqa: PLR2004
        draw_count = min(draw_count, 1)
    elif deck_size < 20:  # noqa: PLR2004
        draw_count = min(draw_count, 2)

    # Final constraint: ensure we don't exceed hand limit
    max_drawable = min(MAX_HAND_SIZE - hand_size, deck_size)
    draw_count = min(draw_count, max_drawable, 3)
    return max(draw_count, 1)  # Always draw at least 1


def choose_target_player(game: "VisualGame") -> "VisualPlayer":
    """Choose which player to steal from.

    Args:
        game: The game instance.

    Returns:
        The target player to steal from.
    """
    other_players = game.get_other_players()

    # Prefer stealing from player with most cards
    return max(other_players, key=lambda p: p.hand.size())


def choose_card_to_discard(game: "VisualGame") -> "VisualCard":
    """Choose which card to discard in draw-discard-discard action.

    Args:
        game: The game instance.

    Returns:
        The card to discard.
    """
    current_player = game.get_current_player()
    cards = current_player.hand.cards

    if not cards:
        msg = "No cards to discard"
        raise ValueError(msg)

    # Strategy: discard cards that are least likely to form groups
    # Count how many cards of each color and number we have

    color_counts = Counter(card.color for card in cards)
    number_counts = Counter(card.number for card in cards)

    # Score each card (lower is worse, more likely to discard)
    card_scores: list[tuple[VisualCard, int]] = []
    for card in cards:
        score = 0
        # Cards with more of the same color are better (can form sequences)
        score += color_counts[card.color] * 2
        # Cards with more of the same number are better (can form sets)
        score += number_counts[card.number] * 2

        # Check if card can be part of a sequence
        for other_card in cards:
            if (
                other_card.color == card.color
                and abs(other_card.number - card.number) == 1
            ):
                score += 3

        card_scores.append((card, score))

    # Sort by score and pick one of the worst cards
    card_scores.sort(key=lambda x: x[1])
    # Pick the worst card
    return card_scores[0][0]


def find_best_discard_group(game: "VisualGame") -> list["VisualCard"] | None:
    """Find the best group of cards to discard.

    Args:
        game: The game instance.

    Returns:
        List of cards to discard, or None if no valid group found.
    """
    discardable_groups = game.get_discardable_groups()
    if not discardable_groups:
        return None
    # Prefer larger groups (discard more cards)
    discardable_groups.sort(key=len, reverse=True)
    return discardable_groups[0]


def computer_chooses_action(game: "VisualGame") -> None:
    """Computer chooses an action using Q-Learning.

    Args:
        game: The game instance.
    """
    # Check if current player is a computer player and auto-pass
    current_player = game.get_current_player()
    if current_player.is_human or not game.can_computer_act():
        return
    game.mark_computer_action()

    # Get the Q-Learning agent
    agent = get_qlearning_agent()

    # Store previous hand size to calculate reward
    prev_hand_size = current_player.hand.size()

    # Choose action using Q-Learning
    action = agent.choose_action(game)

    # Choose appropriate parameters based on the action
    count, card, cards, target_player = None, None, None, None

    if action == Action.DRAW_MULTIPLE:
        count = choose_draw_count(game)
    elif action == Action.STEAL:
        target_player = choose_target_player(game)
    elif action == Action.DRAW_DISCARD_DISCARD:
        card = choose_card_to_discard(game)
    elif action == Action.DISCARD_GROUP:
        cards = find_best_discard_group(game)
        if cards is None:
            # Fallback: if we can't find a valid group, pass instead
            action = Action.NEXT_TURN

    # Execute the action
    game.do_action(
        action, count=count, card=card, cards=cards, target_player=target_player
    )

    # Calculate reward based on the action taken
    player_index = game.players.index(current_player)
    reward = game.calculate_reward(player_index, action)

    # Additional reward shaping based on hand size change
    new_hand_size = current_player.hand.size()
    hand_size_change = prev_hand_size - new_hand_size
    if hand_size_change > 0:
        # Reward for reducing hand size
        reward += hand_size_change * 2.0

    # Learn from the action
    agent.learn(game, reward)

    # Auto-save Q-table periodically (every 100 actions)
    if agent.total_actions % 100 == 0:
        save_path = str(get_qlearning_save_path())
        agent.save(save_path)


def save_qlearning_agent() -> None:
    """Save the Q-Learning agent's Q-table."""
    if _qlearning_agent_container["agent"] is not None:
        save_path = str(get_qlearning_save_path())
        _qlearning_agent_container["agent"].save(save_path)


def reset_qlearning_episode() -> None:
    """Reset the Q-Learning agent for a new episode/game."""
    if _qlearning_agent_container["agent"] is not None:
        _qlearning_agent_container["agent"].reset_episode()
