#! /usr/bin/env python3
'''Main runtime file for game'''

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

if __name__ == '__main__':
    exit(main())
