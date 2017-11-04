#! /usr/bin/env python3
'''Main runtime file for game'''

try:
    import pygame
except ImportError as exc:
    print("Please install the '{0}' module.".format(exc.name))
    print('i.e. [sudo] pip install {0}'.format(exc.name))
    exit(1)

import country
from init import ask_names
from init import welcome

def main():
    'Main'
    welcome()
    countries = ask_names()
    country_a = country.Computer(countries['A'])
    country_b = country.Computer(countries['B'])
    country_c = country.Computer(countries['C'])
    country_d = country.Computer(countries['D'])

    return 0

if __name__ == '__main__':
    exit(main())
