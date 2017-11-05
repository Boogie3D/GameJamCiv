'Various functions that simplify expressions'

def get_allies_count(country):
    'Returns the number of allies a country has.'
    num_allies = 0
    for key, value in country.relationships:
        if country.identity in key and value > 60:
            num_allies += 1
    return num_allies

def get_allies_list(country):
    'Returns a list of allied countries'
    allied_countries = []
    if country.relationships['AP'] > 60:
        allied_countries.append(country.names[1])

    if country.relationships['BP'] > 60:
        allied_countries.append(country.names[2])

    if country.relationships['CP'] > 60:
        allied_countries.append(country.names[3])

    if country.relationships['DP'] > 60:
        allied_countries.append(country.names[4])

    return allied_countries

def get_enemies_count(country):
    'Returns the number of enemies a country has.'
    num_enemies = 0
    for key, value in country.relationships:
        if country.identity in key and value <= 40:
            num_enemies += 1
    return num_enemies

def identity_key(country1, country2):
    "Returns a key for the 'relationships' dict."
    return ''.join(sorted(country1.identity + country2.identity))

def print_countries(country):
    'Prints a list of non-player countries.'
    for index in range(1, 5):
        print('({0}) {1}'.format(index, country.names[index]))
