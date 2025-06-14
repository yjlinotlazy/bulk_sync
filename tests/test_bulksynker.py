import unittest
from bulk_sync.bulk_synker import BulkSynker
from unittest.mock import MagicMock, patch
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

    @patch("os.path.exists", return_value=True)
    def test_valid_input(self, mock_exists):
        filepath = os.path.join(os.path.dirname(__file__), "text2.csv")
        synker = BulkSynker(filepath, default_target="~")
        _, valid, total = synker.validate(synker.get_db())
        mock_exists.assert_called()
        self.assertEqual(valid, 1)
        self.assertEqual(total, 1)

    @patch("os.path.exists", return_value=True)
    def test_sync_all(self, mock_exists):
        filepath = os.path.join(os.path.dirname(__file__), "text2.csv")
        synker = BulkSynker(filepath, default_target="~")
        synker.sync = MagicMock()
        synker.syncall(dryrun=False)
        mock_exists.assert_called()
        synker.sync.assert_called()

    def test_process_target(self):
        filepath = os.path.join(os.path.dirname(__file__), "text1.csv")
        synker = BulkSynker(filepath, default_target="/home/test")
        synker.sync = MagicMock()
        synker.syncall()
        synker.sync.assert_not_called()


if __name__ == "__main__":
    unittest.main()
