import os
import json
import unittest
from mock import Mock
import api2ch

DIR = os.path.dirname(__file__)


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.api = api2ch.Api("pr")
        self.api._url = "file:///" + os.path.join(DIR) + "/"

    def test_api(self):
        self.assertIsInstance(self.api, object)

    def test_set_board(self):
        self.assertEqual(self.api.board, "pr")

    def test_get_board_true(self):
        threads = self.api.get_board("pr")
        thread = threads[0]
        self.assertIsInstance(threads, list)
        self.assertIsInstance(thread, api2ch.Thread)
        self.assertEqual(thread.__repr__(), "<Thread: 87848>")

    def test_get_board_false(self):
        self.api.board = None
        self.assertRaises(ValueError, self.api.get_board)

    def test_get_thread_id_true(self):
        posts = self.api.get_thread(87848)
        post = posts[0]
        self.assertIsInstance(posts, list)
        self.assertIsInstance(post, api2ch.Post)
        self.assertEqual(post.__repr__(), "<Post: 87848>")

    def test_get_thread_object_true(self):
        threads = self.api.get_board()
        posts = self.api.get_thread(threads[0])
        post = posts[0]
        self.assertIsInstance(posts, list)
        self.assertIsInstance(post, api2ch.Post)
        self.assertEqual(post.__repr__(), "<Post: 87848>")

    def test_get_capcha(self):
        CAPTH_MOCK_DATA = file(os.path.join(DIR, "pr", "captcha.json"))

        api = Mock()
        api.get_captcha.return_value = api2ch.Captcha(json.load(CAPTH_MOCK_DATA))
        captcha = api.get_captcha()

        self.assertIsInstance(captcha, api2ch.Captcha)
        self.assertIsNotNone(captcha.url)
        self.assertIsNotNone(captcha.key)

    def test_get_settings(self):
        SETT_MOCK_DATA = file(os.path.join(DIR, "pr", "settings.json"))

        api = Mock()
        api.get_settings.return_value = api2ch.Settings(json.load(SETT_MOCK_DATA))
        settings = api.get_settings()

        self.assertIsInstance(settings, api2ch.Settings)
        self.assertIsNotNone(settings.query_interval)
        self.assertIsNotNone(settings.postfields)

    def test_message_create(self):
        message = api2ch.Message("1", "test comment", "SAGE")
        self.assertEqual(message.subject, "SAGE")

    def test_board_not_exist(self):
        self.assertFalse(self.api.board_exist("bb"))

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
