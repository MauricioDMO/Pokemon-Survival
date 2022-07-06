import pickle
from requests_html import HTMLSession
from os import system

pokemon_base = {
    'name': "",
    'current_health': 100,
    'base_health': 100,
    'level': 1,
    'type': None,
    'attacks': None,
    'current_exp': 0
}

elements = ['acero', 'agua', 'bicho', 'dragon', 'electrico', 'fantasma', 'fuego', 'hada', 'hielo',
    'lucha', 'normal', 'planta', 'psiquico', 'roca', 'siniestro', 'tierra', 'veneno', 'volador']

URL_BASE = 'https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_nivel&pk='

def find_elements(pokemon_page):
<<<<<<< HEAD

    pokemon_elements = []
    
    for element in elements:
    
        if pokemon_page.html.find('td[class=bordeambos]:not(td[align="center"]) img[alt={}]'.format(element)):
    
            pokemon_elements.append(element)
    
=======
    pokemon_elements = []
    for element in elements:
        if pokemon_page.html.find('td[class=bordeambos]:not(td[align="center"]) img[alt={}]'.format(element)):
            pokemon_elements.append(element)
>>>>>>> 7864afc919c0d018195aab45cda171761b237967
    return pokemon_elements


def find_attacks(pokepage):
<<<<<<< HEAD
    
    attacks = []
    
    for attack_item in pokepage.html.find(".pkmain")[-1].find("tr .check3"):
    
=======
    attacks = []
    for attack_item in pokepage.html.find(".pkmain")[-1].find("tr .check3"):
>>>>>>> 7864afc919c0d018195aab45cda171761b237967
        attack = {
            'name': attack_item.find('td', first=True).find('a', first=True).text,
            'type': attack_item.find("td")[1].find("img", first=True).attrs["alt"],
            'min_level': attack_item.find("th", first=True).text,
            'damage': int(attack_item.find("td")[3].text.replace('--', '0'))
        }
        attacks.append(attack)
    
    return attacks


def get_pokemon(index):
<<<<<<< HEAD
    
=======
>>>>>>> 7864afc919c0d018195aab45cda171761b237967
    url = '{}{}'.format(URL_BASE, index)
    session = HTMLSession()
    pokemon_page = session.get(url)

    pokemon_name = pokemon_page.html.find('.mini', first=True).text.split('\n')[0]

    pokemon_types = find_elements(pokemon_page)

    attacks = find_attacks(pokemon_page)

    pokemon_info = pokemon_base.copy()
    pokemon_info['name'] = pokemon_name
    pokemon_info['type'] = pokemon_types
    pokemon_info['attacks'] = attacks

    return pokemon_info

def load(i):
    i += 1
    i /= 151
    percent = round(i * 100, 2)
    i *= 10
    i = int(i)
    load = '[{}{}] {} %'.format('#' * i, '-' * (10 - i), percent)
    system('cls')
    print(load)


def get_all_pokemons():
    
    try:
        with open('pokedex.pkl', 'rb') as pokedex:
            all_pokemons = pickle.load(pokedex)
    
    except FileNotFoundError:
        
        input('Archivo no encontrado, descargando de internet...\nEnter para continuar')
        
        all_pokemons = []
        aux = 0
        system('cls')
        print('[----------] 0.00 %')
        
        for i in range(151):
        
            all_pokemons.append(get_pokemon(i + 1))
            load(i)
        
        with open('pokedex.pkl', 'wb') as pokedex:
            pickle.dump(all_pokemons, pokedex)
        
        print('Todos los pokemons han sido descargados!')
    
    print('Lista de pokemons cargada!')
<<<<<<< HEAD
    
    return all_pokemons

def main():
    
    lista = []
    
=======
    return all_pokemons

def main():
    lista = []
>>>>>>> 7864afc919c0d018195aab45cda171761b237967
    for i in get_all_pokemons():
        for a in i['attacks']:
            if not a['type'] in lista:
                lista.append(a['type'])
<<<<<<< HEAD
    
=======
>>>>>>> 7864afc919c0d018195aab45cda171761b237967
    print(lista)


if __name__ == '__main__':
    main()