#S-Boxes for the simplified DES
_SIMP_S1 = [['101','010','001','110','011','100','111','000'],
            ['001','100','110','010','000','111','101','011']]

_SIMP_S2 = [['100','000','110','101','111','001','011','010'],
            ['101','011','000','111','110','010','001','100']]

_THREEROUND_SECRET_KEY = "secretkey"


def simplified_decrypt(ciphertext: str, key: str, rounds: int = 4) -> str:
    """
    Decryption method for the simplified DES algorithm.

    Args:
        ciphertext (str): The ciphertext to decrypt.
        key (str): The encryption key.
        rounds (int, optional): The number of rounds for the original encryption scheme. Defaults to 4.

    Raises:
        SimplifiedDESException

    Returns:
        str: The decrypted message.
    """
    if len(key) < 2 or len(ciphertext) < 3 or len(ciphertext) % 3 != 0:
        raise SimplifiedDESException
    binary_text = __char_to_binary_string(ciphertext)
    binary_key = __char_to_binary_string(key)
    #Make into 12-bit blocks...
    bit_index = 0
    blocks = []
    while(bit_index < len(binary_text)):
        blocks.append(binary_text[bit_index:(bit_index+12)])
        bit_index += 12 
    #Decrypt
    round = rounds - 1
    while round >= 0:
        for i in range(len(blocks)):
            right = blocks[i][0:6]
            left = blocks[i][6:12]
            next_right = __expander(right)
            ith_key = __ith_key(binary_key, round+1)
            next_right = __xor(next_right,ith_key)
            next_right = __xor(left,__sboxes(next_right))
            blocks[i] = next_right + right
        round -= 1
    #Reconstruct blocks into single bit stream...
    plaintext_bits = ""
    for i in blocks:
        plaintext_bits += i
    index = 0
    plaintext = ""
    while index < len(plaintext_bits):
        plaintext += chr(__bit_string_to_int(plaintext_bits[index:index+8]))
        index += 8
    return plaintext


def simplified_encrypt(plaintext: str, key: str, rounds: int = 4) -> str:
    """
    A simplified 12-bit block version of the DES encryption algorithm.

    Args:
        plaintext (str): The plain text to encrypt.
        key (str): The encryption key.
        rounds (int, optional): The number of encryption rounds. Defaults to 4.

    Raises:
        SimplifiedDESException

    Returns:
        str: The cipher text.
    """
    if len(key) < 2 or len(plaintext) < 3:
        raise SimplifiedDESException
    #Pad the plaintext if it isn't a multiple of 3 characters in length.
    if len(plaintext) % 3 != 0:
        loops = len(plaintext) % 3
        for i in range(3 - loops):
            plaintext += ' '
    binary_text = __char_to_binary_string(plaintext)
    binary_key = __char_to_binary_string(key)
    #Make into 12-bit blocks...
    bit_index = 0
    blocks = []
    while(bit_index < len(binary_text)):
        blocks.append(binary_text[bit_index:(bit_index+12)])
        bit_index += 12
    #Encrypt
    round = 0
    while round < rounds:
        for i in range(len(blocks)):
            left = blocks[i][0:6]
            right = blocks[i][6:12]
            next_right = __expander(right)
            ith_key = __ith_key(binary_key, round+1)
            next_right = __xor(next_right,ith_key)
            next_right = __xor(left,__sboxes(next_right))
            blocks[i] = right + next_right
        round += 1
    #Reconstruct blocks into single bit stream...
    ciphertext_bits = ""
    for i in blocks:
        ciphertext_bits += i
    index = 0
    ciphertext = ""
    while index < len(ciphertext_bits):
        ciphertext += chr(__bit_string_to_int(ciphertext_bits[index:index+8]))
        index += 8
    return ciphertext

