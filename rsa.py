import cryptomath
import math
import random

def encode(m: str, e: int, n: int) -> list:
    """
    Encodes a message using the RSA encryption scheme.

    Args:
        m (str): the message to encrypt.
        e (int): the public encryption exponent.
        n (int): the public key.

    Raises:
        RSAException

    Returns:
        list: the encoded message blocks.
    """
    if n < 256:
        raise RSAException
    #Break message into blocks if needed...
    encrypt_blocks = __convert_to_int(__block_message(m, n))
    send = []
    for m in encrypt_blocks:
        send.append(__calculate_large_mod(m,e,n))
    return send

def decode(block_mes: list, d: int, n: int) -> str:
    """
    Decodes a message that was encoded with the RSA encryption scheme.

    Args:
        block_mes (list): the block message encoded with RSA.
        d (int): the private decryption exponent.
        n (int): the public key.

    Returns:
        str: the decoded message.
    """
    if n < 256:
        raise RSAException
    decrypt_blocks = []
    for b in block_mes:
        decrypt_blocks.append(__calculate_large_mod(b,d,n))
    return __convert_to_str(decrypt_blocks)

def get_public_private_pair(p: int, q: int) -> tuple:
    """
    Generates the public and private encryption exponents for the RSA 
    encryption scheme.

    Args:
        p (int): a large random prime number (public key = p*q).
        q (int): another large random prime number (public key = p*q).

    Returns:
        tuple: the public private exponent pair.
    """
    e = int(random.uniform(1,(p-1)*(q-1)+1))
    while cryptomath.gcd(e,(p-1)*(q-1)) != 1:
        e = int(random.uniform(1,(p-1)*(q-1)+1))
    d = cryptomath.find_mod_inverse(e,(p-1)*(q-1))
    return (e,d)

def __block_message(m: str, n: int) -> list:
    order = int(math.log2(n))
    to_encrypt = []
    if len(m)*8 > order:
        chunk_low = 0
        chunk_high = int(order/8)
        while chunk_high < len(m):
            to_encrypt.append(m[chunk_low:chunk_high])
            chunk_low = chunk_high
            chunk_high += int(order/8)
            if chunk_high >= len(m):
                chunk_high = len(m)
                to_encrypt.append(m[chunk_low:chunk_high])
    else:
        to_encrypt.append(m)
    return to_encrypt

def __calculate_large_mod(base: int, exp: int, mod: int) -> int:
    done = False
    results = 1
    while not done:
        if exp <= 2:
            done = True
            results = (results * ((base**exp) % mod)) % mod
        else:    
            results = (results * ((base**2) % mod)) % mod
            exp = exp - 2
    return results

def __convert_to_int(blocks: list) -> list:
    conv_blocks = []
    for b in blocks:
        block_int = 0
        for i in range(len(b)):
            shifted = ord(b[i]) << i*8
            block_int = block_int + shifted
        conv_blocks.append(block_int)
    return conv_blocks

def __convert_to_str(blocks: list) -> str:
    block_chars = ""
    for b in blocks:
        index = 0
        while index < math.log2(b):
            chunk = (255 << index) & b
            chunk = chunk >> index
            block_chars = block_chars + chr(chunk)
            index = index + 8
    return block_chars


class RSAException(Exception):
    """
    Raised when one or more parameters for the RSA algorithm is invalid.
    """
    def __init__(self):
        super().__init__("One or more parameter for RSA was invalid.")