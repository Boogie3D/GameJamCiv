'Functions for initializing game'

from random import seed, randint
from itertools import combinations

def init_resources():
    '''
    Initializes the statistics for a country, such as population, food,
    and industry
    '''
    seed()
    resources = {
        'population': randint(30, 60),
        'food': 60,
        'industry': 0
    }

    return resources

def init_relationships():
    '''
    Initalizes the country relationships from a range of 25 to 75.
    Relationship ranges:
    0-40: Enemy
    41-60: Neutral
    61-100: Ally
    '''

    seed()
    relationships = {}
    # Computer relationships
    for comb in combinations('ABCD', 2):
        relationships[''.join(comb)] = randint(25, 75)
    # Player-Computer relationships
    while True:
        cheese_count = 0
        for letter in 'ABCD':
            relationships[letter + 'P'] = randint(25, 75)
            # Count the number of initial allies
            # Retry initialization if the game is too easy
            cheese_count += (relationships[letter + 'P'] > 55)
        if cheese_count < 3:
            break
    return relationships

def init_names():
    'Asks the player to enter names for the other countries'
    names = []
    numeral = ['first', 'second', 'third', 'fourth']
    for index in range(4):
        while True:
            names.append(input("Enter the {0} country's name: ".format(numeral[index])))
            # Try again if invalid string
            if names[index] != '' and names[index] != 'You':
                break
            del names[index]
            print('Please try again.')
    return names
