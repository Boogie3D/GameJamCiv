'Class file for the countries in the game.'
from math import floor
import random
import init
import gameutils

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
        self.relationships[gameutils.identity_key(self, target)] -= relationship_drain

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
                if ally_response in ('y', 'yes', 'n', 'no', ''):
                    break
            if ally_response in ('y', 'yes'):
                print('You agree to attack {0} with {1}'.format(target.name,
                                                                ally.name))
            else:
                print('You refuse to attack {0}'.format(target.name))
                return
        else:
            # Calculate ally response
            response_calc = (self.relationships[gameutils.identity_key(self, ally)]
                             - random.randint(0, 10)
                             - self.relationships[gameutils.identity_key(ally, target)]
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
        self.relationships[gameutils.identity_key(self, target)] -= relationship_drain
        self.relationships[gameutils.identity_key(ally, target)] -= relationship_drain

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
        types = ['food', 'industry']
        if self.identity == 'P':
            print('What do you want to trade?')
            print('(1) Food')
            print('(2) Industrial Resources')
            while True:
                send_input = input('>> ')
                if send_input in ('1', '2'):
                    send_type = types[send_input - 1]
                    break
                print('Invalid choice.')
            print('How much?')
            while True:
                try:
                    send_quant = int(input('>> '))
                except ValueError:
                    print('Invalid input.')
                    continue
                if send_quant <= self.resources[send_type]:
                    break
                print('Invalid quantity.')

            print('What do you want in return?')
            print('(1) Food')
            print('(2) Indusrial Resources')
            while True:
                rec_input = input('>> ')
                if rec_input in ('1', '2'):
                    rec_type = types[rec_input - 1]
                    break
                print('Invalid choice.')
            print('How much?')
            while True:
                try:
                    rec_quant = int(input('>> '))
                except ValueError:
                    print('Invalid input.')
                    continue
                if (rec_quant > target.resources[rec_type]
                        or rec_quant > send_quant
                        or self.relationships[gameutils.identity_key(self, target)]
                        + random.randint(0, 20)):
                    print('{0} refuses your trade.'.format(target.name))
                    self.relationships[gameutils.identity_key(self, target)] -= 5
                else:
                    print('{0} accepts your trade.'.format(target.name))
                    self.resources[send_type] -= send_quant
                    self.resources[rec_type] += rec_quant
                    target.resources[send_type] += send_quant
                    target.resources[rec_type] -= rec_quant
                    self.relationships[gameutils.identity_key(self, target)] += 5
        else:
            send_type = random.choice(types)
            send_quant = random.randint(1, self.resources[send_type] - 10)
            rec_type = random.choice(types)
            rec_quant = random.randint(1, target.resources[rec_type])
            print('{0} wants to trade {1} tons of {2} for {3} tons of {4}.'.format(self.name,
                                                                                   send_quant,
                                                                                   send_type,
                                                                                   rec_quant,
                                                                                   rec_type))
            while True:
                response = input('Do you accept this trade [y,N]? ').lower()
                if response in ('y', 'yes', 'n', 'no', ''):
                    if response in ('y', 'yes'):
                        print('Trade accepted.')
                        self.resources[send_type] -= send_quant
                        self.resources[rec_type] += rec_quant
                        target.resources[send_type] += send_quant
                        target.resources[rec_type] -= rec_quant
                        self.relationships[gameutils.identity_key(self, target)] += 5
                    else:
                        print('Trade declined.')
                        self.relationships[gameutils.identity_key(self, target)] -= 5
                    break

    def gather(self):
        'Country gathers resources.'
        gather_food = random.randint(10, 30)
        gather_industry = random.randint(5, 20)
        self.resources['food'] += gather_food
        self.resources['industry'] += gather_industry
        if self.identity == 'P':
            print('You gather the following resources:')
            print('Food: {0} thousand tons'.format(gather_food))
            print('Industrial Resources: {0} thousand tons'.format(gather_industry))
        else:
            print('{0} gathers resources.'.format(self.name))


class Player(Country):
    'Class for the player country.'
    def take_turn(self):
        'Player takes his/her turn.'
        pass

    def diplomacy(self, target):
        'Learn something about another country.'
        if self.relationships[gameutils.identity_key(self, target)] < 40:
            print('{0} refused your diplomat'.format(target.name))
            return
        learn_target = random.choice(['population', 'food', 'industry', 'allies', 'enemies'])
        print('Your diplomat returned.')
        if learn_target == 'population':
            print("{0}'s population is {1} thousand.".format(target.name,
                                                             target.resources['population']))
        elif learn_target == 'food':
            print('{0} has {1} thousand tons of food.'.format(target.name,
                                                              target.resources['food']))
        elif learn_target == 'industry':
            print('{0} has {1} thousand tons of industrial resources.'.format(
                target.name, target.resources['industry']))
        elif learn_target == 'allies':
            print('{0} has {1} allies.'.format(target.name, gameutils.get_allies(target)))
        elif learn_target == 'enemies':
            print('{0} has {1} enemies.'.format(target.name, gameutils.get_enemies(target)))

    def charity(self, target):
        'Give a country a gift.'
        types = ['food', 'industry']
        print('What will you give?')
        print('(1) Food')
        print('(2) Industrial Resources')
        while True:
            send_res = input('>> ')
            if send_res in ('1', '2'):
                send_type = types[send_res - 1]
                break
            print('Invalid choice.')
        print('How much will you give?')
        while True:
            try:
                send_quant = int(input('>> '))
            except ValueError:
                print('Invalid input.')
                continue
            if send_quant <= self.resources[send_type]:
                break
        if send_quant == 0:
            print("You don't have anything to give.")
            return
        print('{0} sends its regards.'.format(target.name))
        self.resources[send_type] -= send_quant
        target.resources[send_type] += send_quant
        self.relationships[gameutils.identity_key(self, target)] += send_quant // 4

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
