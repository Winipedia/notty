# Game Mechanics

This document explains the rules and mechanics of Notty.

## Overview

Notty is a card game for 2-3 players where the objective is to be the first to empty your hand by discarding valid card groups.

## Deck Composition

- **Total cards**: 90
- **Colors**: Red, Green, Yellow, Black, Blue (5 colors)
- **Numbers**: 1 through 9 (9 numbers)
- **Duplicates**: 2 of each color-number combination

Example: There are 2 Red 5s, 2 Blue 3s, etc.

## Game Setup

- **Players**: 2-3 (1 human, 1-2 computer)
- **Starting hand**: 4 cards dealt face-up to each player
- **Hand limit**: Maximum 20 cards per player
- **Turn order**: Players take turns in sequence

## Turn Actions

On your turn, you can perform multiple actions. Most actions can only be done once per turn.

### 1. Draw 1-3 Cards (once per turn)

- Draw between 1 and 3 cards from the deck
- You choose how many to draw
- Cannot exceed the 20-card hand limit

### 2. Steal Card (once per turn)

- Take a random card from an opponent's hand
- The opponent's hand is shuffled before you take a card
- You cannot see which card you'll get

### 3. Draw & Discard (once per turn, two-step)

This is a two-step action:
1. **Draw**: Draw one card from the deck
2. **Discard**: Discard one card back to the deck

Useful for cycling through cards when you need specific numbers or colors.

### 4. Discard Group (unlimited per turn)

- Discard a valid group of cards (see Valid Groups below)
- This is the main way to reduce your hand size
- You can discard multiple groups in one turn
- Discarded cards are shuffled back into the deck

### 5. Next Turn (always available)

- End your turn and pass to the next player
- Use this when you're done performing actions

### 6. Play for Me (always available)

- Let the AI make a move for you
- Useful when learning the game or when stuck
- The AI uses the same Q-Learning strategy as computer players

## Valid Card Groups

You can only discard cards if they form one of these two valid group types:

### Sequence (Run)

**3 or more consecutive cards of the same color**

Examples:
- Blue 4, Blue 5, Blue 6 ✓
- Red 1, Red 2, Red 3, Red 4 ✓
- Green 7, Green 8, Green 9 ✓

Invalid:
- Blue 4, Blue 6, Blue 7 ✗ (not consecutive)
- Blue 4, Red 5, Green 6 ✗ (different colors)

### Set

**4 or more cards of the same number with different colors**

All colors must be unique (no duplicate colors allowed).

Examples:
- Blue 4, Green 4, Red 4, Yellow 4 ✓
- Red 7, Blue 7, Black 7, Green 7, Yellow 7 ✓

Invalid:
- Blue 4, Red 4, Blue 4 ✗ (duplicate color)
- Blue 4, Green 4, Red 4 ✗ (only 3 cards, need at least 4)

## Win Condition

**The first player to empty their hand wins immediately!**

As soon as a player has 0 cards in their hand, the game ends and that player is declared the winner.

## Special Rules

### Card Recycling

- When you discard a group, those cards are shuffled back into the deck
- This means discarded cards can be drawn again later
- The deck is reshuffled after each discard action

### Hand Limit

- Maximum 20 cards per player
- If you have 20 cards, you cannot draw more
- The game enforces this limit automatically

### Computer Delay

- Computer players have a 1-second delay between actions
- This makes it easier to follow what's happening
- The AI uses Q-Learning to make strategic decisions

### Action Tracking

- Most actions can only be performed once per turn
- The "Discard Group" action can be performed unlimited times
- Action availability is reset at the start of each turn

## Strategy Tips

1. **Form groups early**: Try to collect cards that can form sequences or sets
2. **Watch opponents**: Steal from players with many cards
3. **Use Draw & Discard**: Cycle through cards when you need specific ones
4. **Discard often**: The more you discard, the closer you are to winning
5. **Watch the deck**: If the deck is low, be strategic about drawing
6. **Learn from AI**: Use "Play for Me" to see what the AI would do

## Game Flow Example

1. **Your turn starts** (black border around your hand)
2. **Draw 2 cards** from the deck
3. **Discard a group** (Blue 4, Blue 5, Blue 6)
4. **Discard another group** (Red 7, Blue 7, Green 7, Yellow 7)
5. **Click "Next Turn"** to end your turn
6. **Next player's turn** begins

---

For more information, see the [AI System](ai-system.md) documentation.

