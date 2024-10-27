# Fianco AI
This project was developed for the Intelligent Search and Games course @ Maastricht University. The goal was to create a playable version of [Fianco](http://www.di.fc.ul.pt/~jpn/gv/fianco.htm) along with an AI engine by utilizing the Negamax alpha-beta pruning search algorithm and other features learned during the lectures.

## Game rules
1.	The game is played on a 9x9 board.
2.	Two players take turns: Player 1 (White) and Player 2 (Black).
3.	Players can move their pieces forward, left, or right to adjacent empty squares.
4.	Pieces can capture by jumping diagonally over an opponent’s piece.
5.	Capturing is mandatory when available.
6.	A player wins by either:
	-	Moving a piece to the opponent’s starting row.
	-	Capturing all opponent pieces.
	-	Preventing the opponent from making any legal moves.

## Features
- [x] Negamax with alpha beta pruning algorithm
    *   [x] Iterative Deepening Search (IDS)
    *   [x] Quiescence Search (QS)
    *   [x] Principal Variation Search (PVS)
    *   [x] Killer Moves
- [x] Transposition Table
- [x] GUI 

## Installation
In order to run the project locally it is suggested to use a Python Virtual Environment and install the dependencies in the _requirements.txt_ file.

## Usage
Run the game by executing:
```bash
python gui.py
```
Follow the on-screen instructions to choose your players and start the game.

### Controls
- Click on a piece to select it.
- Click on a valid square to move the selected piece.
- Q Key to quit the game.
- R Key to restart and choose new player modes.

## Contributors
- **Salvatore Pascarella** - Developed the game and AI engine as part of the Intelligent Search and Games course at Maastricht University.

## License
This project is licensed under the [GNU General Public License v3.0](./LICENSE). You are free to use, modify, and distribute this software under the terms of the GPL-3.0.












