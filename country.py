'Class file for the countries in the game.'
import init

class Country:
    'Base class for countries.'

    count = 4
    relationships = init.init_relationships()

    def __init__(self):
        "Initialize country's resources."
        self.resources = init.init_resources()

    def attack(self, target):
        'Country attacks another country.'
        pass

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
    def __init__(self, name):
        'Player chooses a name for each country.'
        super().__init__()
        self.name = name

    def take_turn(self):
        'Computer takes its turn'
        pass
