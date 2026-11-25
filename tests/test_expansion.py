import unittest
from algorithm.expansion import expand_words

class ExpansionTests(unittest.TestCase):
    def test_expansion_has_80_words(self):
        words = expand_words(bytes(64))
        self.assertEqual(len(words), 80)
        self.assertTrue(all(0 <= word <= 0xFFFFFFFF for word in words))

    def test_rejects_wrong_block_size(self):
        with self.assertRaises(ValueError):
            expand_words(b"short")

if __name__ == "__main__":
    unittest.main()
