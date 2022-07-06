import unittest
import cryptomath

"""Testing harness for the cryptomath.py module.
    See https://docs.python.org/3/library/unittest.html for details on how to 
    use the unittest framework.
"""
class Test_ExtendedGCD(unittest.TestCase):
    """Tests calls of the extendedgcd method.
    """
    def test_param_zero(self):
        try:
            ans = cryptomath.extendedgcd(0,13)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_param_negative(self):
        try:
            ans = cryptomath.extendedgcd(-13,0)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_a_equal_b(self):
        x, y = cryptomath.extendedgcd(34,34)
        self.assertEqual(x, 0)
        self.assertEqual(y, 1)

    def test_b_divides_a_evenly(self):
        x, y = cryptomath.extendedgcd(6,3)
        self.assertEqual(x, 0)
        self.assertEqual(y, 1)

    def test_round_one(self):
        x, y = cryptomath.extendedgcd(17,5)
        self.assertEqual(x, -2)
        self.assertEqual(y, 7)

    def test_round_two(self):
        x, y = cryptomath.extendedgcd(1180, 482)
        self.assertEqual(x, -29)
        self.assertEqual(y, 71)

    def test_round_three(self):
        x, y = cryptomath.extendedgcd(12345,11111)
        self.assertEqual(x, -2224)
        self.assertEqual(y, 2471)

    def test_params_out_of_order(self):
        x, y = cryptomath.extendedgcd(11111, 12345)
        self.assertEqual(x, -2224)
        self.assertEqual(y, 2471)

class Test_FindModInverse(unittest.TestCase):
    """Tests calls of the findModInverse method.
    """
    def test_param_zero(self):
        try:
            ans = cryptomath.findModInverse(0,13)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_param_negative(self):
        try:
            ans = cryptomath.findModInverse(-13,0)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_round_one(self):
        self.assertEqual(cryptomath.findModInverse(6, 17), 3)

    def test_round_two(self):
        self.assertEqual(cryptomath.findModInverse(17,6), 5)

    def test_round_three(self):
        self.assertEqual(cryptomath.findModInverse(11,13), 6)

    def test_round_four(self):
        self.assertEqual(cryptomath.findModInverse(13,11), 6)

class Test_GCD(unittest.TestCase):
    """Tests calls of the gcd method.
    """
    def test_param_zero(self):
        try:
            ans = cryptomath.gcd(0,13)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_param_negative(self):
        try:
            ans = cryptomath.gcd(-13,0)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_a_equal_b(self):
        ans = cryptomath.gcd(34,34)
        self.assertEqual(34, ans)

    def test_result_one(self):
        ans = cryptomath.gcd(2,13)
        self.assertEqual(1, ans)

    def test_result_two(self):
        ans = cryptomath.gcd(2,22)
        self.assertEqual(2, ans)

    def test_result_three(self):
        ans = cryptomath.gcd(6,15)
        self.assertEqual(3, ans)

    def test_result_seven(self):
        ans = cryptomath.gcd(56,63)
        self.assertEqual(7, ans)

    def test_result_ten(self):
        ans = cryptomath.gcd(40,50)
        self.assertEqual(10, ans)

    def test_params_out_of_order(self):
        ans = cryptomath.gcd(21,6)
        self.assertEqual(3, ans)