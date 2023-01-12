kadcar_stats = {
    'k2p': {
        'handling': 60.0,
        'downforce': 70.0,
        'aerodynamic-factor': 62.0,
        'acceleration': 3.9,
        'braking-power': 70.0,
        'engine-type': 'Hybrid : V6 3.5L + Twin Electric Motors',
        'max-length': 5.12352,
        'max-height': 1.97886,
        'max-width': 2.63035,
        'ground-clearance': 0.297131,
        'wheel-base': 2.82967,
        'wheel-type': 'offroad',
        'horse-power': 754.0,
        'engine-size': 3.5,
        'fuel-consumption': '20/12.8/100'
    },
    'k2': {
        'handling': 65.0,
        'downforce': 50.0,
        'aerodynamic-factor': 70.0,
        'acceleration': 3.6,
        'braking-power': 70.0,
        'spoiler': {
            "spoiler_1": {
                'handling': 9.0,
                'aerodynamic-factor': 1.0,
                'downforce': 9.0
            },
            "spoiler_2": {
                'handling': 6.0,
                'aerodynamic-factor': 3.0,
                'downforce': 6.0
            }
        },
        'engine-type': 'Hybrid : V6 3.5L + Twin Electric Motors',
        'max-length': 5.12352,
        'max-height': 2.08889,
        'max-width': 2.49419,
        'ground-clearance': 0.297131,
        'wheel-base': 2.82967,
        'wheel-type': 'offroad',
        'horse-power': 754.0,
        'engine-size': 3.5,
        'fuel-consumption': '20/12.8/100'
    }
}

feature_names = {
    'colors': {
        'black': 'Onyx Black',
        'red': 'Daredevil Red',
        'green': 'Competition Green',
        'blue': 'Mystique Blue',
        'cyan': 'Cyan',
        'gold': 'Karat Gold',
        'pink': 'Flamingo Pink',
        'lightgray': 'Silver Bullet',
        'darkgray': 'Graphite Gray',
        'orange': 'Marmalade Orange',
        'purple': 'Ultraviolet',
        'white': 'Phantom White'
    },
    'backgrounds': {
        'beach': 'Kadena Beach',
        'mountain': 'Crystal Caves',
        'snow': 'K:2 Summit',
        'cyber': 'Speed King',
        'storage': 'Digital Den'
    },
    'rims': {
        'rims_1': 'Core',
        'rims_2': 'Vault',
        'rims_3': 'Consensus',
        'rims_4': 'Mooncrater',
        'rims_5': 'Starfish'
    },
    'spoilers': {
        'spoiler_1': 'Victory Wing',
        'spoiler_2': 'Slip Stream'
    },
    'clearance-light': {
        'clearance_light_1': 'Pact Lights',
        'clearance_light_2': 'Stadium',
    },
    'trims': {
        'carbon_fiber': 'Carbon Fiber',
        'steel': 'Steel Wolf'
    }
}

rim_stats = {
    'rims_1': {
        'material': 'matte-maroon',
        'diameter': 0.592856
    },
    'rims_2': {
        'material': 'matte-black',
        'diameter': 0.592856
    },
    'rims_3': {
        'material': 'steel-darkgray',
        'diameter': 0.592856
    },
    'rims_4': {
        'material': 'matte-black',
        'diameter': 0.592856
    },
    'rims_5': {
        'material': 'steel-darkgray',
        'diameter': 0.592856
    },
}

wheel_stats = {
    'width': 0.0,
    'height': 0.202254,
    'rim-to-edge': 0.0,
    'diameter': 0.0,
    'braking-power': 0.0,
    'size': ""
}

hdri_ipfs_urls = {
    'snow': 'ipfs://',
    'cyber': 'ipfs://',
    'beach': 'ipfs://',
    'storage': 'ipfs://',
    'mountain': 'ipfs://',
}

weights = {
    'k2': {
        'engine': 185.0,
        'electric_motors': 184.0,
        'body': 1600.0,
        'tire': 116.0,
        'rim': 40.0,
        'spoiler_1': 5.8,
        'spoiler_2': 7.0,
        'wheel': 156.0
    },
    'k2p': {
        'engine': 185.0,
        'electric_motors': 184.0,
        'body': 1550.0,
        'tire': 145.0,
        'rim': 50.0,
        'clearance-light_1': 7.0,
        'clearance-light_2': 6.0,
        'wheel_bar': 15.0,
        'wheel': 195.0
    }
}
