import random, pickle
from os import system

from counter_types import effectivity
from pokeload import get_all_pokemons


def clean_screen():
    system('cls')


def get_player_profile(all_pokemons):
    
    return {
        'player_name': input('Cual es tu nombre?: '),
        'pokemon_inventory': [random.choice(all_pokemons).copy() for a in range(3)],
        'combats': 0,
        'pokeballs': 0,
        'health_potion': 0,
        'coins': 0,
    }


def load_profile(all_pokemons):

    opcion = None

    try:
        while opcion not in ['s', 'n']:
            opcion = input('\n¿Cargar partinda? [S/N]: ').lower()
            if opcion not in ['s', 'n']:
                clean_screen()
                print('Opcion incorrecta\n')
        
        clean_screen()

        if opcion == 's':
            
            with open('profile.pkl', 'rb') as profile:
                input('¡Partida cargada!')
                clean_screen()
                return pickle.load(profile)

        else:
            return get_player_profile(all_pokemons)
    
    except FileNotFoundError:
        
        input('Partida no encontrada\nGenerando nueva partida...')
        clean_screen()
        
        return get_player_profile(all_pokemons)


def save_game(profile):
    with open('profile.pkl', 'wb') as game:
        pickle.dump(profile, game)


def any_player_pokemon_lives(profile):
    return sum([pokemon['current_health'] for pokemon in profile['pokemon_inventory']])


def get_pokemon_info(pokemon):
    return '{} | Lvl {} | Hp {}/{} | Tipo {}'.format(pokemon['name'],
                                           pokemon['level'],
                                           pokemon['current_health'],
                                           pokemon['base_health'],
                                           ' - '.join(pokemon['type']))


def choose_pokemon(profile, enemy_pokemon):
    
    while True:
        print(get_pokemon_info(enemy_pokemon) + '\n')
        print('Elige con que pokemon lucharas\n')

        for i in range(len(profile['pokemon_inventory'])):
            print('{} - {}'.format(i, get_pokemon_info(profile['pokemon_inventory'][i])))
        
        try:
            pokemon =  profile['pokemon_inventory'][int(input('\n¿Cual pokemon eliges?: '))]
            if pokemon['current_health'] > 0:
                clean_screen()
                return pokemon
            else:
                clean_screen()
                print('Opcion invalida, {} no puede luchar...\n'.format(pokemon['name']))

        except (ValueError, IndexError):
            clean_screen()
            print('Opcion invalida\n')


def attacks_of_pokemon(pokemon):
    
    attacks_available = []
    
    for attack in pokemon['attacks']:
        
        if attack['min_level'] == '':
            attack['min_level'] = '1'
        
        if attack['damage'] > 0:
            if pokemon['level'] >= int(attack['min_level']):
                attacks_available.append(attack)
                
    if len(attacks_available) == 0:
        attacks_available = [{
            'name': 'Golpe',
            'type': 'normal',
            'min_level': '1',
            'damage': 10
        }]

    return attacks_available


def show_attacks(attacks, player_pokemon, enemy_pokemon):
    
    while True:
        
        battle(player_pokemon, enemy_pokemon)
        
        print('Ataques disponibles:\n')
        count = 0
        for attack in attacks:
            print(count, '- {}\n    Tipo: {}\n    Daño: {}'.format(attack['name'], attack['type'], attack['damage']))
            count += 1
        try:
            return attacks[int(input('\n¿Que ataque eliges?: '))]
        
        except (ValueError, IndexError, ):
            clean_screen()
            print('Opcion invalida\n')


def player_attack(player_pokemon, enemy_pokemon):
    
    attacks = attacks_of_pokemon(player_pokemon)

    attack = show_attacks(attacks, player_pokemon, enemy_pokemon)

    current_damage = effectivity(attack, enemy_pokemon)

    enemy_pokemon['current_health'] -= current_damage

    clean_screen()
    input('{} uso {} -{} Hp'.format(player_pokemon['name'], attack['name'], current_damage))
    
    if enemy_pokemon['current_health'] < 0:
        enemy_pokemon['current_health'] = 0


def enemy_attack(player_pokemon, enemy_pokemon):
    attacks = attacks_of_pokemon(enemy_pokemon)
    attack = random.choice(attacks)
    current_damage = effectivity(attack, enemy_pokemon)

    clean_screen()
    input('{} ha usado {} -{} Hp'.format(enemy_pokemon['name'], attack['name'], current_damage))
    
    player_pokemon['current_health'] -= current_damage
    if player_pokemon['current_health'] < 0:
        player_pokemon['current_health'] = 0


def battle(player_pokemon, enemy_pokemon):
    print('Contrincantes: {} VS {} \n'.format(get_pokemon_info(player_pokemon), get_pokemon_info(enemy_pokemon)))


def pokemon_apears(enemy_pokemon):
    
    pokemon_apears = '|¡Un {} ha aparecido!|\n'.format(get_pokemon_info(enemy_pokemon))
    new_combat = ']--- NUEVO COMBATE ---['
    space = round((len(pokemon_apears) - len(new_combat)) / 2)
    
    print((space * ' ') + new_combat)
    input(pokemon_apears)
    clean_screen()


