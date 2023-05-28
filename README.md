# ChessAI-v2.0

This is the README file for an AI Chess Program. This program allows you to play chess against an AI opponent or against another human player. It is built using Python and the Pygame library.

## Features

- Play chess against an AI opponent or against another human player.
- Undo moves and reset the game.
- Change the player's turn and switch between playing as white or black.
- Customize the board colors.

## Requirements

- Python 3.11
- Pygame library

## Installation

1. Clone the repository or download the source code.
2. Install the Pygame library by running the following command:
   ```
   pip install pygame
   ```

## Usage

Run the following command to start the AI Chess Program:
```
python main.py
```

The game will open in a Pygame window. You can make moves by clicking on the chessboard squares. The program will validate the moves and update the game state accordingly. The move log is displayed on the right side of the window.

### Controls

- Mouse: Click on a piece and then click on a valid destination square to make a move.
- Keyboard:
  - 'u': Undo the last move.
  - 'r': Reset the game.
  - 'b': Switch to playing as black.
  - 'w': Switch to playing as white.
  - 'p': Switch to player vs. player mode.
  - '1': Set board colors to white and dark blue.
  - '2': Set board colors to white and gray.
  - '3': Set board colors to brown and beige.
  - '4': Set board colors to beige and dark olive green.
  - 'f': (Not implemented) Additional feature.

## Credits

This AI Chess Program is created by Vasishta Malisetty.

## License

The AI Chess Program is released under the [MIT License](https://opensource.org/licenses/MIT).
