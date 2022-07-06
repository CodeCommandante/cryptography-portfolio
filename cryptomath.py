import numpy
import random
import math

"""
A module containing useful mathematical methods used in cryptography and 
crypto-analysis.
"""

def extended_gcd(a: int, b: int):
    """
    Returns the x and y variables of the Diophantine equation ax + by = 1.  
    More specifically, this is used here to express gcd(a,b) = 1 as a linear 
    combination, ax + by = 1.

    Args:
        a (int): The first integer to operate gcd on.
        b (int): The second integer to operate gcd on.

    Raises:
        InfiniteSolutionsException

    Returns:
        int: The coefficient of the 'a' variable in the Diophantine equation.
        int: The coefficient of the 'b' variable in the Diophantine equation.
    """
    #Order first and second...
    if gcd(a,b) != 1:
        raise InfiniteSolutionsException
    #Set up table and trivial solutions for extended Euclid
    ee_table = []
    ee_table.append([b,1,0])
    ee_table.append([a,0,1])
    result_row = 2
    done = False
    while not done:
        if (b % a) == 0:
            done = True
        else:
            div_factor = int(b / a)
            #Calculate remainder for this row...
            rem = b % a
            #Calculate x result for this row...
            x = ee_table[result_row-2][1] - ee_table[result_row-1][1]*div_factor
            #Calculate y result for this row...
            y = ee_table[result_row-2][2] - ee_table[result_row-1][2]*div_factor
            #Add to table, update first and second...
            ee_table.append([rem,x,y])
            b = a
            a = rem
            result_row += 1
    if b > a:
        return ee_table[result_row-1][2], ee_table[result_row-1][1]
    return ee_table[result_row-1][1], ee_table[result_row-1][2]

def factor(n: int, m: str = "r") -> tuple:
    """
    Factors a composite number into one pair (of possibly several) of factors.

    Args:
        n (int): The number to factor
        m (str): A flag indicating which factorization method to use:
            'f' = the Fermat method
            'p' = the Pollard p-1 method
            'r' = the Pollard Rho method

    Raises:
        FactoringException

    Returns:
        tuple: A pair of factors for the composite number.
    """
    factors = ()
    #Solve trivial case...
    if n % 2 == 0:
        factors = (2, int(n/2))    
    elif m == "f":
        factors = __fermat_factor(n)
    elif m == "p":
        factors = __pollard_p_minus_one_factor(n)
    elif m == "r":
        factors = __pollard_rho_factor(n)
    return factors

def find_mod_inverse(a: int, n: int) -> int:
    """
    Finds the multiplicative inverse of a rational number in modular 
    arithmetic.  More specifically, solves the multiplicative inverse of (1/a) 
    in the equation, as = 1 (mod n), where 's' is the coefficient of the 
    corresponding Diophantine equation, as + bt = 1.

    Args:
        a (int): The denominator for which to find the multiplicative inverse.
        n (int): The modular range.

    Raises:
        MultiplicativeInverseException

    Returns:
        int: The multiplicative inverse of (1 / a).
    """
    inverse = 0
    while inverse < n:
        if a*inverse % n == 1:
            return inverse
        inverse += 1
    raise MultiplicativeInverseException

def gcd(a: int, b: int) -> int:
    """
    Finds the greatest common divisor (gcd) of the two parameters provided.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The greatest common divisor of 'a' and 'b' (as a positive 
        integer).
    """
    #Quick checks...
    if a == b:
        return b
    if a > b:
        temp = a
        a = b
        b = temp
    if a == 0:
        return b
    if (b % a) == 0:
        return a
    #Use Euclidean to find GCD...
    remainders = []
    last_r = -1
    done = False
    while not done:
        last_r += 1
        remainders.append(b % a)
        b = a
        a = remainders[last_r]
        if remainders[last_r] == 0:
            done = True
    return abs(remainders[last_r - 1])

def inverse_matrix_modular(matrix: list, mod: int = 26) -> list:
    """
    When given an nxn matrix, will return the inverse of this matrix
    mod(mod).

    Args:
        matrix (list): A provided nxn matrix.
        mod (int, optional): The modulus for the inversed matrix. Defaults to 26.

    Returns:
        list: The inverse mod matrix.
    """
    det = numpy.linalg.det(matrix)
    inv = numpy.linalg.inv(matrix)
    pre_inv = numpy.dot(det,inv)
    mod_inv = find_mod_inverse(round(det),26)
    matrix = numpy.dot(pre_inv,mod_inv)
    full = []
    for i in matrix:
        part = []
        for j in i:
            part.append(round(j) % 26)
        full.append(part)
    return full

