import random
import string


def generate_id(n_chars=32):
    return ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + '_') for _ in range(n_chars)
    ).encode('utf-8')


__all__ = ["generate_id"]
