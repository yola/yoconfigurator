import hashlib


def seeded_auth_token(client, server, seed):
    '''Return an authentication token based on the client+server+seed tuple'''
    hash_func = hashlib.md5()
    hash_func.update(','.join((client, server, seed)))
    return hash_func.hexdigest()
