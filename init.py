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
    for comb in combinations("ABCD", 2):
        relationships[comb] = randint(25, 75)
    # Player-Computer relationships
    while True:
        relationships['p-a'] = randint(25, 75)
        relationships['p-b'] = randint(25, 75)
        relationships['p-c'] = randint(25, 75)
        relationships['p-d'] = randint(25, 75)
        # Count the number of initial allies
        # Retry initialization if the win condition is
        # prematurely satisfied
        ally_count = ((relationships['p-a'] > 60)
                      + (relationships['p-b'] > 60)
                      + (relationships['p-c'] > 60)
                      + (relationships['p-d'] > 60))
        if ally_count < 3:
            break

    return relationships

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

Check Status: List the number of resources owned and the countries
that are allied with you. (Unique to the player)

To win, become allies with more than half of the remaining
countries.
''')

    input('<Press Enter to continue>')

    print('')

def ask_names():
    'Asks the player to enter names for the other countries'
    names = []
    numeral = ['first', 'second', 'third', 'fourth']
    for index in range(4):
        while True:
            names.append(input("Enter the {0} country's name: ".format(numeral[index])))
            if names[index] != '':
                break
            # Try again if empty string
            del names[index]
            print('Please try again.')

    return names
