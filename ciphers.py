import cryptomath
import numpy
import random
import re
import math

"""
Module containing methods that simulate various cipher encoding, decoding, 
and attacking.
"""

#ADFGX as a vector...
_ADFGX = ['a','d','f','g','x']

__ADFGX_SEED = "zlcwetugvormnqpsbxahdkiyf"

#List of the alphabet at proper indexes...
_ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

#List of frequencies for the alphabet in order (a-z)...
_ALPHABET_FREQS = [0.082, 0.015, 0.028, 0.043, 0.13, 0.022, 0.02, 0.061, 
0.07, 0.0015, 0.0077, 0.04, 0.024, 0.067, 0.075, 0.019, 0.00095, 0.06, 0.063,
0.091, 0.028, 0.0098, 0.024, 0.0015, 0.02, 0.00074]

#List of letter frequencies in descending order...
_FREQUENCIES = {'e': 0.13, 't': 0.091, 'a': 0.082, 'o': 0.075, 'i': 0.07, 
                'n': 0.067, 's': 0.063, 'h': 0.061, 'r': 0.06, 'd': 0.043, 
                'l': 0.04, 'c': 0.028, 'u': 0.028, 'm': 0.024, 'w': 0.024, 
                'f': 0.022, 'g': 0.02, 'y': 0.02, 'p': 0.019, 'b': 0.015, 
                'v': 0.0098, 'k': 0.0077, 'x': 0.0015, 'j': 0.0015, 
                'q': 0.00095, 'z': 0.00074}

__HILL_KEY = [[12, 15, 0], [24, 23, 15], [3, 16, 4]]

#Cipher functions...
def adfgx_decode(ciphertext: str, keyword: str,  seed: str =__ADFGX_SEED) -> str:
    """
    Decodes an ADFGX cipher, provided the ciphertext, known keyword, and 
    optionally a seed.  If no seed provided, uses a seed that comes with this 
    module.

    Args:
        ciphertext (str): An encrypted text.
        keyword (str): The keyword used to encrypt the ciphertext.
        seed (str, optional): A 25-character "seed" used by the ADFGX cipher. 
        Defaults to __ADFGX_SEED.

    Returns:
        str: The decoded message.
    """
    len_key = len(keyword)
    len_cipher = len(ciphertext)
    char_count = []
    second_passes = int(len_cipher / len_key)
    count = 0
    #Get character counts assigned to each keyword character...
    for i in keyword:
        count += int(len_cipher / len_key)
        char_count.append(int(len_cipher / len_key))
    if len_cipher % len_key != 0:
        second_passes = int(len_cipher / len_key) + 1
        for j in range(len(keyword)):
            if len_cipher - count == 0:
                break
            else:
                char_count[j] += 1
                count += 1
    #Assign encryption characters to their appropriate columns...
    keyword_map = []
    crypt_index = 0
    for a in _ALPHABET:
        key_index = 0
        for i in keyword:
            if a == i:
                word = i
                bound = crypt_index + char_count[key_index]
                while crypt_index < bound:
                    word += ciphertext[crypt_index]
                    crypt_index += 1
                keyword_map.append(word)
            key_index += 1
    keyword_map = __unsort_keyword_mapping(keyword_map, keyword)
    #Get first pass encryption from algorithm...
    stop = 0
    first_pass = ""
    for i in range(second_passes):
        for item in keyword_map:
            if stop == len_cipher:
                break
            first_pass += item[i+1]
            stop += 1
    #Construct final decoded message...
    index = 0
    result = ""
    while index < len_cipher:
        result += __get_adfgx_decoding(seed, first_pass[index], first_pass[index+1])
        index += 2
    return result

def adfgx_encode(plaintext: str, keyword: str, seed=__ADFGX_SEED) -> str:
    """
    Encodes a plaintext using the ADFGX cipher.  Requires a random ordering of 
    the alphabet (less "j"), called here the "seed", and the encryption 
    keyword as additional parameters.

    Args:
        plaintext (str): The original text to be encrypted.
        seed (str): A selected ordering of the 26-character alphabet (less "j")
        keyword (str): The encryption keyword/password - used for decoding.

    Raises:
        EmptyTextException

    Returns:
        str: An ADFGX encrypted text.
    """
    cleaned_plain = list(__prep_text(plaintext))
    if len(cleaned_plain) == 0:
        raise EmptyTextException
    #Map seed to ADFGX...
    mapping = {}
    for i in range(5):
        for j in range(5):
            pair = _ADFGX[i] + _ADFGX[j]
            mapping[seed[i*5+j]] = pair
    #Get first pass of encoding...
    first_encode = ""
    for letter in cleaned_plain:
        first_encode += mapping[letter]
    #Map first encoding to keyword...
    keyword_map = []
    for index in range(len(keyword)):
        jump = index
        column_word = keyword[index]
        while jump < len(first_encode):
            column_word += first_encode[jump]
            jump += len(keyword)
        keyword_map.append(column_word)
    #Sort the columns alphabetically and construct encrypted string...
    keyword_map = __sort_keyword_mapping(keyword_map)
    encoding = ""
    for index in range(len(keyword_map)):
        encoding += keyword_map[index][1:]
    return encoding

