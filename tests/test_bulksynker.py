import unittest
from bulk_sync.bulk_synker import BulkSynker
import tempfile
import os


class TestBulkSynker(unittest.TestCase):
    def setUp(self):
        self.test_src1 = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.test_src1.cleanup()

    def test_empty_input(self):
        filepath = os.path.join(os.path.dirname(__file__), "text1.csv")
        synker = BulkSynker(filepath, default_target="~")
        synker.load_db(filepath)
        _, valid, total = synker.validate(synker.get_db())
        self.assertEqual(valid, 0)
        self.assertEqual(total, 0)

    def test_invalid_input(self):
        filepath = os.path.join(os.path.dirname(__file__), "text2.csv")
        synker = BulkSynker(filepath, default_target="~")
        synker.load_db(filepath)
        _, valid, total = synker.validate(synker.get_db())
        self.assertEqual(valid, 0)
        self.assertEqual(total, 1)


if __name__ == "__main__":
    unittest.main()
