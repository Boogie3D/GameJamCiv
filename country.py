'Class file for the countries in the game.'
from random import seed, randint, choice, lognormvariate
import init

class Country:
    'Base class for countries.'
    __comp_count__ = 0
    __relationships = init.init_relationships()
    __countries__ = {}

    def __init__(self, name, identity):
        "Initialize country's resources."
        self.name = name
        self.identity = identity
        self.resources = init.init_resources()
        self.__countries__[identity] = self

    def __get_name_from_key(self, key):
        identity = key.strip(self.identity)
        return self.__countries__[identity].name

    def __get_allies_list__(self):
        allied_countries = []
        for key, value in self.__relationships.items():
            if self.identity in key and value > 60:
                allied_countries.append(self.__get_name_from_key(key))
        return allied_countries

    def __get_enemies_list__(self):
        enemy_countries = []
        for key, value in self.__relationships.items():
            if self.identity in key and value < 40:
                enemy_countries.append(self.__get_name_from_key(key))
        return enemy_countries

    def __print_countries__(self):
        index = 1
        identity_list = sorted(list(self.__countries__.keys()))
        print_list = [c for c in identity_list if c != 'P']
        for identity in print_list:
            print('({0}) {1}'.format(index, self.__countries__[identity].name))
            index += 1

    def enemies_count(self):
        'Returns enemy count for a country.'
        enemy_count = 0
        for key, value in self.__relationships.items():
            if self.identity in key and value < 40:
                enemy_count += 1
        return enemy_count

    def allies_count(self):
        'Returns ally count for a country.'
        ally_count = 0
        for key, value in self.__relationships.items():
            if self.identity in key and value > 60:
                ally_count += 1
        return ally_count