def assign_items(profile, pokelog):

    log = []
    coins = random.randint(1, 3)
    log.append('¡Has obtenido {} monedas!'.format(coins))
    profile['coins'] += coins

    luck = random.randint(1, 10)

    if luck  == 1:
        profile['pokeballs'] += 1
        log.append('¡Has encontrado una pokeball!')
    elif luck in range(2, 4):
        profile['health_potion'] += 1
        log.append('¡Has encontrado una pocion de vida!')

    for pokemon in profile['pokemon_inventory']:
        
        if pokemon['name'] in pokelog:
            
            xp = random.randint(5, 10)
            pokemon['current_exp'] += xp

            log.append(' - {} ha recibido {} de xp'.format(pokemon['name'], xp))

            xp_level_up = (pokemon['level'] ** 2) + 20

            if pokemon['current_exp'] >= xp_level_up:
                pokemon['level'] += 1
                pokemon['current_exp'] %= xp_level_up
                pokemon['base_health'] += 20
                pokemon['current_health'] = pokemon['base_health']
                
                clean_screen()
                input('¡{} ha subido a nivel {}!'.format(pokemon['name'], pokemon['level']))
    
    clean_screen()

    for element in log:
        print(element)

    input()


def player_opcion(profile):
    clean_screen()
    while True:
        player_opcion = input(
'''\
L - Luchar
T - Tienda                         (Tienes {} Monedas)
C - Curar pokemon                  (Tienes {} Posiones)
I - Informacion de los pokemon

G - Guardar y salir

Elige una opcion: '''.format(profile['coins'], profile['health_potion'])\
        ).lower()
        if player_opcion not in ['l', 't', 'c','i', 'g']:
            clean_screen()
            print('Opcion incorrecta.\n')
        else:
            return player_opcion


def player_opcion_in_battle(profile, player_pokemon, enemy_pokemon):
    while True:
        battle(player_pokemon, enemy_pokemon)
        opcion = input('A - Atacar\n\
C - Curar pokemon     (Tienes {} Pociones)\n\
P - Lanzar pokeball   (Tienes {} Pokeballs)\n\
E - Cambiar pokemon\n\
\nEliges: '.format(profile['health_potion'], profile['pokeballs'])).lower()
        if opcion in ['a', 'c', 'p', 'e']:
            clean_screen()
            return opcion
        else:
            clean_screen()
            print('Opcion invalida.\n')


def capture_pokemon(profile, enemy_pokemon):
    clean_screen()
    
    if profile['pokeballs'] > 0:
        
        profile['pokeballs'] -= 1
        enemy_health = (enemy_pokemon['current_health']/enemy_pokemon['base_health'])*100
        capture_percentage = round((((100 - enemy_health) ** 2) / 100))
        
        if random.randint(1, 100) in range(1, capture_percentage + 1):
            profile['pokemon_inventory'].append(enemy_pokemon)
            input('¡Pokemon capturado!')
            return True
        else:
            return False
    
    else:
        input('No tienes pokeballs...')
        clean_screen()
        return False


def fight(profile, enemy_pokemon):
    
    clean_screen()
    pokemon_apears(enemy_pokemon)
    player_pokemon = choose_pokemon(profile, enemy_pokemon)
    pokelog = [player_pokemon['name']]

    while any_player_pokemon_lives(profile) and enemy_pokemon['current_health'] > 0:
        
        clean_screen()
        pokemon_captured = False

        if player_pokemon['current_health'] > 0:
            
            opcion = player_opcion_in_battle(profile, player_pokemon, enemy_pokemon) # 'a', 'c', 'p', 'e'

            if opcion == 'a':
                player_attack(player_pokemon, enemy_pokemon)
                
                if player_pokemon['name'] not in pokelog:
                    pokelog.append(player_pokemon['name'])
            
            elif opcion == 'c':
                cure_pokemon(profile)

            elif opcion == 'e':
                player_pokemon = choose_pokemon(profile, enemy_pokemon)
            
            else:
                pokemon_captured = capture_pokemon(profile, enemy_pokemon)

            if enemy_pokemon['current_health'] == 0 or pokemon_captured: 
                break
            
            enemy_attack(player_pokemon, enemy_pokemon)
            
        else:

            player_pokemon = choose_pokemon(profile, enemy_pokemon)

    
    clean_screen()
    input(']--- FIN DEL COMBATE ---[')
    clean_screen()

    if enemy_pokemon['current_health'] == 0:
        profile['combats'] += 1
        assign_items(profile, pokelog)