def affine_ciphertext_attack(text: str) -> str:
    """
    Runs all 312 possible affine decodings against the provided text and
    returns the results for examination.

    Args:
        text (str): The affine-encrypted message/text.

    Raises:
        EmptyTextException

    Returns:
        str: A comprehensive list of the possible decodings.
    """
    if len(text) == 0:
        raise EmptyTextException
    affineAlphas = [1,3,5,7,9,11,15,17,19,21,23,25]
    results = "Encrypted text:  " + text + "\n"
    results = results + "===================================================\n"
    results = results + "Affine encoding:                       Output:\n"
    for a in affineAlphas:
        for b in range(26):
            results = results + str(a) + "x + " + str(b) + " => " + affine_decode(text, a, b) + "\n"
    return results


def affine_decode(text: str, alpha: int, beta: int) -> str:
    """
    Decodes a text encrypted with an affine cypher with the known alpha and 
    beta parameters.  Affine cyphers are of the form ax + b (mod26) = E, where 
    'a' (alpha) is a number gcd(a,26) = 1; 'b' (beta) is any positive or 
    negative integer; and E is the position of the new letter in the alphabet.

    Args:
        text (str): The encrypted message to decrypt.
        alpha (int): The multiplied factor of the affine encryption algorithm 
        (a, where ax + b (mod26) = E).
        beta (int): The shifted amount of the affine encryption algorithm (b, 
        where ax + b (mod26) = E).
 
    Raises:
        AffineAlphaException or EmptyTextException

    Returns:
        str: The decrypted message.
    """
    if cryptomath.gcd(alpha, 26) != 1:
        raise AffineAlphaException
    decodeArray = list(__prep_text(text))
    if len(decodeArray) == 0:
        raise EmptyTextException
    plainText = ""
    for symbol in decodeArray:
        x = (_ALPHABET.index(symbol) - beta) * cryptomath.find_mod_inverse(alpha, 26)
        plainText = plainText + _ALPHABET[x % 26]
    return plainText

def affine_encode(text: str, alpha: int, beta: int) -> str:
    """
    Encodes a provided text using an affine cipher of the form ax + b (mod 26) 
    = E; where a is parameter alpha and b is parameter beta.

    Args:
        text (str): The text to encrypt.
        alpha (int): The multiplied factor of the affine encryption algorithm 
        (a, where ax + b (mod26) = E).
        beta (int): The shifted amount of the affine encryption algorithm (b, 
        where ax + b (mod26) = E).

    Raises:
        AffineAlphaException
        EmptyTextException

    Returns:
        str: The encrypted message.
    """
    if cryptomath.gcd(alpha, 26) != 1:
        raise AffineAlphaException
    encodeArray = list(__prep_text(text))
    if len(encodeArray) == 0:
        raise EmptyTextException
    cipherText = ""
    for symbol in encodeArray:
        encodeIndex = (alpha * _ALPHABET.index(symbol) + beta) % 26
        cipherText = cipherText + _ALPHABET[encodeIndex]
    return cipherText

def affine_plaintext_attack(text: str, pt_letter: str, ct_letter: str) -> str:
    """
    Given a known plaintext letter and it's corresponding ciphertext letter, 
    runs the 12 possible affine decodings against the provided text and
    returns the results for examination.

    Args:
        text (str): The affine-encrypted message/text.
        pt_letter (str): The plaintext letter.
        ct_letter (str): The corresponding ciphertext letter.

    Raises:
        EmptyTextException

    Returns:
        str: A comprehensive list of the possible decodings.
    """
    if len(text) == 0 or len(pt_letter) != 1 or len(ct_letter) != 1:
        raise EmptyTextException
    affineAlphas = [1,3,5,7,9,11,15,17,19,21,23,25]
    results = "Encrypted text:  " + text + "\n"
    results = results + "===================================================\n"
    results = results + "Affine encoding:                       Output:\n"
    for a in affineAlphas:
        beta = __get_alphabet_index(ct_letter) - a*__get_alphabet_index(pt_letter)
        beta = beta % 26
        results = results + str(a) + "x + " + str(beta) + " => " + affine_decode(text, a, beta) + "\n"
    return results

