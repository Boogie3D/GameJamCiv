'Various functions that simplify expressions'

def get_allies(country):
    'Returns the number of allies a country has.'
    num_allies = 0
    for key, value in country.relationships:
        if country.identity in key and value > 60:
            num_allies += 1
    return num_allies

def get_enemies(country):
    'Returns the number of enemies a country has.'
    num_enemies = 0
    for key, value in country.relationships:
        if country.identity in key and value <= 40:
            num_enemies += 1
    return num_enemies

def identity_key(country1, country2):
    "Returns a key for the 'relationships' dict"
    return ''.join(sorted(country1.identity + country2.identity))
