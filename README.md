# Kid Deyer's Societies: Readme #

### To play the game, run civ.py in Python 3.X. ###

## Purpose ##
This is a text-based game inspired by Sid Meier's Civilization. It was written entirely in Python 3 for a 48-hour Game Jam--the major theme of which was "Interconnected Worlds" with a minor theme of "Problems that can be solved with violence but probably shouldn't be"--hosted by the New Mexico Tech ACM Chapter. As the game was made at the time by 3 undergraduates with none to novice Python experience during a Game Jam, the code is markedly unoptimized and un-Pythonic. No further updates are planned.

## Graphics ##
The game features no graphics, although originally graphics were planned to be implemented with Pygame. Some early concept pixel art is located in the 'concept_art' directory. The game is text-based and is played directly in an interactive shell.

## Gameplay ##
The game revolves around the relations of 5 "countries," one of which is controlled by the player. The objective of the game is
to either become allied with at least half the remaining other countries (i.e. 3 if all 5 countries are alive, 2 if 4 are alive,
etc.). This entails choosing diplomacy or war. The specific rules of the game are explained upon launching the game.

## Bugs and Exceptions ##
Currently, if another country chooses to perform a "Dual Attack" without any allies with which to attack, an exception may be
raised. There is no intention to fix this.

## Style Self-Critique ##
The answer to the following concerns about the coding style is simply that the code was written in a total of 39 hours from scratch; there was no time to try to make the code more "Pythonic," let alone implement actual graphics, after the initial program structure was decided.
### Immediate Issues: ###
* There is too much code.
* The code is too complex.
* The code contains excessively-nested statements.
* Code is re-used too often; sub-routines are sparse.
* The dictionary reference system is convoluted.
