'Class file for the countries in the game.'
from random import randint
import init

class Country:
    'Base class for countries.'
    __comp_count__ = 0
    __relationships__ = init.init_relationships()
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
        for key, value in self.__relationships__.items():
            if self.identity in key and value > 60:
                allied_countries.append(self.__get_name_from_key(key))
        return allied_countries

    def __get_enemies_list__(self):
        enemy_countries = []
        for key, value in self.__relationships__.items():
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

    def __relationship_bound__(self, target):
        key = identity_key(self, target)
        if self.__relationships__[key] > 100:
            self.__relationships__[key] = 100
        elif self.__relationships__[key] < 0:
            self.__relationships__[key] = 0

    def __passive_gather__(self):
        pop_gain = randint(1, 3)
        if self.resources['food'] < 20:
            pop_gain = -pop_gain - randint(3, 5)
        food_gain = randint(1, 7)
        industry_gain = randint(3, 10)
        self.resources['population'] += pop_gain
        self.resources['food'] += food_gain
        self.resources['industry'] += industry_gain
        return {'pop': pop_gain, 'food': food_gain, 'industry': industry_gain}

    def enemies_count(self):
        'Returns enemy count for a country.'
        return len(self.__get_enemies_list__())

    def allies_count(self):
        'Returns ally count for a country.'
        return len(self.__get_allies_list__())

    def get_name_from_id(self, identity):
        'Returns the name of a country from its ID.'
        return self.__countries__[identity].name

def identity_key(country1, country2):
    "Returns a key for the 'relationships' dict."
    return ''.join(sorted(country1.identity + country2.identity))