def calculate_letter_freqs(text: str) -> dict:
    """
    Given a text/message, calculates the count frequency for each letter a-z 
    in the message.

    Args:
        text (str): The message for which to calculate the letter frequencies.

    Raises:
        EmptyTextException

    Returns:
        dict: A dictionary of letters a-z, along with their frequencies (as a 
        function of the total alphabetic characters in the text).
    """
    cAlphabet = {}
    #Initialize count dictionary for text...
    for a in _ALPHABET:
        cAlphabet[a] = 0
    cleanedText = list(__prep_text(text))
    if len(cleanedText) == 0:
        raise EmptyTextException
    for symbol in cleanedText:
        cAlphabet[symbol] += 1
    #Initialize rate dictionary for text and return...
    #Be careful here!  cAlphabet members are deleted during the fAlphabet 
    #construction loop.  If you exceed the range of cAlphabet, you will 
    #access an empty list!
    fAlphabet = {}
    for i in range(26):
        theKey, theVal = __find_dict_max(cAlphabet)
        fAlphabet[theKey] = theVal / len(cleanedText)
        del cAlphabet[theKey]
    return fAlphabet   

def get_random_adfgx_seed() -> str:
    """
    Returns:
        str: A string of the alphabet in a random order, excluding the letter 
            "j".  This can be used to seed an ADFGX cipher.
    """
    loops = int(random.uniform(0,1) * 26)
    alph_copy = _ALPHABET.copy()
    alph_copy.pop(9)    #remove j from the alphabet
    index = 0
    while index < loops:
        swap_a = int(random.uniform(0,1) * 25)
        swap_b = int(random.uniform(0,1) * 25)
        temp = alph_copy[swap_a]
        alph_copy[swap_a] = alph_copy[swap_b]
        alph_copy[swap_b] = temp
        index += 1
    return_str = ""
    for letter in alph_copy:
        return_str += str(letter)
    return return_str

def get_random_hill_key(n: int) -> list:
    """
    Generates an nxn matrix\key with random letters from the 26-character 
    alphabet in it (mapped as numbers).  Checks that the matrix will be 
    invertable and re-constructs if not.  Used for the Hill cipher.

    Args:
        n (int): The number of rows and columns for the matrix.

    Returns:
        list: The matrix/2D array of numbers (the key).
    """
    again = True
    key = []
    while again:
        key.clear()
        for i in range(n):
            row = []
            for j in range(n):
                row.append(int(random.uniform(0,1)*26))
            key.append(row)
        if cryptomath.gcd(__determinant(key), 26) == 1:
            again = False
    return key

def hill_decode(ciphertext: str, key: list = __HILL_KEY) -> str:
    """
    Decodes a message that was encoded with a Hill cipher using the known key.

    Args:
        ciphertext (str): The encrypted message.
        key (list, optional): The Hill cipher key. Defaults to __HILL_KEY.

    Raises:
        EmptyTextException
        HillCipherKeyException

    Returns:
        str: The decrypted message.
    """
    #Preliminaries: check for bad input...
    if len(ciphertext) == 0 or len(ciphertext) % len(key) != 0:
        raise EmptyTextException
    if not is_valid_hill_key(key):
        raise HillCipherKeyException
    #Get inverse of key...
    inv_key = cryptomath.inverse_matrix_modular(key)
    n = len(inv_key)
    plain_vecs = []
    for i in range(int(len(ciphertext) / n)):
        vec = []
        for j in range(n):
            vec.append(__get_alphabet_index(ciphertext[i*n + j]))
        plain_vecs.append(numpy.dot(numpy.array(vec),inv_key))
    return __map_vectors_to_string(plain_vecs)

def hill_encode(plaintext: str, key: list = __HILL_KEY) -> str:
    """
    Encodes a plain text message using the "key" provided.

    Args:
        plaintext (str): The message to encrypt.
        key (list, optional): The key to use in the Hill cipher encryption 
        sheme. Defaults to __HILL_KEY.

    Raises:
        EmptyTextException
        HillCipherKeyException

    Returns:
        str: The encoded message.
    """
    #Clean plaintext, check that key is valid...
    cleantext = __prep_text(plaintext)
    if len(cleantext) == 0:
        raise EmptyTextException
    np_key = numpy.array(key)
    if not is_valid_hill_key(key):
        raise HillCipherKeyException
    #Pad text, if needed...
    if len(cleantext) % np_key.shape[0] != 0:
        bound = np_key.shape[0] - len(cleantext) % np_key.shape[0]
        for i in range(bound):
            cleantext += 'x'
    #Turn plaintext into a series of vectors and perform multiplication...
    n = np_key.shape[0]
    cipher_vecs = []
    for i in range(int(len(cleantext) / n)):
        vec = []
        for j in range(n):
            vec.append(__get_alphabet_index(cleantext[i*n + j]))
        cipher_vecs.append(numpy.dot(numpy.array(vec),np_key))
    return __map_vectors_to_string(cipher_vecs)

