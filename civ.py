#! /usr/bin/env python3
'''Main runtime file for game'''

try:
    import pygame
except ImportError as exc:
    print("Please install the '{0}' module.".format(exc.name))
    print('i.e. [sudo] pip install {0}'.format(exc.name))
    exit(1)

import countrycpu
import countryplayer
from init import init_names

def main():
    'Runtime function for game.'
    welcome()
    country_names = init_names()
    print('')
    # Initalize countries and player
    player = countryplayer.Player('you', 'P')
    country_a = countrycpu.Computer(country_names[0], 'A')
    country_b = countrycpu.Computer(country_names[1], 'B')
    country_c = countrycpu.Computer(country_names[2], 'C')
    country_d = countrycpu.Computer(country_names[3], 'D')
    countries = [player, country_a, country_b, country_c, country_d]
    # Game should start here
    player.check_status()
    running = True
    while running:
        for active in countries:
            status = 'init'
            while True:
                status = active.take_turn(status)
                if status != 'retry':
                    break
            if status == 'quit':
                running = False
                print('Goodbye.')
                break
            if active == player and status == 'dead':
                lose()
                running = False
                break
            elif (player.__comp_count__ == 0
                  or player.allies_count() > player.__comp_count__ // 2):
                win()
                running = False
                break
            if active != player and status == 'dead':
                active.die()
            input('<Press Enter to continue>')
            print('')
    if status != 'quit':
        input('<Press Enter to continue>')
    return 0

def welcome():
    'Displays a welcome message and the game instructions.'

    print('''
Welcome to Kid Deyer's NOT Civilization: An Orignal Game (Do Not Steal)!

You are the leader of a great country in a tiny world.
There are only four other countries on this vicious little planet.
You may become allies or enemies with any of these countries.

Each country has a number of resources:

Population: The manpower of a country.

Food: Substinence for a country's people. If food runs low, the
population will begin to dwindle.

Industry: The strength of a country's industry determines whether
it is capable of attacking or defending itself.

Resources will always passively increase of each round, with the exception of
the population, which will decrease if food is too low.

If a country's population drops to 0, it is permanently destroyed.
If your population drops to 0, you lose.
''')

    input('<Press Enter to continue>')

    print('''
Each surviving country will take a turn and may perform one of the
following actions:

Trade: Trade resources with another country.

Attack: Attack another country.

Dual Attack: Propose a dual attack with an allied country on another
country.

Gather: Gather additional resources.

Diplomacy: Send a diplomat to learn something about a country.

Charity: Send a country a gift.
''')

    input('<Press Enter to continue>')

    print('''
The following action is unique to the player:

Check Status: List the number of resources owned and the countries
that are allied with you.

To win, become allies with more than half of the remaining
countries.
''')

    input('<Press Enter to continue>')

    print('')

def win():
    'Subroutines for winning a game'
    print('''
What a humanitarian! You've united half the world!

Congratulations! You win!
''')

def lose():
    'Subroutines for losing a game'
    print('''
Your time has run out. Your towns lay empty, your nation is a wasteland.
All that remains is the charred and starving bodies of your former populace.

Sorry! You lose!
''')

if __name__ == '__main__':
    exit(main())
