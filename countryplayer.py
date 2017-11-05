'Class file for a human player.'
from random import seed, randint, choice, lognormvariate
from country import Country, identity_key

class Player(Country):
    'Class for the player country.'
    def take_turn(self, context):
        'Player takes his/her turn.'
        if context == 'init':
            print("It's your turn!")
            gains = self.__passive_gather__()
            if gains['pop'] > 0:
                print('You gain {0} thousand people.'.format(gains['pop']))
            else:
                print('You lose {0} thousand people.'.format(-gains['pop']))
                if self.resources['population'] <= 0:
                    return 'dead'
            print('You gain {0} thousand tons of food.'.format(gains['food']))
            print('You gain {0} thousand tons of industry resources.'.format(gains['industry']))
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
            self.__relationship_bound__(country_choice)
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
            self.__relationship_bound__(country_choice)
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
            self.__relationship_bound__(country_choice)
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
            self.__relationship_bound__(country_choice)
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
                try:
                    player_target = int(input('>> '))
                except ValueError:
                    print('Invalid input.')
                    continue
                if player_target in range(1, self.__comp_count__):
                    break
                print('Invalid choice.')
            country_list = [c for c in sorted(list(self.__countries__.keys()))
                            if c != 'P']
            country_target = self.__countries__[country_list[player_target - 1]]
            while True:
                print('Who will join you?')
                for ally in allies_list:
                    print('({0}) {1}'.format(allies_list.index(ally) + 1, ally))
                try:
                    player_ally = int(input('>> '))
                except ValueError:
                    print('Invalid input.')
                    continue
                print('Invalid choice.')
            ally_name = allies_list[player_ally - 1]
            for country_value in self.__countries__.values():
                if ally_name == country_value.name:
                    country_ally = country_value
                    break
            if country_target == country_ally:
                print("A country can't help you attack it.")
                return 'retry'
            self.dual_attack(country_ally, country_target)
            self.__relationship_bound__(country_ally)
            self.__relationship_bound__(country_target)
        # Check Status
        elif player_input == '7':
            self.check_status()
            return 'retry'
        # Quit
        elif player_input == '8':
            return 'quit'
        else:
            print('Invalid choice.')
            return 'retry'
        return 'alive'

    def trade(self, target):
        'Country proposes a trade.'
        types = ['food', 'industry']
        print('What do you want to trade?')
        print('(1) Food')
        print('(2) Industrial Resources')
        while True:
            try:
                send_input = int(input('>> '))
            except ValueError:
                print('Invalid input.')
                continue
            if send_input in (1, 2):
                send_type = types[send_input - 1]
                break
            print('Invalid choice.')
        if self.resources[send_type] == 0:
            print('You have nothing to give.')
            return
        print('How much?')
        while True:
            try:
                send_quant = int(input('>> '))
            except ValueError:
                print('Invalid input.')
                continue
            if send_quant <= self.resources[send_type] and send_quant > 0:
                break
            print('Invalid quantity.')

        print('What do you want in return?')
        print('(1) Food')
        print('(2) Indusrial Resources')
        while True:
            try:
                rec_input = int(input('>> '))
            except ValueError:
                print('Invalid input.')
                continue
            if rec_input in (1, 2):
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
            if rec_quant > 0:
                break
            print('Invalid quantity.')
        if (rec_quant > target.resources[rec_type] + 5
                or rec_quant + randint(0, 10) > send_quant
                or self.__relationships__[identity_key(self, target)]
                + randint(0, 20) < 50):
            print('{0} refuses your trade.'.format(target.name))
            self.__relationships__[identity_key(self, target)] -= 5
        else:
            print('{0} accepts your trade.'.format(target.name))
            self.resources[send_type] -= send_quant
            self.resources[rec_type] += rec_quant
            target.resources[send_type] += send_quant
            target.resources[rec_type] -= rec_quant
            self.__relationships__[identity_key(self, target)] += send_quant // 5

    def diplomacy(self, target):
        'Learn something about another country.'
        print('You sent your diplomat to {0}.'.format(target.name))
        if self.__relationships__[identity_key(self, target)] < randint(25, 40):
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
        self.__relationships__[identity_key(self, target)] += 3

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
            try:
                send_input = int(input('>> '))
            except ValueError:
                print('Invalid input.')
                continue
            if send_input in (1, 2):
                send_type = types[send_input - 1]
                break
            print('Invalid choice.')
        if self.resources[send_type] == 0:
            print("You don't have anything to give.")
            return
        while True:
            print('How much will you give?')
            try:
                send_quant = int(input('>> '))
            except ValueError:
                print('Invalid input.')
                continue
            if send_quant <= self.resources[send_type] and send_quant > 0:
                break
            print('Invalid quantity.')
        print('{0} sends its regards.'.format(target.name))
        self.resources[send_type] -= send_quant
        target.resources[send_type] += send_quant
        self.__relationships__[identity_key(self, target)] += send_quant // 4

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
        self.__relationships__[identity_key(self, target)] -= relationship_drain

    def dual_attack(self, ally, target):
        'Country proposes dual attack on another country.'
        print('You propose to attack {0} with {1}'.format(target.name,
                                                          ally.name))
        self_ally_key = identity_key(self, ally)
        self_target_key = identity_key(self, target)
        ally_target_key = identity_key(ally, target)
        # Calculate ally response
        response_calc = (self.__relationships__[self_ally_key]
                         - randint(0, 5)
                         - self.__relationships__[ally_target_key]
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
        self.__relationships__[self_target_key] -= relationship_drain
        self.__relationships__[ally_target_key] -= relationship_drain

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
