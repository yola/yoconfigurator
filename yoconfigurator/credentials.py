import hashlib


def seeded_auth_token(client, service, seed):
    """Return an auth token based on the client+service+seed tuple."""
    hash_func = hashlib.md5()
    hash_func.update(b','.join((client, service, seed)))
    return hash_func.hexdigest()
