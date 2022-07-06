import unittest
import ciphers

"""
Testing harness for the cipher.py module.
See https://docs.python.org/3/library/unittest.html for details on how to
use the unittest framework.
"""
class Test_Affine_Decode(unittest.TestCase):
    """
    Tests calls of the affine_decode method.
    """
    def test_bad_alpha_1(self):
        try:
            ciphers.affine_decode("cvvwpm", 2, 17)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_bad_alpha_2(self):
        try:
            ciphers.affine_decode("cvvwpm", 13, 17)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_bad_alpha_3(self):
        try:
            ciphers.affine_decode("cvvwpm", 32, 17)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_bad_alpha_4(self):
        try:
            ciphers.affine_decode("cvvwpm", -5, 17)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_bad_alpha_5(self):
        try:
            ciphers.affine_decode("cvvwpm", 0, 17)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_empty_text(self):
        try:
            ciphers.affine_decode("", 9, 2)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_bad_text(self):
        try:
            ciphers.affine_decode("@#$%   .(", 9, 2)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_no_shift(self):
        self.assertEqual("testmeoutsomejunkhere", ciphers.affine_decode("test$$meouts@omeju^nkhere", 1, 0))

    def test_simple_shift_left(self):
        self.assertEqual("testmeout", ciphers.affine_decode("sdrsldnts", 1, -1))

    def test_simple_shift_right(self):
        self.assertEqual("testmeout", ciphers.affine_decode("uftunfpvu", 1, 1))

    def test_decrypt(self):
        self.assertEqual("affine", ciphers.affine_decode("cvvwpm", 9, 2))


class Test_Affine_Encode(unittest.TestCase):
    """
    Tests calls of the affine_encode method.
    """
    def test_bad_alpha_1(self):
        try:
            ciphers.affine_encode("affine", 2, 17)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_bad_alpha_2(self):
        try:
            ciphers.affine_encode("affine", 13, 17)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_bad_alpha_3(self):
        try:
            ciphers.affine_encode("affine", 32, 17)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_bad_alpha_4(self):
        try:
            ciphers.affine_encode("affine", -5, 17)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_bad_alpha_5(self):
        try:
            ciphers.affine_encode("affine", 0, 17)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_empty_text(self):
        try:
            ciphers.affine_encode("", 9, 2)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_bad_text(self):
        try:
            ciphers.affine_encode("@#$%   .(", 9, 2)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_no_shift(self):
        self.assertEqual("testmeoutsomejunkhere", ciphers.affine_encode("Test ME ouT! @# SOME 900 junkHere ... ()", 1, 0))

    def test_simple_shift_left(self):
        self.assertEqual("sdrsldnts", ciphers.affine_encode("Test me OUT!", 1, -1))

    def test_simple_shift_right(self):
        self.assertEqual("uftunfpvu", ciphers.affine_encode("Test me OUT!", 1, 1))

    def test_encrypt(self):
        self.assertEqual("cvvwpm", ciphers.affine_encode("affine", 9, 2))

class Test_Calculate_Letter_Frequencies(unittest.TestCase):
    """
    Tests calls of the calculate_letter_frequencies method.
    """
    def test_empty_text(self):
        try:
            ciphers.calculate_letter_freqs("")
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_only_one_letter(self):
        fDict = ciphers.calculate_letter_freqs("mmmmmmmmmmmmm")
        self.assertEqual(fDict['a'], 0.0)
        self.assertEqual(fDict['m'], 1.0)

    def test_only_two_letters(self):
        fDict = ciphers.calculate_letter_freqs("aaabbb")
        self.assertEqual(fDict['a'], 0.5)
        self.assertEqual(fDict['b'], 0.5)
        self.assertEqual(fDict['m'], 0.0)

    def test_small_random(self):
        fDict = ciphers.calculate_letter_freqs("testmeout")
        self.assertEqual(fDict['t'], float(1/3))
        self.assertEqual(fDict['e'], float(2/9))
        self.assertEqual(fDict['s'], float(1/9))
        self.assertEqual(fDict['m'], float(1/9))
        self.assertEqual(fDict['o'], float(1/9))
        self.assertEqual(fDict['u'], float(1/9))
        self.assertEqual(fDict['a'], 0.0)

class Test_Vigenere_Decode(unittest.TestCase):
    """
    Tests calls of the vigenere_decode method.
    """
    def test_empty_text(self):
        try:
            ciphers.vigenere_decode("","vector")
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_empty_key(self):
        try:
            ciphers.vigenere_decode("testmeout", "")
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_bad_key(self):
        try:
            ciphers.vigenere_decode("testmeout", " &&vector")
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_no_shift(self):
        self.assertEqual("testmeout", ciphers.vigenere_decode("testmeout", "aaaaa"))

    def test_simple_shift_left(self):
        self.assertEqual("testmeout", ciphers.vigenere_decode("sdrsldnts", "zzzz"))
    
    def test_simple_shift_right(self):
        self.assertEqual("testmeout", ciphers.vigenere_decode("uftunfpvu", "bbbb"))

    def test_decrypt(self):
        self.assertEqual("hereishowitworks", ciphers.vigenere_decode("citxwjcsybhnjvml", "vector"))

class Test_Vigenere_Encode(unittest.TestCase):
    """
    Tests calls of the vigenere_encode method.
    """
    def test_empty_text(self):
        try:
            ciphers.vigenere_encode("","vector")
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_empty_key(self):
        try:
            ciphers.vigenere_encode("testmeout", "")
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_bad_key(self):
        try:
            ciphers.vigenere_encode("testmeout", " &&vector")
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_no_shift(self):
        self.assertEqual("testmeoutsomejunkhere", ciphers.vigenere_encode("Test ME ouT! @# SOME 900 junkHere ... ()", "aaaaa"))

    def test_simple_shift_left(self):
        self.assertEqual("sdrsldnts", ciphers.vigenere_encode("Test me OUT!", "zzzz"))
    
    def test_simple_shift_right(self):
        self.assertEqual("uftunfpvu", ciphers.vigenere_encode("Test me OUT!", "bbbb"))

    def test_encrypt(self):
        self.assertEqual("citxwjcsybhnjvml", ciphers.vigenere_encode("hereishowitworks", "vector"))