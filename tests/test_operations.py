import unittest
from algorithm.operations import rotl32, majority3, select3, nl1, nl2, nl3, nl4

class OperationsTests(unittest.TestCase):
    def test_rotation_keeps_32_bits(self):
        self.assertEqual(rotl32(0x80000000, 1), 0x00000001)
        self.assertEqual(rotl32(0x12345678, 0), 0x12345678)

    def test_majority_truth_table(self):
        expected = [0, 0, 0, 1, 0, 1, 1, 1]
        actual = [majority3(x, y, z) & 1
                  for x, y, z in [(0,0,0),(0,0,1),(0,1,0),(0,1,1),
                                  (1,0,0),(1,0,1),(1,1,0),(1,1,1)]]
        self.assertEqual(actual, expected)

    def test_select_truth_table(self):
        expected = [0, 1, 0, 1, 0, 0, 1, 1]
        actual = [select3(x, y, z) & 1
                  for x, y, z in [(0,0,0),(0,0,1),(0,1,0),(0,1,1),
                                  (1,0,0),(1,0,1),(1,1,0),(1,1,1)]]
        self.assertEqual(actual, expected)

    def test_all_custom_functions_are_32_bit(self):
        values = [nl1(0xFFFFFFFF, 0x12345678, 0x87654321),
                  nl2(0xFFFFFFFF, 0x12345678, 0x87654321),
                  nl3(0xFFFFFFFF, 0x12345678, 0x87654321),
                  nl4(0xFFFFFFFF, 0x12345678, 0x87654321)]
        self.assertTrue(all(0 <= value <= 0xFFFFFFFF for value in values))

if __name__ == "__main__":
    unittest.main()
