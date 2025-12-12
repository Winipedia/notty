# notty

<!-- tooling -->
[![pyrig](https://img.shields.io/badge/built%20with-pyrig-3776AB?logo=buildkite&logoColor=black)](https://github.com/Winipedia/pyrig)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)
<!-- code-quality -->
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/type%20checked-mypy-039dfc.svg)](https://mypy-lang.org/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![pytest](https://img.shields.io/badge/tested%20with-pytest-46a2f1.svg?logo=pytest)](https://pytest.org/)
[![coverage](https://img.shields.io/badge/coverage-90%25+-brightgreen.svg?logo=codecov&logoColor=white)](https://github.com/winipedia/pyrig)
<!-- package-info -->
[![PyPI](https://img.shields.io/pypi/v/notty?logo=pypi&logoColor=white)](https://pypi.org/project/notty/)
[![Python](https://img.shields.io/pypi/pyversions/notty)](https://pypi.org/project/notty/)
[![License](https://img.shields.io/github/license/Winipedia/notty)](https://github.com/Winipedia/notty/blob/main/LICENSE)
<!-- ci/cd -->
[![CI](https://img.shields.io/github/actions/workflow/status/Winipedia/notty/health_check.yaml?label=CI&logo=github)](https://github.com/Winipedia/notty/actions/workflows/health_check.yaml)
[![CD](https://img.shields.io/github/actions/workflow/status/Winipedia/notty/release.yaml?label=CD&logo=github)](https://github.com/Winipedia/notty/actions/workflows/release.yaml)


---

> A simple card game called Notty using Pygame

---



## Features

- 🎮 Visual interface with Pygame
- 🤖 AI opponents using Q-Learning
- 🎯 Multiple strategic actions per turn
- 🎴 90-card deck (5 colors × 9 numbers × 2 duplicates)
- 💾 AI learns and improves over time

## Installation

**Requirements:** Python 3.12

```bash
# Clone the repository
git clone https://github.com/Winipedia/notty.git
cd notty

# Install with uv (recommended)
uv pip install -e .

# Or install with pip
pip install -e .
```

## Quick Start

Run the game:

```bash
notty
```

The game will guide you through:
1. Selecting your player character
2. Choosing 1-2 computer opponents
3. Starting with 4 cards each

## Game Rules

### Deck
- **90 cards**: 5 colors (Red, Green, Yellow, Black, Blue) × 9 numbers (1-9) × 2 duplicates
- **Players**: 2-3 (1 human, 1-2 computer)
- **Starting hand**: 4 cards per player
- **Hand limit**: 20 cards maximum

### Actions (per turn)

1. **Draw 1-3 Cards** (once) - Draw from the deck
2. **Steal Card** (once) - Take a random card from an opponent
3. **Draw & Discard** (once) - Draw one card, then discard one card
4. **Discard Group** (unlimited) - Discard valid card groups
5. **Next Turn** - End your turn
6. **Play for Me** - Let AI make a move for you

### Valid Card Groups

**Sequence (Run):** 3+ consecutive cards of the same color
- Example: Blue 4, Blue 5, Blue 6

**Set:** 4+ cards of the same number with different colors (no duplicate colors)
- Example: Blue 4, Green 4, Red 4, Yellow 4

### Win Condition

**First player to empty their hand wins!**

## How to Play

### Interface
- **Top center**: Deck with card count
- **Bottom**: Player hands and avatars
- **Right side**: Action buttons
- **Black border**: Current player's turn

### Controls
- **Green buttons**: Available actions
- **Gray buttons**: Unavailable actions
- Click buttons to perform actions

### Tips
- Use "Play for Me" to learn from the AI
- Form sequences (same color, consecutive) or sets (same number, different colors)
- Steal from opponents with many cards
- Watch the deck count

## Development

### Setup

```bash
# Install with dev dependencies
uv pip install -e .

# Run tests
pytest

# Run linter
ruff check .

# Run type checker
mypy .
```

### Project Structure

```
notty/
├── notty/
│   ├── main.py              # Entry point
│   └── src/
│       ├── visual/          # Pygame UI components
│       ├── qlearning_agent.py  # AI implementation
│       └── computer_action_selection.py  # AI strategy
├── tests/                   # Test files
└── docs/                    # Documentation
```

## Documentation

See the [docs/](docs/) directory for more information:
- [Game Mechanics](docs/game-mechanics.md) - Detailed rules
- [AI System](docs/ai-system.md) - How the AI works

## License

MIT License - see [LICENSE](LICENSE) file.

## Authors

- Winipedia
- Azeez
- Hanmiao chen

---

Built with [pyrig](https://github.com/Winipedia/pyrig) and [Pygame](https://www.pygame.org/)
