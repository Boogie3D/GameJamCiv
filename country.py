'Class file for the countries in the game.'
from math import floor
import random
import init

class Country:
    'Base class for countries.'
    count = 4
    relationships = init.init_relationships()

    def __init__(self, name):
        "Initialize country's resources."
        self.name = name
        self.resources = init.init_resources()

    def attack(self, target):
        'Country attacks another country.'
        if self.name == 'You':
            print('You are attacking {1}!'.format(target.name))
        else:
            print('{0} is attacking {1}!'.format(self.name, target.name))
        random.seed()
        # Damage mostly 1-3, theoretical range is 0-12
        damage = floor(random.lognormvariate(1, 0.5))
        target.resources['population'] -= damage
        if damage == 0:
            # Randomized statements
            statement = [
                '{0} tried to attack {1}, but failed!'.format(self.name,
                                                              target.name),
                '{0} saw it coming a mile away!'.format(target.name),
                'A spy has warned {0} in advance!'.format(target.name)
            ]
            print(random.choice(statement), end=' ')
            print('No one was killed.')
        elif damage <= 4:
            print('{0} attacked {1}! \
                  {2} thousand were killed!'.format(self.name, target.name,
                                                    damage))
        elif damage <= 8:
            # Randomized statements
            statement = [
                '{0} launched missiles at {1}!'.format(self.name, target.name),
                '{0} surprise attacked {1}!'.format(self.name, target.name),
            ]
            print(random.choice(statement), end=' ')
            print('{0} thousand were killed!'.format(damage))
        else:
            print('A devastating nuclear attack! \
                  {0} thousand were wiped out!!!'.format(damage))

    def dual_attack(self, ally, target):
        'Country proposes dual attack on another country.'
        pass

    def trade(self, target):
        'Country proposes a trade.'
        pass

    def gather(self):
        'Country gathers resources.'
        pass


class Player(Country):
    'Class for the player country.'
    def take_turn(self):
        'Player takes his/her turn.'
        pass

    def check_status(self):
        '''
        Player checks his/her status in the game, displaying each country's \
        disposition to the player and each country's power.
        '''


class Computer(Country):
    'Class for the computer country'
    def take_turn(self):
        'Computer takes its turn'
        pass
