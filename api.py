import json
import urllib2


class Post(object):
    def __init__(self, post):
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
    def __init__(self, thread):
        self.reply_count = int(thread[u"reply_count"])
        self.posts = [Post(post[0]) for post in thread[u"posts"]]

    def __repr__(self):
        return "<Thread: {num}>".format(num=self.posts[0].num)


class Api(object):
    def __init__(self):
        self.board = None
        self._url = "http://2ch.so/"

    def get_threads(self, board=None):
        """
        Get all threads from :board:
        @param board: code of board
        @return dict: list threads on board
        """
        if self.board is None:
            self.board = board
        threads = self._get(url="wakaba.json")[u'threads']
        return [Thread(thread) for thread in threads]

    def _get(self, url):
        """
        Get page
        @param url:
        """
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
        @return: dict
        """
        posts = self._get("res/" + str(thread) + ".json")[u"thread"]
        return [Post(post[0]) for post in posts]
