# notty

<!-- project-status -->
[![CI](https://img.shields.io/github/actions/workflow/status/Winipedia/notty/health_check.yml?label=CI&logo=github)](https://github.com/Winipedia/notty/actions/workflows/health_check.yml)
[![CD](https://img.shields.io/github/actions/workflow/status/Winipedia/notty/deploy.yml?label=CD&logo=github)](https://github.com/Winipedia/notty/actions/workflows/deploy.yml)
[![CoverageTester](https://codecov.io/gh/Winipedia/notty/branch/main/graph/badge.svg)](https://codecov.io/gh/Winipedia/notty)
<!-- code-quality -->
[![ByteOrderMarkerFormatter](https://img.shields.io/badge/BOM-fix--byte--order--marker-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![CaseConflictChecker](https://img.shields.io/badge/case--conflict-check--case--conflict-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![DependencyAuditor](https://img.shields.io/badge/security-pip--audit-blue?logo=python)](https://github.com/pypa/pip-audit)
[![DependencyChecker](https://img.shields.io/badge/dependencies-deptry-blue)](https://github.com/osprey-oss/deptry)
[![EndOfFileFormatter](https://img.shields.io/badge/EOF-end--of--file--fixer-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![EndOfLineFormatter](https://img.shields.io/badge/EOL-mixed--line--ending-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![JSONFormatter](https://img.shields.io/badge/JSON-pretty--format--json-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![JSONLinter](https://img.shields.io/badge/JSON-check--json-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![LargeFileChecker](https://img.shields.io/badge/large--files-check--added--large--files-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![MarkdownLinter](https://img.shields.io/badge/Markdown-rumdl-darkgreen)](https://github.com/rvben/rumdl)
[![MergeConflictChecker](https://img.shields.io/badge/merge--conflict-check--merge--conflict-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![ModuleTestNamingChecker](https://img.shields.io/badge/test--naming-name--tests--test-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![PythonLinter](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![SecretsChecker](https://img.shields.io/badge/secrets-detect--secrets-blue)](https://github.com/Yelp/detect-secrets)
[![SecurityChecker](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![ShellFormatter](https://img.shields.io/badge/shell-shfmt-orange)](https://github.com/mvdan/sh)
[![ShellLinter](https://img.shields.io/badge/shell-shellcheck-blue)](https://github.com/koalaman/shellcheck)
[![SpellChecker](https://img.shields.io/badge/spell--check-typos-blue)](https://github.com/crate-ci/typos)
[![TOMLLinter](https://img.shields.io/badge/TOML-tombi-blueviolet)](https://github.com/tombi-toml/tombi)
[![TrailingWhitespaceFormatter](https://img.shields.io/badge/whitespace-trailing--whitespace--fixer-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![TypeChecker](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![YAMLLinter](https://img.shields.io/badge/YAML-ryl-red)](https://github.com/owenlamont/ryl)
<!-- tooling -->
[![PackageManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Pyrigger](https://img.shields.io/badge/built%20with-pyrig-3776AB?logo=buildkite&logoColor=black)](https://github.com/Winipedia/pyrig)
[![RemoteVersionController](https://img.shields.io/github/stars/Winipedia/notty?style=social)](https://github.com/Winipedia/notty)
[![VersionControlHookManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
[![VersionController](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white)](https://git-scm.com)
<!-- project-info -->
[![DocsBuilder](https://img.shields.io/badge/MkDocs-Documentation-326CE5?logo=mkdocs&logoColor=white)](https://Winipedia.github.io/notty)
[![ExecutableBuilder](https://img.shields.io/github/downloads/Winipedia/notty/total?logo=github&label=downloads)](https://github.com/Winipedia/notty/releases)
[![ProgrammingLanguage](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/github/license/Winipedia/notty)](https://github.com/Winipedia/notty/blob/main/LICENSE)

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

- **90 cards**: 5 colors (Red, Green, Yellow, Black, Blue)
  × 9 numbers (1-9) × 2 duplicates
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
- Form sequences (same color, consecutive)
  or sets (same number, different colors)
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

```text
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

Built with [pyrig](https://github.com/Winipedia/pyrig)
and [Pygame](https://www.pygame.org/)
