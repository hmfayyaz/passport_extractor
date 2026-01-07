import unittest
import os
from src.extractor import PassportExtractor

class TestPassportExtractor(unittest.TestCase):
    def test_initialization(self):
        """Test if the extractor can be initialized."""
        try:
            extractor = PassportExtractor(use_gpu=False)
            self.assertIsNotNone(extractor.reader)
        except Exception as e:
            self.fail(f"Initialization failed: {e}")

    def test_utils_import(self):
        """Test if utils can be imported correctly."""
        from src.utils import clean_string
        self.assertEqual(clean_string("Hello 123!"), "HELLO123")

if __name__ == '__main__':
    unittest.main()
