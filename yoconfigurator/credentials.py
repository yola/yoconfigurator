import hashlib


def seeded_auth_token(client, service, seed):
    """Return an auth token based on the client+service+seed tuple."""
    hash_func = hashlib.md5()
    token = ','.join((client, service, seed)).encode('utf-8')
    hash_func.update(token)
    return hash_func.hexdigest()
