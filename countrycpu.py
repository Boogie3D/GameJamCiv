'Class file for a CPU player.'
from random import seed, randint, choice, lognormvariate
from country import Country, identity_key

class Computer(Country):
    'Class for the computer country.'
    def __init__(self, name, identity):
        super().__init__(name, identity)
        Country.__comp_count__ += 1

    def __die(self):
        Country.__comp_count__ -= 1
        del Country.__countries__[self.identity]

    def die(self):
        'Pseudo-deconstructor for a dead Computer player.'
        self.__die()

    def take_turn(self, context):
        'Computer takes its turn.'
        if context == 'init':
            self.__passive_gather__()
            if self.resources['population'] <= 0:
                return 'dead'
        choices = []
        enemies_count = self.enemies_count()
        enemies_list = self.__get_enemies_list__()
        allies_count = self.allies_count()
        allies_list = self.__get_allies_list__()

        # Choice logic
        for _ in range(enemies_count * 3 // 2):
            choices.append('attack')
            choices.append('attack')
            choices.append('charity')
            choices.append('diplomacy')
        for _ in range(4 - enemies_count):
            choices.append('trade')
            choices.append('trade')
            choices.append('diplomacy')
        if allies_count > 0:
            choices.append('trade')
            choices.append('diplomacy')
        if sum(self.__countries__['P'].resources.values()) > 150:
            choices.append('trade')
            choices.append('attack')
        if allies_list > 0 and enemies_list > 0:
            choices.append('dual attack')
        if allies_list > 1 and enemies_list > 1:
            choices.append('dual attack')
        if self.resources['food'] < 30 or self.resources['industry'] < 30:
            choices.append('gather')
        if self.resources['food'] < 20 or self.resources['industry'] < 20:
            choices.append('gather')
        if self.resources['food'] < 10 or self.resources['industry'] < 10:
            choices.append('gather')
            choices.append('gather')

        countries_list = self.__countries__.values()
        action = choice(choices)

        if action == 'trade':
            if self.resources['food'] < 10 or self.resources['industry'] < 10:
                return 'retry'
            trade_list = [c for c in countries_list if c.name not in enemies_list
                          and c.name != self.name]
            if not trade_list:
                return 'retry'
            self.trade(choice(trade_list))
        if action == 'diplomacy':
            diplomacy_list = [c for c in countries_list if c.name != self.name]
            self.diplomacy(choice(diplomacy_list))
        if action == 'charity':
            charity_list = [c for c in countries_list if c.name != self.name]
            if self.resources['food'] < 10 or self.resources['industry'] < 10:
                return 'retry'
            self.charity(choice(charity_list))
        if action == 'gather':
            self.gather()
        if action == 'attack':
            if self.resources['industry'] < 20:
                return 'retry'
            attack_list = [c for c in countries_list if c.name not in allies_list
                           and c.name != self.name]
            attack_target = choice(self.__get_enemies_list__())
            self.attack(attack_target)
            self.__relationship_bound__(attack_target)
        if action == 'dual attack':
            if self.resources['industry'] < 30:
                return 'retry'
            ally_target = choice(self.__get_allies_list__())
            attack_target = choice(self.__get_enemies_list__())
            self.dual_attack(ally_target, attack_target)
            self.__relationship_bound__(ally_target)
            self.__relationship_bound__(attack_target)
            ally_target.__relationship_bound__(attack_list)

    def trade(self, target):
        'Country proposes a trade.'
        seed()
        types = ['food', 'industry']
        send_type = choice(types)
        send_max = (self.resources[send_type] + 1) * 3 // 5
        rec_type = choice(types)
        rec_max = (target.resoures[rec_type] + 1) * 4 // 5
        self_target_key = identity_key(self, target)

        send_quant = randint(1, send_max)
        rec_quant = randint(max(1, send_max - randint(3, 10)),
                            min(rec_max, send_max + randint(3, 10)))

        if target.identity == 'P':
            while True:
                print('{0} wants to trade {1} tons of {2} for {3} tons of {4}.'.format(self.name,
                                                                                       send_quant,
                                                                                       send_type,
                                                                                       rec_quant,
                                                                                       rec_type))
                response = input('Do you accept this trade [y,N]? ').lower()
                if response in ('y', 'yes', 'n', 'no', ''):
                    if response in ('y', 'yes'):
                        print('Trade accepted.')
                        self.resources[send_type] -= send_quant
                        self.resources[rec_type] += rec_quant
                        target.resources[send_type] += send_quant
                        target.resources[rec_type] -= rec_quant
                        self.__relationships__[self_target_key] += 5
                    else:
                        print('Trade declined.')
                        self.__relationships__[self_target_key] -= 5
                    break
        else:
            print("{0} attempts to trade with {1}.".format(self.name, target.name))
            response = choice((True, True, True, False))
            if response:
                self.resources[send_type] -= send_quant
                self.resources[rec_type] += rec_quant
                target.resources[send_type] += send_quant
                target.resources[rec_type] -= rec_quant
                self.__relationships__[self_target_key] += 5
            else:
                self.__relationships__[self_target_key] -= 5

    def diplomacy(self, target):
        'Learn something about another country.'
        print('{0} sent a diplomat to {1}.'.format(self.name, target.name))
        if self.__relationships__[identity_key(self, target)] < 35:
            print("{0} sent {1}'s diplomat back.".format(target.name, self.name))
            return
        self_target_key = identity_key(self, target)
        self.__relationships__[self_target_key] += 3

    def charity(self, target):
        'Country gives to another country.'
        pass

    def gather(self):
        'Country gathers resources.'
        print('{0} gathers resources.'.format(self.name))
        gather_food = randint(10, 30)
        gather_industry = randint(5, 20)
        self.resources['food'] += gather_food
        self.resources['industry'] += gather_industry

    def attack(self, target):
        'Country attacks another country.'
        if self.identity == 'P':
            print('You are attacking {1}!'.format(target.name))
        else:
            print('{0} is attacking {1}!'.format(self.name, target.name))
        seed()
        # Damage mostly 1-3, theoretical range is 0-12
        damage = int(lognormvariate(1, 0.5))
        # This may change
        industry_drain = damage * 3 // 2
        if industry_drain > self.resources['industry']:
            industry_drain = self.resources['industry']
        self.resources['industry'] = max(0, self.resources['industry']
                                         - industry_drain)
        target.resources['population'] -= damage
        if damage == 0:
            # Randomized statements
            statement = [
                '{0} tried to attack {1}, but failed!'.format(self.name,
                                                              target.name),
                '{0} saw it coming a mile away!'.format(target.name),
                'A spy warned {0} of the attack!'.format(target.name)
            ]
            print(choice(statement), end=' ')
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
            print(choice(statement), end=' ')
            print('{0} thousand were killed!'.format(damage))
        else:
            print('A devastating nuclear attack unleashes hell!')
            print('{0} thousand were wiped out!!!'.format(damage))
        if self.identity == 'P':
            print('Your industrial resources are now {0} thousand tons.'.format(
                self.resources['industry']))
        relationship_drain = 5 + damage * 2
        self.__relationships__[identity_key(self, target)] -= relationship_drain

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
            response_calc = (self.__relationships__[identity_key(self, ally)]
                             - randint(0, 10)
                             - self.__relationships__[identity_key(ally, target)]
                             // 2)
            # This may change
            if response_calc > 30:
                print('{0} agrees to attack {1}.'.format(ally.name,
                                                         target.name))
            else:
                print('{0} refuses to attack {1}.'.format(ally.name,
                                                          target.name))
                return

        damage = int(lognormvariate(2, 0.4))
        industry_drain = damage * 3 // 4
        self.resources['industry'] = max(0, self.resources['industry']
                                         - industry_drain)
        ally.resources['industry'] = max(0, ally.resources['industry']
                                         - industry_drain)
        target.resources['population'] -= damage
        relationship_drain = 10 + damage * 2
        self.__relationships__[identity_key(self, target)] -= relationship_drain
        self.__relationships__[identity_key(ally, target)] -= relationship_drain

        if damage == 0:
            print('Somehow, you both failed to kill anyone!')
        elif damage <= 4:
            statement = [
                'Bombs rain down from above!'
                'Soldiers storm the mainland!'
            ]
            print(choice(statement))
            print('{0} thousand were killed!'.format(damage))
        elif damage <= 14:
            statement = [
                'Tactile missiles strike from two sides!'
                'Soldiers overwhelm {0}, wreaking havoc!'.format(target.name)
            ]
            print(choice(statement))
            print('{0} thousand were killed!'.format(damage))
        else:
            print('Dual nuclear strikes obliterate the enemy!')
            print('{0} thousand are now dust!!!'.format(damage))
        if self.identity == 'P':
            print('Your resources are now {0}.'.format(self.resources['industry']))
        elif ally.identity == 'P':
            print('Your resources are now {0}.'.format(ally.resources['industry']))