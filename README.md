# Kid Deyer's Societies: Readme #

### To run the game, execute the file civ.py in a Python 3.x shell. ###

## Purpose ##
This is a text-based game inspired by Sid Meier's Civilization. It was written entirely in
Python 3 for a 48-hour Game Jam--the major theme of which was "Interconnected Worlds" with a minor theme of "Problems that can
be solved with violence but shouldn't be"--hosted by the New Mexico Tech ACM Chapter. As the game was made during a Game Jam, no
further updates are planned.

## Graphics ##
The game features no graphics, although originally graphics were planned to be implemented with Pygame. Some early pixel art may
be found in the 'concept_art' directory. The game is text-based and is played directly in a Python 3.x shell.

## Gameplay ##
The game revolves around the relations of 5 "countries," one of which is controlled by the player. The objective of the game is
to either become allied with at least half the remaining other countries (i.e. 3 if all 5 countries are alive, 2 if 4 are alive,
etc.). This entails choosing diplomacy or war. The specific rules of the game are explained upon launching the game.

## Bugs and Exceptions ##
Currently, if another country chooses to perform a "Dual Attack" without any allies with which to attack, an exception may be
raised. There is no plan to fix this.

## Style Issues ##
The answer to the following concerns about the coding style is simply that the code was written in a total of 37 hours from
scratch mostly by one person; there was no time to try to significantly improve the style, let alone implement graphics,
after the initial program structure was decided.
### Concerns: ###
* The code is too long.
* The code is too complex.
* The code contains statements nested too far.
* Code is re-used too often.
* The dictionary reference system is convoluted.
