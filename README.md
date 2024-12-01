# Connect-4-Minimax
Program:
A Connect 4 game with one single AI bot(using Minimax Alpha beta pruning and two evaluation functions) against a human player. The game is entirely played on the terminal where 1 is the human player piece and 2 is the AI player piece

Layout of Code:
In the first 8 function define the connect 4 game such as the creating the board, dropping the pieces and if there is 4 consecutive cells for a win. The last few functions define the AI player and the minimax alpha-beta pruning algorithm. The last part of the code is the game logic where the game is played.

How to interact with the program:
The human player types in a number (0-6) to drop a piece in the corresponding column. The human player keeps playing against the AI until one of them wins.

What does each file do?
The readme file contains the description of the code and how to run it. The connect4.py has all the game logic and the AI bot utilizing a minimax algorithm where the human player can run it and play against the AI bot

Python Libraries Used: numpy, math, random (need to install numpy)
```
pip install numpy
```
To run the program
```
python connect4.py
```
