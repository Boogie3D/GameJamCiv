#! /usr/bin/env python3
'''Main runtime file for game'''

try:
    import pygame
except ImportError as exc:
    print("Please install the '{0}' module.".format(exc.name))
    print('i.e. [sudo] pip install {0}'.format(exc.name))
    exit(1)

import country
from init import init_names

def main():
    'Main'
    welcome()
    country_names = init_names()
    print('')
    # Initalize countries and player
    player = country.Player('You', 'P')
    country_a = country.Computer(country_names[0], 'A')
    country_b = country.Computer(country_names[1], 'B')
    country_c = country.Computer(country_names[2], 'C')
    country_d = country.Computer(country_names[3], 'D')
    countries = [player, country_a, country_b, country_c, country_d]
    # Game should start here
    player.check_status()
    running = True
    while running:
        for active in countries:
            while True:
                print(player.__comp_count__)
                status = active.take_turn()
                if status != 'retry':
                    break
            if active == player and status == 'dead':
                lose()
                running = False
            if active != player and status == 'dead':
                active.die()
            if (player.__comp_count__ == 0
                    or player.allies_count > player.__comp_count__ // 2):
                win()
                running = False
            if active != player:
                input('<Press Enter to continue')
    return 0

def welcome():
    'Displays a welcome message and the game instructions.'

    print('''
Welcome to GAME!

You are the leader of a great country in a tiny world.
There are only four other countries on this vicious little planet.
You may become allies or enemies with any of these countries.

Each country has a number of resources:

Population: The manpower of a country.

Food: Substinence for a country's people. If food runs low, the
population will begin to dwindle.

Industry: The strength of a country's industry determines whether
it is capable of attacking or defending itself.

Resources may passively increase or decrease at the beginning of
each round.
If a country's population drops to 0, it is permanently destroyed.
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
    pass

def lose():
    'Subroutines for losing a game'
    pass

if __name__ == '__main__':
    exit(main())
