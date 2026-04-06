"""Q-Learning agent for Notty card game."""

import logging
import pickle  # nosec: B403
import secrets
from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from notty.src.visual.game import VisualGame

logger = logging.getLogger(__name__)


class QLearningAgent:
    """Q-Learning agent that learns to play Notty through reinforcement learning."""

    def __init__(
        self,
        alpha: float = 0.1,
        gamma: float = 0.9,
        epsilon: float = 0.2,
        epsilon_decay: float = 0.9995,
        epsilon_min: float = 0.05,
    ) -> None:
        """Initialize Q-Learning agent.

        Args:
            alpha: Learning rate (how much to update Q-values).
            gamma: Discount factor (how much to value future rewards).
            epsilon: Exploration rate (probability of random action).
            epsilon_decay: Rate at which epsilon decreases.
            epsilon_min: Minimum epsilon value.
        """
        self.q_table: dict[tuple[int, int, bool, int], dict[str, float]] = defaultdict(
            lambda: defaultdict(float)
        )
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

        # Track learning statistics
        self.total_actions = 0
        self.exploration_actions = 0
        self.last_state: tuple[int, int, bool, int] | None = None
        self.last_action: str | None = None

    def get_state(self, game: "VisualGame") -> tuple[int, int, bool, int]:
        """Extract state features from the game.

        Args:
            game: The game instance.

        Returns:
            Tuple representing the current state.
        """
        current_player = game.get_current_player()
        hand_size = current_player.hand.size()
        deck_size = game.deck.size()

        # Discretize hand size into buckets
        hand_bucket = min(hand_size // 5, 3)  # 0-4, 5-9, 10-14, 15-20

        # Discretize deck size
        deck_bucket = 0 if deck_size < 30 else (1 if deck_size < 60 else 2)  # noqa: PLR2004

        # Check if can discard
        can_discard = game.can_discard_group()

        # Count other players' cards (simplified)
        other_players = game.get_other_players()
        avg_other_hand_size = (
            sum(p.hand.size() for p in other_players) // len(other_players)
            if other_players
            else 0
        )
        other_hand_bucket = min(avg_other_hand_size // 5, 3)

        return (hand_bucket, deck_bucket, can_discard, other_hand_bucket)

    def choose_action(self, game: "VisualGame") -> str:
        """Choose an action using epsilon-greedy policy.

        Args:
            game: The game instance.

        Returns:
            The chosen action name.
        """
        state = self.get_state(game)
        possible_actions = game.get_all_possible_actions()

        if not possible_actions:
            # Fallback - should not happen
            return "next_turn"

        self.total_actions += 1

        # Epsilon-greedy exploration
        if secrets.randbelow(10000) / 10000 < self.epsilon:
            self.exploration_actions += 1
            action = secrets.choice(possible_actions)
        else:
            # Exploitation: choose best known action
            q_values = {
                action: self.q_table[state][action] for action in possible_actions
            }
            max_q = max(q_values.values())
            # If multiple actions have same Q-value, choose randomly among them
            best_actions = [a for a, q in q_values.items() if q == max_q]
            action = secrets.choice(best_actions)

        # Store for learning
        self.last_state = state
        self.last_action = action

        return action

    def learn(self, game: "VisualGame", reward: float) -> None:
        """Update Q-values based on the reward received.

        Args:
            game: The game instance.
            reward: The reward received for the last action.
        """
        if self.last_state is None or self.last_action is None:
            return

        current_state = self.get_state(game)
        possible_actions = game.get_all_possible_actions()

        # Get max Q-value for next state
        if possible_actions:
            next_max_q = max(
                self.q_table[current_state][action] for action in possible_actions
            )
        else:
            next_max_q = 0.0

        # Q-learning update rule
        old_q = self.q_table[self.last_state][self.last_action]
        new_q = old_q + self.alpha * (reward + self.gamma * next_max_q - old_q)
        self.q_table[self.last_state][self.last_action] = new_q

        # Decay epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def reset_episode(self) -> None:
        """Reset episode-specific tracking."""
        self.last_state = None
        self.last_action = None

    def save(self, filepath: str = "notty_qtable.pkl") -> None:
        """Save Q-table to file.

        Args:
            filepath: Path to save the Q-table.
        """
        data: dict[
            str, dict[tuple[int, int, bool, int], dict[str, float]] | float | int
        ] = {
            "q_table": dict(self.q_table),
            "epsilon": self.epsilon,
            "total_actions": self.total_actions,
            "exploration_actions": self.exploration_actions,
        }
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with Path(filepath).open("wb") as f:
            pickle.dump(data, f)
        logger.info("Q-table saved to %s", filepath)

    def load(self, filepath: str = "notty_qtable.pkl") -> bool:
        """Load Q-table from file.

        Args:
            filepath: Path to load the Q-table from.

        Returns:
            True if loaded successfully, False otherwise.
        """
        if not Path(filepath).exists():
            logger.info("No Q-table found at %s, starting fresh", filepath)
            return False

        try:
            with Path(filepath).open("rb") as f:
                data = pickle.load(f)  # nosec: B301  # noqa: S301

            # Convert back to defaultdict
            self.q_table = defaultdict(lambda: defaultdict(float))
            for state, actions in data["q_table"].items():
                for action, q_value in actions.items():
                    self.q_table[state][action] = q_value

            self.epsilon = data.get("epsilon", self.epsilon)
            self.total_actions = data.get("total_actions", 0)
            self.exploration_actions = data.get("exploration_actions", 0)

            logger.info("Q-table loaded from %s", filepath)
            logger.info("  States learned: %d", len(self.q_table))
            logger.info("  Total actions: %d", self.total_actions)
            logger.info("  Exploration rate: %.3f", self.epsilon)
        except Exception:
            logger.exception("Error loading Q-table")
            return False
        else:
            return True

    def get_stats(self) -> dict[str, int | float]:
        """Get learning statistics.

        Returns:
            Dictionary with learning statistics.
        """
        exploration_rate = (
            self.exploration_actions / self.total_actions
            if self.total_actions > 0
            else 0
        )
        return {
            "states_learned": len(self.q_table),
            "total_actions": self.total_actions,
            "exploration_actions": self.exploration_actions,
            "exploration_rate": exploration_rate,
            "current_epsilon": self.epsilon,
        }