def is_prime(number: int) -> bool:
    """
    Determines if the provided number is a prime.  Uses the Miller-Rabin 
    algorithm to achieve this.

    Args:
        number (int): The number to test for primality.

    Returns:
        bool: True if prime, False otherwise.
    """
    #Trivial cases...
    if number < 2:
        return False
    elif number == 2:
        return True
    elif number % 2 == 0:
        return False
    k = 0
    m = number - 1
    while m % 2 == 0:
        m = m / 2
        k += 1
    b = __calculate_large_mod_base2(m,number)   
    if b == 1 or b == (number-1):
        return True
    #Loop through algorithm.  If indeterminate, return false.
    while k > 1:
        b = (b**2) % number
        if b == 1:
            return False
        elif b == (number-1):
            return True
        k -= 1
    return False

def is_primitive_root(base: int, modulus: int) -> bool:
    """
    Determines if the base provided is a primitive root of modulus.

    Args:
        base (int): The number for which all non-zero congruences of modulus 
        are obtained.
        modulus (int): A prime number.

    Raises:
        PrimitiveRootException

    Returns:
        bool: True if base is a primitive root; False otherwise.
    """
    #Verify that 1 <= base < modulus and modulus is prime....
    if base <= 1 or base >= modulus or not is_prime(modulus):
        raise PrimitiveRootException
    #Initialize a list of booleans....
    encountered = []
    for i in range(modulus):
        encountered.append(False)
    encountered[0] = True
    #Walk through list of numbers between 1 and modulus and check...
    exp = 1
    while exp < modulus:
        if encountered[base**exp % modulus]:
            return False
        encountered[base**exp % modulus] = True
        exp += 1
    return True

def random_prime(b: int) -> int:
    """
    Generates a prime number greater than 2^b - 1 but less than 2^(b+1) - 1.

    Args:
        b (int): the order (base_2) defining the range containing the prime 
        number

    Returns:
        int: the generated prime number
    """
    candidate = int(random.uniform((2**b)-1,(2**(b+1))))
    while not is_prime(candidate):
        candidate = int(random.uniform((2**b)-1,(2**(b+1))))
    return candidate

def __calculate_large_mod_base2(exp: int, mod: int) -> int:
    done = False
    results = 1
    while not done:
        if exp <= 63:
            done = True
            results = (results * ((2**exp) % mod)) % mod
        else:    
            results = (results * ((2**63) % mod)) % mod
            exp = exp - 63
    return results
        
def __calculate_large_mod_base2_rec(exp: int, mod: int, result: int) -> int:
    if exp <= 63:
        return result * ((2**exp) % mod) % mod
    else:
        result = result * ((2**63) % mod) % mod
        return __calculate_large_mod_base2_rec(exp-63,mod,result)

def __fermat_factor(n: int) -> tuple:
    done = False
    result = tuple()
    y = 1
    while not done:
        pot_sqr = n + y**2
        x = int(math.sqrt(pot_sqr))
        if x**2 == pot_sqr:
            result = (x - y, x + y)
            done = True
        y += 1
        if y >= int(math.sqrt(n)):
            raise FactoringException
    return result

def __pollard_p_minus_one_factor(n: int) -> tuple:
    B = int(random.uniform(1,n))
    while B > 0:
        b = __calculate_large_mod_base2(B,n)
        B = B - 1
        d = gcd(b-1,n)
        if d > 1 and d < n:
            return (d, int(n/d))
    raise FactoringException

def __pollard_rho_factor(n: int) -> tuple:
    #Algorithm found at:  
    #https://www.geeksforgeeks.org/pollards-rho-algorithm-prime-factorization/
    if is_prime(n):
        raise FactoringException
    done = False
    d = 1
    while not done:
        x = int(random.uniform(1,n))
        y = x
        x = (x**2 + 1) % n
        y = (((y**2 + 1) % n)**2 + 1) % n
        d = gcd(abs(x-y),n)
        if d != n and d != 1:
            done = True
    return (d, int(n/d))


class FactoringException(Exception):
    """
    Raised if the factor method is called on a prime number or the flag passed 
    as a parameter is not recognized.
    """
    def __init__(self):
        super().__init__("Factoring method was passed a prime or incorrect flag.")

class InfiniteSolutionsException(Exception):
    """
    Raised when user calls extended_gcd that has multiple solutions for both 
    x and y (when gcd(a,b) does not equal 1).
    """
    def __init__(self):
        super().__init__("No single solution can be arrived at for extended_gcd(a,b).")

class MatrixShapeException(Exception):
    """
    Raised when user tries to check the determinant of a matrix which does not 
    have an equal number of rows and columns.
    """
    def __init__(self):
        super().__init__("Matrix must contain equal number of rows and columns.")

class MultiplicativeInverseException(Exception):
    """
    Raised if the parameters 'a' and 'n' do not have gcd(a,n) equal to 1.
    """
    def __init__(self):
        super().__init__("Multiplicative inverse does not exist.")


class PrimitiveRootException(Exception):
    """
    Raised if parameters passed into the is_primitive_root method are invalid.
    """
    def __init__(self):
        super().__init__("Base must be greater than 1 and less than modulus; modulus must be a prime number")