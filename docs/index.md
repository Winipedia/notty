# Home

<!-- ci/cd -->
[![CI](https://img.shields.io/github/actions/workflow/status/Winipedia/notty/health_check.yml?label=CI&logo=github)](https://github.com/Winipedia/notty/actions/workflows/health_check.yml)
[![CD](https://img.shields.io/github/actions/workflow/status/Winipedia/notty/deploy.yml?label=CD&logo=github)](https://github.com/Winipedia/notty/actions/workflows/deploy.yml)
<!-- testing -->
[![CoverageTester](https://codecov.io/gh/Winipedia/notty/branch/main/graph/badge.svg)](https://codecov.io/gh/Winipedia/notty)
[![ProjectTester](https://img.shields.io/badge/tested%20with-pytest-46a2f1.svg?logo=pytest)](https://pytest.org)
<!-- code-quality -->
[![DependencyAuditor](https://img.shields.io/badge/security-pip--audit-blue?logo=python)](https://github.com/pypa/pip-audit)
[![DependencyChecker](https://img.shields.io/badge/dependencies-deptry-blue)](https://github.com/osprey-oss/deptry)
[![MarkdownLinter](https://img.shields.io/badge/markdown-rumdl-darkgreen)](https://github.com/rvben/rumdl)
[![PythonLinter](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![SecretsChecker](https://img.shields.io/badge/secrets-detect--secrets-blue)](https://github.com/Yelp/detect-secrets)
[![SecurityLinter](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![SpellChecker](https://img.shields.io/badge/spell--check-typos-blue)](https://github.com/crate-ci/typos)
[![TypeChecker](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![VersionControlHookManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
<!-- tooling -->
[![PackageManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Pyrigger](https://img.shields.io/badge/built%20with-pyrig-3776AB?logo=buildkite&logoColor=black)](https://github.com/Winipedia/pyrig)
[![RemoteVersionController](https://img.shields.io/github/stars/Winipedia/notty?style=social)](https://github.com/Winipedia/notty)
[![VersionController](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white)](https://git-scm.com)
<!-- project-info -->
[![DocsBuilder](https://img.shields.io/badge/MkDocs-Documentation-326CE5?logo=mkdocs&logoColor=white)](https://Winipedia.github.io/notty)
[![ExecutableBuilder](https://img.shields.io/github/downloads/Winipedia/notty/total?logo=github&label=downloads)](https://github.com/Winipedia/notty/releases)
[![ProgrammingLanguage](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/github/license/Winipedia/notty)](https://github.com/Winipedia/notty/blob/main/LICENSE)

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

- [Main README](https://github.com/Winipedia/notty/blob/main/README.md)
- [GitHub Repository](https://github.com/Winipedia/notty)
- [License](https://github.com/Winipedia/notty/blob/main/LICENSE)
