# notty Documentation

<!-- tooling -->
[![pyrig](https://img.shields.io/badge/built%20with-pyrig-3776AB?logo=buildkite&logoColor=black)](https://github.com/Winipedia/pyrig)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Container](https://img.shields.io/badge/Container-Podman-A23CD6?logo=podman&logoColor=grey&colorA=0D1F3F&colorB=A23CD6)](https://podman.io/)
[![prek](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
[![MkDocs](https://img.shields.io/badge/MkDocs-Documentation-326CE5?logo=mkdocs&logoColor=white)](https://www.mkdocs.org/)
<!-- code-quality -->
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![pytest](https://img.shields.io/badge/tested%20with-pytest-46a2f1.svg?logo=pytest)](https://pytest.org/)
[![codecov](https://codecov.io/gh/Winipedia/notty/branch/main/graph/badge.svg)](https://codecov.io/gh/Winipedia/notty)
[![rumdl](https://img.shields.io/badge/markdown-rumdl-darkgreen)](https://github.com/rvben/rumdl)
<!-- package-info -->
[![PyPI](https://img.shields.io/pypi/v/notty?logo=pypi&logoColor=white)](https://pypi.org/project/notty)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/github/license/Winipedia/notty)](https://github.com/Winipedia/notty/blob/main/LICENSE)
<!-- ci/cd -->
[![CI](https://img.shields.io/github/actions/workflow/status/Winipedia/notty/health_check.yml?label=CI&logo=github)](https://github.com/Winipedia/notty/actions/workflows/health_check.yml)
[![CD](https://img.shields.io/github/actions/workflow/status/Winipedia/notty/release.yml?label=CD&logo=github)](https://github.com/Winipedia/notty/actions/workflows/release.yml)
<!-- documentation -->
[![Documentation](https://img.shields.io/badge/Docs-GitHub%20Pages-black?style=for-the-badge&logo=github&logoColor=white)](https://Winipedia.github.io/notty)

---

> A simple card game called Notty using Pygame

---

Welcome to the Notty card game documentation.

## Contents

- [Game Mechanics](game-mechanics.md) - How to play
- [AI System](ai-system.md) - How the computer players work

## Quick Start

1. Install: `uv pip install -e .`
2. Run: `notty`
3. Read [Game Mechanics](game-mechanics.md) to learn the rules

## About

Notty is a strategic card game for 2-3 players built with Python and Pygame.
The goal is to be the first to empty your hand by discarding valid card groups.

**Features:**

- 90-card deck (5 colors × 9 numbers × 2 duplicates)
- AI opponents using Q-Learning
- Visual interface with Pygame
- Multiple strategic actions

## Links

- [Main README](../README.md)
- [GitHub Repository](https://github.com/Winipedia/notty)
- [License](../LICENSE)
