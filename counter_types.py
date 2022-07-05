def effectivity(attack, enemy):
    EFFECTIVITY = {
        'agua': {
            'agua': 0.5,
            'dragon': 0.5,
            'fuego': 2,
            'planta': 0.5,
            'roca': 2,
            'tierra': 2
        },
        'bicho': {
            'fuego': 0.5,
            'lucha': 0.5,
            'planta': 2,
            'psiquico': 2,
            'veneno': 2,
            'volador': 0.5
        },
        'dragon': {'dragon': 2},
        'electrico': {
            'agua': 2,
            'dragon': 0.5,
            'electrico': 0.5,
            'planta': 0.5,
            'tierra': 0,
            'volador': 2
        },
        'fantasma': {
            'fantasma': 2,
            'normal': 0,
            'psiquico': 0
        },
        'fuego': {
            'agua': 0.5,
            'bicho': 2,
            'dragon': 0.5,
            'fuego': 0.5,
            'hielo': 2,
            'planta': 2,
            'roca': 0.5
        },
        'hielo': {
            'agua': 0.5,
            'dragon': 2,
            'hielo': 0.5,
            'planta': 2,
            'tierra': 2,
            'volador': 2
        },
        'lucha': {
            'bicho': 0.5,
            'fantasma': 0,
            'hielo': 2,
            'normal': 2,
            'psiquico': 0.5,
            'roca': 2,
            'veneno': 0.5,
            'volador': 0.5
        },
        'normal': {
            'fantasma': 0,
            'roca': 0.5
        },
        'planta': {
            'agua': 2,
            'bicho': 0.5,
            'dragon': 0.5,
            'fuego': 0.5,
            'planta': 0.5,
            'roca': 2,
            'tierra': 2,
            'veneno': 0.5,
            'volador': 0.5
        },
        'psiquico': {
            'lucha': 2,
            'psiquico': 0.5,
            'veneno': 2
        },
        'roca': {
            'bicho': 2,
            'fuego': 2,
            'hielo': 2,
            'lucha': 0.5,
            'tierra': 0.5,
            'volador': 2
        },
        'tierra': {
            'bicho': 0.5,
            'electrico': 2,
            'fuego': 2,
            'planta': 0.5,
            'roca': 2,
            'veneno': 2,
            'volador': 0
        },
        'veneno': {
            'bicho': 2,
            'fantasma': 0.5,
            'planta': 2,
            'roca': 0.5,
            'tierra': 0.5,
            'veneno': 0.5
        },
        'volador': {
            'bicho': 2,
            'electrico': 0.5,
            'lucha': 2,
            'planta': 2,
            'roca': 0.5
        },
        'siniestro': {
            'fantasma': 2,
            'lucha': 0.5,
            'psiquico': 2,
            'siniestro': 0.5
        }
    }

    current_damage = attack['damage']
    type_attack = EFFECTIVITY[attack['type']]
    for type in enemy['type']:
        try:
            current_damage *= type_attack[type]
        except KeyError:
            pass
    return int(current_damage)


def main():
    ata = {
        'type': 'agua',
        'damage': 10
    }
    ene = {
        'type': ['tierra', 'roca']
    }
    print(effectivity(ata, ene))


if __name__ == '__main__':
    main()