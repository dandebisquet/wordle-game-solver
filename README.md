# Wordle Game + Solver (Information Theory Helper)

A terminal-based Wordle implementation in Python with two modes:

- **Game mode:** play Wordle in the console with colored feedback.
- **Helper mode:** get recommended guesses based on an information-theory style score and automatically narrow down the candidate list as you play.

The word list is fetched from a public Wordle list on GitHub at runtime.

## Features
- Play Wordle in the terminal (6 guesses)
- ANSI-colored feedback for each letter (green/yellow/gray style)
- Helper mode that:
  - recommends a guess with the highest estimated information
  - filters the candidate word list based on your previous guess feedback

## How it works (high level)
1. Downloads a list of valid Wordle words from a public repository.
2. Chooses a target word.
3. For each guess, computes Wordle-style feedback:
   - **green**: correct letter, correct position
   - **yellow**: correct letter, wrong position (with simple handling for repeats)
   - **gray**: letter not present (or already accounted for)
4. In **helper mode**, the program:
   - scores candidate guesses using a heuristic information score (`log2(probability)` style)
   - suggests the best-scoring word
   - removes impossible words from the candidate list after each guess

## Requirements
- Python 3.8+ recommended
- No external packages required (uses Python standard library only)

## Run
```bash
python wordle_solver.py
