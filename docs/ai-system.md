# AI System

This document explains how the computer players work in Notty.

## Overview

Computer players in Notty use **Q-Learning**, a reinforcement learning technique, to make strategic decisions. The AI learns from experience and improves over time.

## Q-Learning Basics

Q-Learning is a type of machine learning where an agent learns to make decisions by:
1. **Observing** the current state of the game
2. **Choosing** an action to perform
3. **Receiving** a reward based on the outcome
4. **Learning** from the reward to improve future decisions

### Key Concepts

- **State**: The current situation in the game (hand size, deck size, etc.)
- **Action**: What the AI can do (draw cards, steal, discard, etc.)
- **Reward**: Points given for good or bad actions
- **Q-Table**: A lookup table that stores the value of each action in each state

## How the AI Works

### State Representation

The AI simplifies the game state into four features:

1. **Hand size bucket**: 0-4 cards, 5-9 cards, 10-14 cards, or 15-20 cards
2. **Deck size bucket**: Low (<30), Medium (30-59), or High (≥60)
3. **Can discard**: Whether the AI can discard a valid group
4. **Opponent hand size**: Average hand size of other players (bucketed)

This simplified state makes learning faster and more efficient.

### Action Selection

The AI uses an **epsilon-greedy** strategy:

- **Exploration** (ε% of the time): Try a random action to discover new strategies
- **Exploitation** (1-ε% of the time): Choose the best known action based on past experience

The exploration rate (epsilon) starts at 20% and gradually decreases to 5% as the AI learns.

### Reward System

The AI receives rewards based on its actions:

| Action | Reward | Reason |
|--------|--------|--------|
| Win the game | +100.0 | Biggest reward for achieving the goal |
| Discard group | +10.0 | Good - reduces hand size |
| Reduce hand size | +2.0 per card | Encourages getting closer to winning |
| Steal card | +0.5 | Neutral - takes from opponent |
| Draw cards | -0.5 | Small penalty - increases hand size |
| Pass turn | -1.0 | Penalty for not making progress |

### Learning Process

After each action, the AI updates its Q-table using this formula:

```
Q(state, action) = Q(state, action) + α × [reward + γ × max(Q(next_state)) - Q(state, action)]
```

Where:
- **α (alpha)** = 0.1 (learning rate - how much to update)
- **γ (gamma)** = 0.9 (discount factor - how much to value future rewards)

## AI Strategy Components

### Draw Count Selection

When drawing cards, the AI considers:
- **Hand size**: Draw fewer if close to 20-card limit
- **Card potential**: Draw more if close to forming groups
- **Opponent status**: Draw more if opponents have few cards
- **Deck size**: Be conservative if deck is low

### Target Player Selection

When stealing, the AI targets:
- Players with the most cards (more likely to have useful cards)
- Avoids players with very few cards (close to winning)

### Card Discard Selection

When using Draw & Discard, the AI discards:
- Cards that don't fit into potential groups
- Duplicate cards that aren't useful
- Cards with numbers/colors that are isolated

### Group Discard Selection

The AI finds the best group to discard by:
1. Finding all valid groups in hand
2. Prioritizing larger groups (more cards discarded)
3. Choosing groups that leave useful cards in hand

## Persistent Learning

The AI's Q-table is saved to disk periodically:
- **Auto-save**: Every 100 actions
- **Manual save**: When the game exits
- **Save location**: `~/.notty/qlearning/notty_qtable.pkl`

This means the AI remembers what it learned across multiple games and continues to improve.

## Learning Statistics

The AI tracks:
- **Total actions**: How many actions it has taken
- **Exploration actions**: How many were random (exploring)
- **Epsilon**: Current exploration rate
- **Q-table size**: Number of state-action pairs learned

## AI Behavior

### Early Games (Exploration Phase)

- Takes more random actions (20% exploration)
- Tries different strategies
- Builds up the Q-table
- May make suboptimal moves

### Later Games (Exploitation Phase)

- Takes fewer random actions (5% exploration)
- Uses learned strategies
- Makes more optimal moves
- Still explores occasionally to find better strategies

## Implementation Details

### Files

- `notty/src/qlearning_agent.py`: Q-Learning agent implementation
- `notty/src/computer_action_selection.py`: AI strategy and decision-making

### Key Classes

- **QLearningAgent**: Manages Q-table, learning, and action selection
- **computer_chooses_action()**: Main function for AI decision-making

### Timing

- Computer players have a 1-second delay between actions
- This makes the game easier to follow visually
- The delay is purely cosmetic and doesn't affect AI performance

## Customization

You can modify the AI behavior by changing these parameters in `computer_action_selection.py`:

```python
agent = QLearningAgent(
    alpha=0.1,          # Learning rate (0.0 to 1.0)
    gamma=0.9,          # Discount factor (0.0 to 1.0)
    epsilon=0.2,        # Initial exploration rate (0.0 to 1.0)
    epsilon_decay=0.9995,  # How fast epsilon decreases
    epsilon_min=0.05    # Minimum exploration rate
)
```

## Future Improvements

Potential enhancements to the AI system:
- More sophisticated state representation
- Deep Q-Learning with neural networks
- Multi-agent learning (AIs learn from each other)
- Different difficulty levels
- Opponent modeling

---

For game rules, see [Game Mechanics](game-mechanics.md).

