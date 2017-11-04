#! /usr/env python3
'''Main runtime file for game'''

from init import ask_names
from init import welcome

def main():
    'Main'
    welcome()
    countries = ask_names()

if __name__ == '__main__':
    exit(main())
