import os
import unittest
from api2ch import Api, Thread, Post, Captcha


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.api = Api()
        self.api._url = "file:///" + os.path.join(os.path.dirname(__file__)) + "/"
        self.api.board = "pr"

    def test_api(self):
        self.assertTrue(isinstance(self.api, object))

    def test_set_board(self):
        self.assertEqual(self.api.board, "pr")

    def test_get_board_true(self):
        threads = self.api.get_board()
        thread = threads[0]
        self.assertTrue(isinstance(threads, list))
        self.assertTrue(isinstance(thread, Thread))
        self.assertEqual(thread.__repr__(), "<Thread: 87848>")

    def test_get_board_false(self):
        self.api.board = None
        self.assertRaises(ValueError, self.api.get_board)

    def test_get_thread_id_true(self):
        posts = self.api.get_thread(87848)
        post = posts[0]
        self.assertTrue(isinstance(posts, list))
        self.assertTrue(isinstance(post, Post))
        self.assertEqual(post.__repr__(), "<Post: 87848>")

    def test_get_thread_object_true(self):
        threads = self.api.get_board()
        posts = self.api.get_thread(threads[0])
        post = posts[0]
        self.assertTrue(isinstance(posts, list))
        self.assertTrue(isinstance(post, Post))
        self.assertEqual(post.__repr__(), "<Post: 87848>")

    def test_get_capcha(self):
        self.api._url = "http://2ch.so/"
        captcha = self.api.get_captcha()
        self.assertTrue(isinstance(captcha, Captcha))
        self.assertIsNotNone(captcha.url)
        self.assertIsNotNone(captcha.key)

if __name__ == '__main__':
    unittest.main()
