from yoconfigurator.dicts import merge_dicts


def update(config):
    new = {
        'myapp': {
            'secret': 'sauce',
            'hello': 'world',
            'some': {
                'deeply': {
                    'nested': {
                        'value': 'Stefano likes beer'
                    },
                },
            },
            'oz': {
                'tigers': True,
                'lions': True,
                'bears': True,
                'zebras': False,
            },
        }
    }
    return merge_dicts(config, new)
