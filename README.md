# notty

(This project uses [pyrig](https://github.com/Winipedia/pyrig))

A card game called Notty implementation in Python using Pygame.

## Game Overview

Notty is a card game for 2-3 players where the goal is to be the first to empty your hand by discarding valid card groups.

**Game Setup:**
- 90 cards total: 5 colors × 9 numbers × 2 duplicates
- Colors: red, green, yellow, black, blue
- Numbers: 1-9
- Each player starts with 4 cards (face-up, visible to all)
- Maximum 20 cards per hand

**Win Condition:**
- First player to empty their hand wins immediately

## Code Architecture

### Core Modules (`notty/src/`)

#### `card.py` - Card Representation
- **`Color`**: Constants for card colors (RED, GREEN, YELLOW, BLACK, BLUE)
- **`Number`**: Constants for card numbers (ONE through NINE)
- **`Card`**: Immutable dataclass representing a single card
  - Frozen dataclass ensures cards cannot be modified after creation
  - Validates color and number in `__post_init__`

#### `deck.py` - Deck Management
- **`Deck`**: Manages the 90-card deck
  - `draw()`: Draw a single card (raises ValueError if empty)
  - `draw_multiple(count)`: Draw multiple cards at once
  - `add_card(card)` / `add_cards(cards)`: Return discarded cards to deck
  - `shuffle()`: Randomize deck order
  - `is_empty()` / `size()`: Check deck state

#### `player.py` - Player & Hand Management
- **`Hand`**: Manages a player's cards
  - `MAX_CARDS = 20`: Maximum hand size
  - `add_card(card)`: Add card, auto-shuffles hand after adding
  - `add_cards(cards)`: Returns `dict[Card, bool]` showing which cards were added
  - `remove_card(card)` / `remove_cards(cards)`: Remove cards from hand
  - `hand_is_full()`: Check if at 20-card limit
  - `shuffle()`: Randomize card order in hand

- **`Player`**: Represents a player
  - `name`: Player's name
  - `is_human`: Boolean flag (True for human, False for computer)
  - `hand`: The player's Hand instance
  - Constants: `TYPE_HUMAN`, `TYPE_COMPUTER`

#### `game.py` - Game Logic & Turn Management
- **`Action`**: Constants for the 4 turn actions
  - `DRAW`: Draw 1-3 cards (once per turn)
  - `STEAL`: Take random card from opponent (once per turn)
  - `DRAW_DISCARD_DRAW`: Draw card, discard one, draw again (once per turn)
  - `DRAW_DISCARD_DISCARD`: Second part of draw-discard action

- **`Game`**: Orchestrates the entire game
  - **Setup**: `setup()` shuffles deck and deals 4 cards to each player
  - **Turn Management**:
    - `get_current_player()`: Returns whose turn it is
    - `get_other_players()`: Returns opponents (for stealing)
    - `next_turn()`: Advances to next player, resets action tracking
  - **Actions**:
    - `player_draws_multiple(count)`: Action 1 - Draw 1-3 cards
    - `player_steals(target)`: Action 2 - Steal random card from opponent
    - `player_draw_discard_draws()` + `player_draw_discard_discards(card)`: Action 3 - Draw, discard, draw
    - `player_discards_group(cards)`: Action 4 - Discard valid group (unlimited per turn)
  - **Validation**:
    - `card_group_is_valid(cards)`: Validates if cards form a legal group
      - **Sequence**: 3+ consecutive numbers, same color (e.g., red 4-5-6)
      - **Set**: 4+ same number, different colors (e.g., red 4, blue 4, green 4, yellow 4)
  - **Win Condition**: `check_win_condition()` checks if any player has empty hand
  - **Deck Reshuffling**: After discarding a group, cards are added back to deck and entire deck is reshuffled

#### `consts.py` - Constants
- `APP_NAME`
- `APP_WIDTH`
- `APP_HEIGHT`
- `ANTI_ALIASING`

### Main Application (`notty/main.py`)

#### Entry Point
- `main()`: Initializes Pygame, runs game, cleans up
- `run()`: Creates window, initializes game, starts event loop

#### Display Functions
- **`create_window()`**: Creates Pygame window with icon
- **`show_deck(screen, deck)`**: Displays deck widget at top center
  - Red rectangle (card back) with white border
  - Shows card count in center
  - "DECK" label below

- **`show_players(screen, game)`**: Displays all players horizontally at bottom
  - Divides screen width by number of players
  - Calls `show_player_with_hand()` for each player

- **`show_player_with_hand(screen, player, x_position)`**: Displays one player's area
  - Player name with emoji (👤 for human, 🤖 for computer)
  - Each card shown as:
    - White border
    - Colored center (matches card color)
    - Black outline
    - White number in center
  - Cards displayed side-by-side with spacing

#### Game Loop
- **`run_event_loop(screen, game)`**: Main game loop
  - Handles `pygame.QUIT` event (X button)
  - Clears screen with teal background `(25, 78, 78)`
  - Renders deck and all players
  - Updates display at 60 FPS

## Running the Game

```bash
# Using Poetry
poetry run notty

# Or just
notty
```

## Development

### Project Structure
```
notty/
├── notty/
│   ├── src/
│   │   ├── card.py       # Card, Color, Number classes
│   │   ├── deck.py       # Deck management
│   │   ├── player.py     # Hand and Player classes
│   │   ├── game.py       # Game logic and actions
│   │   └── consts.py     # Constants
│   └── main.py           # Pygame UI and entry point
├── tests/
│   └── test_notty/
│       └── test_src/     # Unit tests for all modules
└── README.md
```

### Running Tests
```bash
poetry run pytest tests/test_notty/test_src/
```

## Game Rules

### Turn Actions
Each turn, a player can perform:

1. **Draw (once per turn)**: Draw 1-3 cards from the deck
2. **Steal (once per turn)**: Take a random card from an opponent's hand (opponent's hand is shuffled first)
3. **Draw-Discard-Draw (once per turn)**: Draw a card, discard one, then draw again (allows drawing when hand is full)
4. **Discard Group (unlimited)**: Discard a valid group of cards

### Valid Card Groups
- **Sequence**: 3+ consecutive numbers of the same color
  - Example: red 4, red 5, red 6
- **Set**: 4+ cards with the same number but different colors
  - Example: red 7, blue 7, green 7, yellow 7

### Important Mechanics
- All cards are face-up and visible to all players
- After discarding a group, those cards are added back to the deck and the entire deck is reshuffled
- Maximum hand size is 20 cards (except during draw-discard-draw action)
- Players can pass their turn if they don't want to take any actions