def three_round_analysis(message1: str, message2: str) -> str:
    """
    INCOMPLETE FUNCTION.  TO-DO!
    """
    #enc_bin_string1 = __char_to_binary_string(simplified_encrypt(message1,_THREEROUND_SECRET_KEY,3))
    #enc_bin_string2 = __char_to_binary_string(simplified_encrypt(message2,_THREEROUND_SECRET_KEY,3))
    enc_bin_string1 = "000011100101"
    enc_bin_string2 = "100100011000"
    L4_exp = __expander(enc_bin_string1[0:6])
    L4s_exp = __expander(enc_bin_string2[0:6])
    enc_bin_string_xor = __xor(L4_exp,L4s_exp)
    inputS1 = enc_bin_string_xor[0:4]
    inputS2 = enc_bin_string_xor[4:8]
    outputS1 = enc_bin_string_xor[0:3]
    outputS2 = enc_bin_string_xor[3:6]
    K4_first = __find_common_pairs(inputS1, outputS1)
    return

#Helpers...
def __char_to_binary_string(string: str) -> str:
    result = ""
    for ch in string:
        result = result + "{:08b}".format(ord(ch))
    return result

def __bit_string_to_int(bit_string: str) -> int:
    index = 0
    result = 0
    while index < len(bit_string):
        if int(bit_string[len(bit_string) - 1 - index]) == 1:
            result = result + 2**index
        index += 1
    return result

def __int_to_bit_string(i: int, length: int) -> str:
    len_str = "{:0" + str(length) + "b}"
    return len_str.format(i)

def __expander(bit_string: str) -> str:
    expanded = bit_string[0] + bit_string[1] + bit_string[3] + bit_string[2]
    expanded = expanded + bit_string[3] + bit_string[2] + bit_string[4] + bit_string[5]
    return expanded 

def __ith_key(key: str, position: int) -> str:
    ith_key = ""
    for i in range(8):
        ith_key = ith_key + key[(position+i)%8]
    return ith_key

def __sboxes(bit_string: str) -> str:
    right_left = bit_string[0:4]
    right_right = bit_string[4:8]
    return _SIMP_S1[__bit_string_to_int(right_left[0])][__bit_string_to_int(right_left[1:4])] + _SIMP_S2[__bit_string_to_int(right_right[0])][__bit_string_to_int(right_right[1:4])]

def __find_common_pairs(input_cond: str, output_cond: str) -> list:
    input_int = __bit_string_to_int(input_cond)
    output_int = __bit_string_to_int(output_cond)
    input_xors = []
    output_xors = []
    for i in range(16):
        for j in range(16):
            if i ^ j == input_int:
                input_xors.append([i,j])
    for k in range(8):
        for l in range(8):
            if k ^ l == output_int:
                output_xors.append([__reverse_lookup_S1_0(k),__reverse_lookup_S1_0(l)])
                output_xors.append([__reverse_lookup_S1_1(k),__reverse_lookup_S1_1(l)])
                output_xors.append([__reverse_lookup_S1_0(k),__reverse_lookup_S1_1(l)])
                output_xors.append([__reverse_lookup_S1_1(k),__reverse_lookup_S1_0(l)])
    shared_pairs = []
    for a in input_xors:
        for b in output_xors:
            if a[0] == b[0] and a[1] == b[1]:
                shared_pairs.append(a)
    return shared_pairs

def __reverse_lookup_S1_0(out: int) -> int:
    value = 0
    for i in _SIMP_S1[0]:
        if __int_to_bit_string(out,3) == i:
            return value
        value += 1
    return value

def __reverse_lookup_S1_1(out: int) -> int:
    value = 0
    for i in _SIMP_S1[1]:
        if __int_to_bit_string(out,3) == i:
            return value + 8
        value += 1
    return value

def __xor(bit_string_1: str, bit_string_2: str) -> str:
    result = ""
    if len(bit_string_1) > len(bit_string_2):
        temp = ""
        for i in range(len(bit_string_1) - len(bit_string_2)):
            temp = temp + "0"
        bit_string_2 = temp + bit_string_2
    elif len(bit_string_2) > len(bit_string_1):
        temp = ""
        for i in range(len(bit_string_2) - len(bit_string_1)):
            temp = temp + "0"
        bit_string_1 = temp + bit_string_1
    for i in range(len(bit_string_1)):
        if bit_string_1[i] == bit_string_2[i]:
            result = result + "0"
        else:
            result = result + "1"
    return result
    

class SimplifiedDESException(Exception):
    """
    Raised if parameters passed into the simplified DES are invalid.
    """
    def __init__(self):
        super().__init__("Plain text must contain at least three characters; Key must be one character long.")