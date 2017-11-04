'Functions for initializing game'

from random import seed
from random import randint

def init_resources():
    '''
    Initializes the statistics for a country, such as population, food, and \
    industry
    '''
    seed()
    resources = {}
    resources['population'] = randint(30, 60)
    resources['food'] = 60
    resources['industry'] = 0

    return resources

def init_relationships():
    'Initalizes the country relationships from a range of 25 to 75'
    seed()
    relationships = {}
    while True:
        relationships['p_a'] = randint(25, 75)
        relationships['p_b'] = randint(25, 75)
        relationships['p_c'] = randint(25, 75)
        relationships['p_d'] = randint(25, 75)
        if relationships['p_a'] + relationships['p_b'] + relationships['p_c'] < 182 and \
        relationships['p_a'] + relationships['p_b'] + relationships['p_d'] < 182 and \
        relationships['p_a'] + relationships['p_c'] + relationships['p_d'] < 182 and \
        relationships['p_b'] + relationships['p_c'] + relationships['p_d'] < 182:
            break
    relationships['a_b'] = randint(25, 75)
    relationships['a_c'] = randint(25, 75)
    relationships['a_d'] = randint(25, 75)
    relationships['b_c'] = randint(25, 75)
    relationships['b_d'] = randint(25, 75)
    relationships['c_d'] = randint(25, 75)

    return relationships

def welcome():
    'Displays a welcome message and the game instructions.'
    print('Welcome to GAME!')
    print('You are the leader of a country.')
    print('There are four other countries.')
    print('You can become allies or enemies with any of the four countries.')
    print('Each country has a number of resources.')
    print('''Each country takes a turn and can perform one of the following
          actions:''')
    print('Trade: Trade resources with another country.')
    print('Attack: Attack another country.')
    print('''Dual Attack: Propose a dual attack with an allied country on
          another country.''')
    print('Gather: Gather additional resources.')
    print('''To win, become allies with more than half of the remaining
          countries.''')
def ask_names():
    'Asks the player to enter names for the other countries'
    names = {}
    while True:
        names['A'] = input("Enter the first country's name: ")
        if names['A'] != '':
            break
        print('Please try again.')
    while True:
        names['B'] = input("Enter the second country's name: ")
        if names['B'] != '':
            break
        print('Please try again.')
    while True:
        names['C'] = input("Enter the third country's name: ")
        if names['C'] != '':
            break
        print('Please try again.')
    while True:
        names['D'] = input("Enter the fourth country's name: ")
        if names['D'] != '':
            break
        print('Please try again.')

    return names