class Player(Country):
    'Class for the player country.'
    def take_turn(self):
        'Player takes his/her turn.'
        print("It's your turn!")
        pop_gain = randint(1, 3) * (-1 if self.resources['food'] < 10 else 1)
        food_gain = randint(1, 7)
        industry_gain = randint(3, 10)
        self.resources['population'] += pop_gain
        self.resources['food'] += food_gain
        self.resources['industry'] += industry_gain
        if pop_gain > 0:
            print('You gain {0} thousand people.'.format(pop_gain))
        else:
            print('You lose {0} thousand people.'.format(-pop_gain))
            if self.resources['population'] <= 0:
                return 'dead'
        print('You gain {0} thousand tons of food.'.format(food_gain))
        print('You gain {0} thousand tons of industrial resources.'.format(industry_gain))
        print('What will you do?')
        while True:
            print('(1) Trade')
            print('(2) Diplomacy')
            print('(3) Gather Resources')
            print('(4) Charity')
            print('(5) Attack')
            print('(6) Dual Attack')
            print('(7) Show Status')
            print('(8) Quit')
            player_input = input('>> ')
            if player_input in ('1', '2', '3', '4', '5', '6', '7', '8'):
                break
            print('Invalid choice.')
        # Trade
        if player_input == '1':
            while True:
                print('Who will you trade with?')
                self.__print_countries__()
                try:
                    player_input = int(input('>> ')) - 1
                except ValueError:
                    print('Invalid input.')
                    continue
                if player_input in range(self.__comp_count__):
                    break
                print('Invalid choice.')
            country_identity = sorted(list(self.__countries__.keys()))[player_input]
            country_choice = self.__countries__[country_identity]
            self.trade(country_choice)
            self_country_key = identity_key(self, country_choice)
            if self.__relationships[self_country_key] > 100:
                self.__relationships[self_country_key] = 100
            elif self.__relationships[self_country_key] < 0:
                self.__relationships[self_country_key] = 0
        # Diplomacy
        elif player_input == '2':
            while True:
                print('Where will you send your diplomat?')
                self.__print_countries__()
                try:
                    player_input = int(input('>> '))
                except ValueError:
                    print('Invalid input.')
                    continue
                if player_input in range(self.__comp_count__):
                    break
                print('Invalid choice.')
            country_identity = sorted(list(self.__countries__.keys()))[player_input]
            country_choice = self.__countries__[country_identity]
            self.diplomacy(country_choice)
            self_country_key = identity_key(self, country_choice)
            if self.__relationships[self_country_key] > 100:
                self.__relationships[self_country_key] = 100
        # Gather Resources
        elif player_input == '3':
            self.gather()
        # Charity
        elif player_input == '4':
            while True:
                print('Who will you give to?')
                self.__print_countries__()
                try:
                    player_input = int(input('>> '))
                except ValueError:
                    print('Invalid input.')
                    continue
                if player_input in range(self.__comp_count__):
                    break
                print('Invalid choice.')
            country_identity = sorted(list(self.__countries__.keys()))[player_input]
            country_choice = self.__countries__[country_identity]
            self.charity(country_choice)
            self_country_key = identity_key(self, country_choice)
            if self.__relationships[self_country_key] > 100:
                self.__relationships[self_country_key] = 100
        # Attack
        elif player_input == '5':
            if self.resources['industry'] < 20:
                print('Not enough industrial resources.')
                return 'retry'
            while True:
                print('Who will you attack?')
                self.__print_countries__()
                player_input = input('>> ')
                if player_input in ('1', '2', '3', '4'):
                    break
                print('Invalid choice.')
            country_choice = self.__countries__[int(player_input)]
            self.attack(country_choice)
            self_country_key = identity_key(self, country_choice)
            if self.__relationships[self_country_key] < 0:
                self.__relationships[self_country_key] = 0
        # Dual Attack
        elif player_input == '6':
            if self.resources['industry'] < 30:
                print('Not enough industrial resources.')
                return 'retry'
            allies_list = self.__get_allies_list__()
            if not allies_list:
                print('You are alone in this world.')
                return 'retry'
            while True:
                print('Who will you attack?')
                self.__print_countries__()
                player_target = input('>> ')
                if player_target in ('1', '2', '3', '4'):
                    break
                print('Invalid choice.')
            country_target = self.__countries__[int(player_target)]
            while True:
                print('Who will join you?')
                for ally in allies_list:
                    print('({0}) {1}'.format(allies_list.index(ally) + 1, ally))
                player_ally = input('>> ')
                if player_ally in [str(x) for x in range(1, len(allies_list))]:
                    break
                print('Invalid choice.')
            for country in self.__countries__.values():
                if allies_list[int(player_ally)] == country.name:
                    country_ally = country
            if country_target == country_ally:
                print("A country can't help you attack it.")
                return 'retry'
            self.dual_attack(country_ally, country_target)
        # Check Status
        elif player_input == '7':
            self.check_status()
            return 'retry'
        # Quit
        elif player_input == '8':
            return 'quit'
        return 'alive'

    def trade(self, target):
        'Country proposes a trade.'
        types = ['food', 'industry']
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
                    or rec_quant + randint(0, 10) > send_quant
                    or self.__relationships[identity_key(self, target)]
                    + randint(0, 20) < 50):
                print('{0} refuses your trade.'.format(target.name))
                self.__relationships[identity_key(self, target)] -= 5
            else:
                print('{0} accepts your trade.'.format(target.name))
                self.resources[send_type] -= send_quant
                self.resources[rec_type] += rec_quant
                target.resources[send_type] += send_quant
                target.resources[rec_type] -= rec_quant
                self.__relationships[identity_key(self, target)] += send_quant // 5

    def diplomacy(self, target):
        'Learn something about another country.'
        if self.__relationships[identity_key(self, target)] < 35:
            print('{0} sent your diplomat back.'.format(target.name))
            return
        learn_target = choice(['population', 'food', 'industry', 'allies', 'enemies'])
        print('Your diplomat returned with new information:')
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
            print('{0} has {1} allies.'.format(target.name, target.allies_count()))
        elif learn_target == 'enemies':
            print('{0} has {1} enemies.'.format(target.name, target.enemies_count()))
        self.__relationships[identity_key(self, target)] += 3

    def gather(self):
        'Country gathers resources.'
        gather_food = int(lognormvariate(1.5, 0.4))
        gather_industry = int(lognormvariate(2, 0.4))
        self.resources['food'] += gather_food
        self.resources['industry'] += gather_industry
        print('You gather the following resources:')
        print('Food: {0} thousand tons'.format(gather_food))
        print('Industrial Resources: {0} thousand tons'.format(gather_industry))

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
        self.__relationships[identity_key(self, target)] += send_quant // 4

    def attack(self, target):
        'Country attacks another country.'
        print('You are attacking {1}!'.format(target.name))
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
                'You tried to attack {1}, but failed!'.format(target.name),
                '{0} saw it coming a mile away!'.format(target.name),
                'A spy has warned {0} of your attack!'.format(target.name)
            ]
            print(choice(statement), end=' ')
            print('No one was killed.')
        elif damage <= 4:
            print('You attacked {1}! {2} thousand were killed!'.format(target.name,
                                                                       damage))
        elif damage <= 8:
            # Randomized statements
            statement = [
                'You launched missiles at {1}!'.format(target.name),
                'You surprise-attacked {1}!'.format(target.name),
            ]
            print(choice(statement), end=' ')
            print('{0} thousand were killed!'.format(damage))
        else:
            print('A devastating nuclear attack unleashed hell!')
            print('{0} thousand were wiped out!!!'.format(damage))
        print('Your industrial resources are now {0} thousand tons.'.format(
            self.resources['industry']))
        relationship_drain = 5 + damage * 2
        self.__relationships[identity_key(self, target)] -= relationship_drain

    def dual_attack(self, ally, target):
        'Country proposes dual attack on another country.'
        print('You propose to attack {0} with {1}'.format(target.name,
                                                          ally.name))
        self_ally_key = identity_key(self, ally)
        self_target_key = identity_key(self, target)
        ally_target_key = identity_key(ally, target)
        # Calculate ally response
        response_calc = (self.__relationships[self_ally_key]
                         - randint(0, 5)
                         - self.__relationships[ally_target_key]
                         // 2)
        # This may change
        if response_calc > 42:
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
        relationship_drain = 7 + damage * 2
        self.__relationships[self_target_key] -= relationship_drain
        self.__relationships[ally_target_key] -= relationship_drain

        if damage == 0:
            print('Somehow, you both failed to kill anyone!')
        elif damage <= 4:
            statement = [
                'Your bombs rain down from above!'
                'Your soldiers storm the mainland!'
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
        print('Your resources are now {0}.'.format(self.resources['industry']))

    def check_status(self):
        '''
        Player checks his/her status in the game, displaying each country's
        disposition to the player and each country's power.
        '''
        print('Population: {0} thousand'.format(self.resources['population']))
        print('Food: {0} thousand tons'.format(self.resources['food']))
        print('Industrial Resources: {0} thousand tons'.format(self.resources['industry']))
        print('Allies:')
        allies_list = self.__get_allies_list__()
        for ally in allies_list:
            print(ally)
        if not allies_list:
            print('You are alone in this world.')


class Computer(Country):
    'Class for the computer country'
    def __init__(self, name, identity):
        super().__init__(name, identity)
        self.__comp_count__ += 1

    def __die(self):
        del self.__countries__[self.identity]

    def die(self):
        'Pseudo-deconstructor for a dead Computer player.'
        self.__comp_count__ -= 1
        self.__die()

    def take_turn(self):
        'Computer takes its turn'
        pop_gain = randint(1, 3) * (-1 if self.resources['food'] < 10 else 1)
        food_gain = randint(1, 4)
        industry_gain = randint(1, 3)
        self.resources['population'] += pop_gain
        self.resources['food'] += food_gain
        self.resources['industry'] += industry_gain
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
        if sum(self.__countries__['P'].resources.values() > 150):
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
            if self.resources['food'] < 10 or self.resources['industry'] < 10:
                return 'retry'
            self.charity(choice(countries_list))
        if action == 'gather':
            self.gather()
        if action == 'attack':
            if self.resources['industry'] < 20:
                return 'retry'
            attack_list = [c for c in countries_list if c.name not in allies_list
                           and c.name != self.name]
            if not attack_list:
                return 'retry'
            self.attack(choice(attack_list))
        if action == 'dual attack':
            if self.resources['industry'] < 30:
                return 'retry'
            attack_list = [c for c in countries_list if c.name not in enemies_list
                           and c.name != self.name]
            if not attack_list:
                return 'retry'

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
                        self.__relationships[self_target_key] += 5
                    else:
                        print('Trade declined.')
                        self.__relationships[self_target_key] -= 5
                    break
        else:
            print("{0} attempts to trade with {1}.".format(self.name, target.name))
            response = choice((True, True, True, False))
            if response:
                self.resources[send_type] -= send_quant
                self.resources[rec_type] += rec_quant
                target.resources[send_type] += send_quant
                target.resources[rec_type] -= rec_quant
                self.__relationships[self_target_key] += 5
            else:
                self.__relationships[self_target_key] -= 5

    def diplomacy(self, target):
        'Learn something about another country.'
        print('{0} sent a diplomat to {1}.'.format(self.name, target.name))
        if self.__relationships[identity_key(self, target)] < 35:
            print("{0} sent {1}'s diplomat back.".format(target.name, self.name))
            return
        self_target_key = identity_key(self, target)
        self.__relationships[self_target_key] += 3

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
        self.__relationships[identity_key(self, target)] -= relationship_drain

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
            response_calc = (self.__relationships[identity_key(self, ally)]
                             - randint(0, 10)
                             - self.__relationships[identity_key(ally, target)]
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
        self.__relationships[identity_key(self, target)] -= relationship_drain
        self.__relationships[identity_key(ally, target)] -= relationship_drain

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


def identity_key(country1, country2):
    "Returns a key for the 'relationships' dict."
    return ''.join(sorted(country1.identity + country2.identity))
