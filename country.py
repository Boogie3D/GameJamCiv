'Class file for the countries in the game.'
from math import floor
import random
import init

class Country:
    'Base class for countries.'
    count = 4
    relationships = init.init_relationships()

    def __init__(self, name, identity):
        "Initialize country's resources."
        self.name = name
        self.identity = identity
        self.resources = init.init_resources()

    def attack(self, target):
        'Country attacks another country.'
        if self.identity == 'P':
            print('You are attacking {1}!'.format(target.name))
        else:
            print('{0} is attacking {1}!'.format(self.name, target.name))
        random.seed()
        # Damage mostly 1-3, theoretical range is 0-12
        damage = floor(random.lognormvariate(1, 0.5))
        # This may change
        industry_drain = damage * 3 // 2
        if industry_drain > self.resources['industry']:
            industry_drain = self.resources['industry']
        self.resources['industry'] -= industry_drain
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
            print('{0} attacked {1}! {2} thousand were killed!'.format(self.name,
                                                                       target.name,
                                                                       damage))
        elif damage <= 8:
            # Randomized statements
            statement = [
                '{0} launched missiles at {1}!'.format(self.name, target.name),
                '{0} surprise-attacked {1}!'.format(self.name, target.name),
            ]
            print(random.choice(statement), end=' ')
            print('{0} thousand were killed!'.format(damage))
        else:
            print('A devastating nuclear attack unleashes hell!')
            print('{0} thousand were wiped out!!!'.format(damage))
        if self.identity == 'P':
            print('Your industrial resources are now {0} thousand tons.'.format(
                self.resources['industry']))
        relationship_drain = 5 + damage * 2
        self.relationships[''.join(sorted(self.identity + target.identity))] -= relationship_drain

    def dual_attack(self, ally, target):
        'Country proposes dual attack on another country.'
        if self.identity == 'P':
            print('You propose to attack {0} with {1}'.format(target.name,
                                                              ally.name))
        else:
            print('{0} proposes to attack {1} with {2}'.format(self.name,
                                                               target.name,
                                                               ally.name))
        if ally.identity == 'P':
            while True:
                ally_response = input('Do you accept [y,N]? ').lower()
                if ally_response in ('y', 'yes', 'n', 'no'):
                    break
            if ally_response in ('y', 'yes'):
                print('You agree to attack {0} with {1}'.format(target.name,
                                                                ally.name))
            else:
                print('You refuse to attack {0}'.format(target.name))
                return
        else:
            # Calculate ally response
            response_calc = (self.relationships[''.join(sorted(self.identity
                                                               + ally.identity))]
                             - random.randint(0, 10)
                             - self.relationships[''.join(sorted(ally.identity
                                                                 + target.identity))]
                             // 2)
            # This may change
            if response_calc > 30:
                print('{0} agrees to attack {1}.'.format(ally.name,
                                                         target.name))
            else:
                print('{0} refuses to attack {1}.'.format(ally.name,
                                                          target.name))
                return

        damage = floor(random.lognormvariate(2, 0.4))
        industry_drain = damage * 3 // 4
        self.resources['industry'] = max(0, self.resources['industry']
                                         - industry_drain)
        ally.resources['industry'] = max(0, ally.resources['industry']
                                         - industry_drain)
        target.resources['population'] -= damage
        relationship_drain = 10 + damage * 2
        self.relationships[''.join(sorted(self.identity + target.identity))] -= relationship_drain
        self.relationships[''.join(sorted(ally.identity + target.identity))] -= relationship_drain

        if damage == 0:
            print('Somehow, you both failed to kill anyone!')
        elif damage <= 4:
            statement = [
                'Bombs rain down from above!'
                'Soldiers storm the mainland!'
            ]
            print(random.choice(statement))
            print('{0} thousand were killed!'.format(damage))
        elif damage <= 14:
            statement = [
                'Tactile missiles strike from two sides!'
                'Soldiers overwhelm {0}, wreaking havoc!'.format(target.name)
            ]
            print(random.choice(statement))
            print('{0} thousand were killed!'.format(damage))
        else:
            print('Dual nuclear strikes obliterate the enemy!')
            print('{0} thousand are now dust!!!'.format(damage))
        if self.identity == 'P':
            print('Your resources are now {0}.'.format(self.resources['industry']))
        elif ally.identity == 'P':
            print('Your resources are now {0}.'.format(ally.resources['industry']))

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

    def diplomacy(self, target):
        'Learn something about another country.'
        pass

    def check_status(self):
        '''
        Player checks his/her status in the game, displaying each country's \
        disposition to the player and each country's power.
        '''
        pass


class Computer(Country):
    'Class for the computer country'
    def take_turn(self):
        'Computer takes its turn'
        pass
