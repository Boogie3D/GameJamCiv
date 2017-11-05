#! /usr/bin/env python3
'''Main runtime file for game'''

try:
    import pygame
except ImportError as exc:
    print("Please install the '{0}' module.".format(exc.name))
    print('i.e. [sudo] pip install {0}'.format(exc.name))
    exit(1)

import country
from init import ask_names, welcome

def main():
    'Main'
    welcome()
    country_names = ask_names()
    # Initalize countries and player
    player = country.Player('You', 'P')
    country_a = country.Computer(country_names[0], 'A')
    country_b = country.Computer(country_names[1], 'B')
    country_c = country.Computer(country_names[2], 'C')
    country_d = country.Computer(country_names[3], 'D')
    all_players = [player, country_a, country_b, country_c, country_d]
    current = player
    # Game should start here

    return 0

if __name__ == '__main__':
    exit(main())