def shop(profile):
    
    clean_screen()

    while True:
    
        print('Estas en la tienda                Monedas: {} Pociones: {} Pokeballs: {}\n'.format(profile['coins'],
                                                                                            profile['health_potion'],
                                                                                            profile['pokeballs']))
        print('0 - Pocion de vida (1) = $5')
        print('1 - Pocion de vida (3) = $12')
        print('2 - Pokeball (1) = $10')
        print('3 - Pokeballs (3) = $25')
        print('\nS - Salir\n')
        opcion = input('Elige una opcion: ').lower()

        if opcion == 's': return
        else: 
            try:
                
                opcion = int(opcion)

                if opcion > 3:

                    clean_screen()
                    print('Opcion invalida.\n')

                elif opcion == 0 and profile['coins'] >= 5:

                    clean_screen()
                    profile['coins'] -= 5
                    profile['health_potion'] += 1

                elif opcion == 1 and profile['coins'] >= 12:

                    clean_screen()
                    profile['coins'] -= 12
                    profile['health_potion'] += 3

                elif opcion == 2 and profile['coins'] >= 10:

                    clean_screen()
                    profile['coins'] -= 10
                    profile['pokeballs'] += 1

                elif opcion == 3 and profile['coins'] >= 25:

                    clean_screen()
                    profile['coins'] -= 25
                    profile['pokeballs'] += 3

                else:
                    clean_screen()
                    print('Dinero insuficiente...\n')

            except (ValueError, TypeError):
                clean_screen()
                print('Opcion invalida.\n')


def cure_pokemon(profile):
    
    clean_screen()

    while True:

        count = 0
        injured_pokemons = []
        print('Estas viento tu mochila              Pociones: {}\n'.format(profile['health_potion']))
        print('Curar 50 de vida con una pocion a:\n')
        
        for pokemon in profile['pokemon_inventory']:
            
            if pokemon['current_health'] < pokemon['base_health']:

                injured_pokemons.append(pokemon)
                print('{} - {} | Hp {}/{}'.format(count, pokemon['name'],
                    pokemon['current_health'], pokemon['base_health']))
                count += 1

        if count == 0:
            print('¡Todos los pokemons estan sanos!')

        print('\nS - Salir\n')
        opcion = input('Eliges: ').lower()

        if opcion == 's': return

        try:

            opcion = int(opcion)
            pokemon = injured_pokemons[opcion]
            
            if profile['health_potion'] > 0:

                pokemon['current_health'] += 50
                profile['health_potion'] -= 1
                
                if pokemon['current_health'] > pokemon['base_health']:
                    pokemon['current_health'] = pokemon['base_health']
                clean_screen()
            
            else:
                clean_screen()
                print('No tienes pociones.\n')
        
        except (ValueError, TypeError, IndexError):
            clean_screen()
            print('Opcion incorrecta.\n')


def all_pokemon_info(pokemons):

    clean_screen()

    while True:

        print('Pokemons en tu inventario:\n')
        count = 0

        for pokemon in pokemons:

            print('{} - {}'.format(count, pokemon['name']))
            count += 1

        print('\nS - Salir\n')

        opcion = input('Eliges: ').lower()

        if opcion == 's': return

        try:
            opcion = int(opcion)
            pokemon = pokemons[opcion]
            clean_screen()
            input('''\
Nombre: {}
Tipo: {}
Nivel: {}
Experiencia: {}/{}
Vida: {}/{}'''.format(pokemon['name'], ' - '.join(pokemon['type']), pokemon['level'], pokemon['current_exp'],
                ((pokemon['level'] ** 2) + 20), pokemon['current_health'], pokemon['base_health']))
            clean_screen()

        except (ValueError, IndexError, TypeError):
            clean_screen()
            print('Opcion invalida.\n')


def assign_enemy_pokemon(profile, all_pokemons):
    
    enemy_pokemon = random.choice(all_pokemons).copy()
    
    pokemons = profile['pokemon_inventory']
    levels = [pokemon['level'] for pokemon in pokemons]
    player_general_level = round((sum(levels) / len(profile['pokemon_inventory'])))
    
    enemy_level = player_general_level + random.randint(-1, 1)
    
    if enemy_level <= 0:
        enemy_level = 1
    
    enemy_pokemon['level'] = enemy_level
    
    if enemy_level > 1:
        enemy_pokemon['base_health'] = enemy_pokemon['base_health'] + (20 * (enemy_level - 1))
        enemy_pokemon['current_health'] = enemy_pokemon['base_health']

    return enemy_pokemon


def main():
    clean_screen()
    all_pokemons = get_all_pokemons() 
    profile = load_profile(all_pokemons)
    exit_game = False
    
    while any_player_pokemon_lives(profile) and not exit_game:
        
        enemy_pokemon = assign_enemy_pokemon(profile, all_pokemons)
        save_game(profile)
        opcion = player_opcion(profile) # l, t, c, i, g
            
        if opcion == 'l':
            fight(profile, enemy_pokemon)
        
        elif opcion == 't':
            shop(profile)
        
        elif opcion == 'c':
            cure_pokemon(profile)
        
        elif opcion == 'i':
            all_pokemon_info(profile['pokemon_inventory'])

        elif opcion == 'g':
            save_game(profile)
            exit_game = True


    if not exit_game:
        system('rm profile.pkl')
        input('{} has perdido en el combate #{}\n\nEnter para comtinuar...'.format(profile['player_name'], profile['combats']))
    
    else:
        clean_screen()
        input('¡Se guardo la partida!\nSaliendo...')


if __name__ == '__main__':
    main()
