"""2ch.so API"""

__author__ = "d1ffuz0r"
__version__ = "0.0.1"
__all__ = ["Api", "Thread", "Post", "Captcha"]

import json
import urllib2


class Post(object):
    """Post object. make object from dict"""
    def __init__(self, post):
        """
        @param post: dict with post info
        """
        self.lasthit = post[u"lasthit"]
        self.comment = post[u"comment"]
        self.name = post[u"name"]
        self.parent = post[u"parent"]
        self.timestamp = post[u"timestamp"]
        self.banned = post[u"banned"]
        self.sticky = post[u"sticky"]
        self.height = post[u"height"]
        self.width = post[u"width"]
        self.num = post[u"num"]
        self.video = post[u"video"]
        self.tn_height = post[u"tn_height"]
        self.closed = post[u"closed"]
        self.tn_width = post[u"tn_width"]
        self.date = post[u"date"]
        self.subject = post[u"subject"]
        self.image = post[u"image"]
        self.thumbnail = post[u"thumbnail"]
        self.op = post[u"op"]
        self.size = post[u"size"]

    def __repr__(self):
        return "<Post: {num}>".format(num=self.num)


class Thread(object):
    """Thread object"""
    def __init__(self, thread):
        """
        @param thread: dict with thread info
        """
        self.reply_count = int(thread[u"reply_count"])
        self.posts = Post(thread[u"posts"][0][0])
        self.num = self.posts.num

    def __repr__(self):
        return "<Thread: {num}>".format(num=self.num)


class Captcha(object):
    """Captcha object"""
    def __init__(self, captcha):
        """
        @param captcha: dict with captcha info
        """
        self.key = captcha[u"key"]
        self.url = captcha[u"url"]


class Api(object):
    """Api object"""
    def __init__(self, board=None):
        """
        @param board: board code
        """
        self.board = board
        self._url = "http://2ch.so/"

    def get_board(self, board=None):
        """
        Get all threads from :board:
        @param board: code of board
        @return: list threads on board
        """
        if self.board is None:
            self.board = board

        threads = self._get(url="wakaba.json")[u'threads']

        return [Thread(thread) for thread in threads]

    def _get(self, url):
        if not self.board:
            raise ValueError("Board is not selected")
        else:
            return json.load(
                urllib2.urlopen(self._url + self.board + "/" + url)
            )

    def get_thread(self, thread):
        """
        Get thread
        @param thread: id of thread
        @return: dict of Posts
        """
        if isinstance(thread, Thread):
            thread = thread.num

        posts = self._get("res/" + str(thread) + ".json")[u"thread"]

        return [Post(post[0]) for post in posts]

    def get_captcha(self):
        """
        @return: captcha info
        """
        captcha = self._get(self._url +
                            self.board +
                            "/wakaba.pl?task=api&code=getcaptcha")

        return Captcha(captcha)