def is_valid_hill_key(key: list) -> bool:
    """
    Checks that the provided key is a valid Hill cipher key.

    Args:
        key (list): The key/matrix to check.

    Returns:
        bool: Valid key if true; invalid key if false.
    """
    np_key = numpy.array(key)
    try:
        if np_key.shape[0] != np_key.shape[1]:
            return False
        if cryptomath.gcd(__determinant(key),26) != 1:
            return False
        for i in key:
            for j in i:
                if j < 0 or j >= 26:
                    return False
    except:
        return False
    return True

def vigenere_decode(text: str, key: str) -> str:
    """
    Given the key for a Vigenere cipher, decodes an encrypted message.

    Args:
        text (str): The message encrypted with a Vigenere cipher.
        key (str): The key used to encrypt the message.

    Raises:
        EmptyTextException

    Returns:
        str: The decrypted message/text.
    """
    decodeArray = list(__prep_text(text))
    if not __is_valid_key(key) or len(decodeArray) == 0:
        raise EmptyTextException
    keyIndex = 0
    plainText = ""
    for symbol in decodeArray:
        keyIndex = keyIndex % len(key)
        decryptIndex = (_ALPHABET.index(symbol) - _ALPHABET.index(key[keyIndex])) % 26
        plainText = plainText + _ALPHABET[decryptIndex]
        keyIndex += 1
    return plainText

def vigenere_encode(text: str, key: str) -> str:
    """
    Given an encryption key, encrypts a message using the Vigenere method.

    Args:
        text (str): The message/text to encrypt.
        key (str): The Vigenere key.

    Raises:
        EmptyTextException

    Returns:
        str: The encrypted message/text.
    """
    encodeArray = list(__prep_text(text))
    if not __is_valid_key(key) or len(encodeArray) == 0:
        raise EmptyTextException
    keyIndex = 0
    cipherText = ""
    for symbol in encodeArray:
        keyIndex = keyIndex % len(key)
        encryptIndex = (_ALPHABET.index(symbol) + _ALPHABET.index(key[keyIndex])) % 26
        cipherText = cipherText + _ALPHABET[encryptIndex]
        keyIndex += 1
    return cipherText

def vigenere_find_key_length(cipher_text: str) -> list:
    """
    Given an encrypted text, finds the top candidates for the key length based 
    on the number of "coincidences" that occur.

    Args:
        cipher_text (str): The previously encrypted message/text.

    Raises:
        EmptyTextException

    Returns:
        list: A list of most-likely key lengths.
    """
    if len(cipher_text) == 0:
        raise EmptyTextException
    disp_text = cipher_text
    displacement = 1
    results = []
    coincidences = []
    coincidences.append(-1)
    while displacement < len(cipher_text) and displacement < 23:
        disp_text = disp_text[1:] + disp_text[0:1]
        coincidences.append(__find_coincidences(cipher_text, disp_text))
        displacement += 1
    first_cand = max(coincidences)
    second_cand = __max_second(coincidences, first_cand)
    third_cand = __max_third(coincidences, first_cand, second_cand)
    for i in range(len(coincidences)):
        if coincidences[i] == first_cand or coincidences[i] == second_cand or coincidences[i] == third_cand:
            results.append(i)
    return results

def vigenere_get_key(cipher_text: str, key_length: int) -> str:
    """
    Given an ecrypted text and a supposed key length, returns the key most 
    likely associated with this key length.

    Args:
        cipher_text (str): The encrypted text you are seeking to decode.
        key_length (int): The supposed length of the encryption key.

    Raises:
        EmptyTextException

    Returns:
        str: A key of length key_length that may decode the encrypted text.
    """
    if len(cipher_text) == 0:
        raise EmptyTextException
    total_chars = len(cipher_text)
    key = ""
    loop_count = 0
    #Run for each possible letter in the key...
    while loop_count < key_length:
        index = loop_count
        #Gets a new list for the alphabet, initialized to zero...
        alpha_count = __get_alphabet_count()
        #Get letter frequencies for the key position...
        while index < total_chars:
            alpha_count[__get_alphabet_index(cipher_text[index])] += 1
            index += key_length
        key = key + __calculate_key_char(alpha_count)
        loop_count += 1
    return key

#Helper functions...
def __calculate_key_char(count_vec: list) -> str:
    copy_vec = count_vec.copy()
    freq_vec = []
    freq_vec.append(numpy.dot(count_vec,_ALPHABET_FREQS))
    index = 1
    while index < 26:
        copy_vec = copy_vec[1:] + copy_vec[0:1]
        freq_vec.append(numpy.dot(copy_vec,_ALPHABET_FREQS))
        index += 1
    key = __find_list_max_index(freq_vec)
    return _ALPHABET[key]

def __determinant(matrix: list) -> int:
    np_key = numpy.array(matrix)
    return round(numpy.linalg.det(np_key))

def __find_coincidences(text_a: str, text_b: str) -> int:
    count = 0
    for i in range(len(text_a)):
        if text_a[i] == text_b[i]:
            count += 1
    return count

def __find_dict_max(dictionary: dict):
    currMax = -1
    currKey = ''
    for key, val in dictionary.items():
        if val > currMax:
            currMax = val
            currKey = key
    return currKey, currMax

def __find_list_max_index(theList: list) -> int:
    max_val = -1
    max_key = 0
    for index in range(len(theList)):
        if theList[index] > max_val:
            max_val = theList[index]
            max_key = index
    return max_key

def __get_adfgx_decoding(seed: str, row: str, column: str) -> str:
    return seed[__get_adfgx_index(row) * 5 + __get_adfgx_index(column)]

def __get_adfgx_index(character: str) -> int:
    if character == 'a':
        return 0
    elif character == 'd':
        return 1
    elif character == 'f':
        return 2
    elif character == 'g':
        return 3
    elif character == 'x':
        return 4
    else:
        return -1

def __get_alphabet_index(letter: str) -> int:
    index = 0
    for symbol in _ALPHABET:
        if symbol == letter:
            return index
        index += 1

def __get_alphabet_count() -> list:
    alpha_count = []
    for letter in _ALPHABET:
        alpha_count.append(0)
    return alpha_count

def __map_vectors_to_string(vectors: list) -> str:
    result = ""
    for i in vectors:
        for j in i:
            result += _ALPHABET[j%26]
    return result

def __is_valid_key(key: str) -> bool:
    result = re.search(r'[^A-Za-z]', key)
    if result == None:
        return True
    return False

def __max_second(list: list, first_max: int) -> int:
    candidate = 0
    for value in list:
        if value > candidate and value != first_max:
            candidate = value
    return candidate

def __max_third(list: list, first_max: int, second_max: int) -> int:
    candidate = 0
    for value in list:
        if value > candidate and value != first_max and value != second_max:
            candidate = value
    return candidate

def __prep_text(text: str) -> str:
    prepped = re.sub(r'[^A-Za-z]', '', text)
    prepped = prepped.lower()
    return prepped

def __sort_keyword_mapping(keyword_map: list) -> list:
    i = len(keyword_map) - 1
    while i >= 0:
        j = i
        while j < len(keyword_map) - 1:
            if ord(keyword_map[j][0]) > ord(keyword_map[j+1][0]):
                temp_map = keyword_map[j]
                keyword_map[j] = keyword_map[j+1]
                keyword_map[j+1] = temp_map
                j += 1
            else:
                break
        i -= 1
    return keyword_map

def __unsort_keyword_mapping(keyword_map: list, keyword: str) -> list:
    for i in range(len(keyword) - 1):
        j = i
        while j < len(keyword_map):
            if keyword[i] == keyword_map[j][0] and i == j:
                break
            elif keyword[i] == keyword_map[j][0]:
                temp = keyword_map[i]
                keyword_map[i] = keyword_map[j]
                keyword_map[j] = temp
                break
            j += 1
    return keyword_map

#Exceptions...
class AffineAlphaException(Exception):
    """
    Raised when user provides an alpha parameter that 
    results in an impossible decryption.  gcd(alpha, 26) must equal 1.
    """
    def __init__(self):
        super().__init__("Alpha should be relative prime with 26.")

class EmptyTextException(Exception):
    """
    Raised when user provides a text (either to encrypt or 
    decrypt) which is empty.
    """
    def __init__(self):
        super().__init__("Text and keys must contain only alphabetic characters.")

class HillCipherKeyException(Exception):
    """
    Raised when user provides an invalid or non-invertible Hill cipher key 
    (matrix).
    """
    def __init__(self):
        super().__init__("Hill cipher key/matrix is not valid.")
