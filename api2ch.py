# -*- coding:utf-8 -*-
"""2ch.so API"""
__author__ = "d1ffuz0r"
__version__ = "0.0.1"
__all__ = ["Api", "Thread", "Post", "Captcha", "Settings", "BOARDS"]

import json
import urllib2
from urllib import urlencode

# List sections on board
BOARDS = {
    "thematics": ["au", "bi", "biz", "bo", "c", "em", "ew", "fa", "fiz",
                  "fl", "hi", "hw", "me", "mlp", "mo", "mu", "ne", "ph",
                  "po", "pr", "psy", "ra", "re", "s", "sf", "sci", "sn",
                  "sp", "t", "tr", "tv", "un", "w", "wh", "wm"],
    "creation": ["di", "de", "diy", "f", "pa", "p", "wp", "td"],
    "games": ["bg", "mc", "mmo", "vg", "wr"],
    "japanese": ["a", "aa", "fd", "ma", "vn"],
    "other": ["b", "soc", "r", "abu", "int"],
    "adults": ["fg", "fur", "g", "ga", "h", "ho", "per", "sex"],
    "test": ["fag", "rm", "mg", "adv", "ls", "gb", "spc", "to", "tes", "gd"]
}

listmerge = lambda s: reduce(lambda d, el: d.extend(el) or d, s, [])
BOARDS_ALL = listmerge(BOARDS)


class Post(object):
    """Post object"""
    def __init__(self, post):
        """
        Create object from dict with post info
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


class Message(object):
    """Message object"""
    def __init__(self, parent="", comment="", subject=""):
        """
        @param parent: parent id (№ OP post)
        @param comment: text your comment
        @param subject: subject message example( SAGE )
        @return:
        """
        self.captcha_key = ""
        self.video = ""
        self.nofile = ""
        self.subject = subject
        self.parent = parent
        self.submit = ""
        self.file = ""
        self.name = ""
        self.task = "pоst"
        self.captcha = ""
        self.email = ""
        self.comment = comment


class Thread(object):
    """Thread object"""
    def __init__(self, thread):
        """
        Create object from dict with thread info
        @param thread: dict with thread info
        """
        self.reply_count = int(thread[u"reply_count"])
        self.post = Post(thread[u"posts"][0][0])
        self.num = self.post.num

    def __repr__(self):
        return "<Thread: {num}>".format(num=self.num)


class Captcha(object):
    """Captcha object"""
    def __init__(self, captcha):
        """
        Create object from dict with captcha info
        @param captcha: dict with captcha info
        """
        self.key = captcha[u"key"]
        self.url = captcha[u"url"]


class Settings(object):
    """Settings object"""
    def __init__(self, settings):
        """
        Create object from dict with settings info
        @param settings: dict with settings info
        """
        self.query_interval = settings[u"query_interval"]
        self.query_limit = settings[u"query_limit"]
        self.ban_time = settings[u"ban_time"]

        postfields = settings[u"postfields"]
        self.postfields = {
            "captcha_key": postfields[u"captcha_key"],
            "video": postfields[u"video"],
            "nofile": postfields[u"nofile"],
            "subject": postfields[u"subject"],
            "submit": postfields[u"submit"],
            "file": postfields[u"file"],
            "name": postfields[u"name"],
            "task": postfields[u"task"],
            "captcha": postfields[u"captcha"],
            "email": postfields[u"email"],
            "comment": postfields[u"comment"],
        }

        board = settings[u"board"]
        self.board = {
            "thumb_dir": board[u"thumb_dir"],
            "shortname": board[u"shortname"],
            "wakaba_version": board[u"wakaba_version"],
            "enable_wakabamark": board[u"enable_wakabamark"],
            "imagesize": board[u"imagesize"],
            "favicon": board[u"favicon"],
            "name": board[u"name"],
            "charset": board[u"charset"],
            "max_comment_length": board[u"max_comment_length"],
            "enable_bbcode": board[u"enable_bbcode"],
            "threads_per_page": board[u"threads_per_page"],
            "img_dir": board[u"img_dir"],
            "page_ext": board[u"page_ext"],
            "image_h": board[u"image_h"],
            "image_w": board[u"image_w"],
            "max_field_length": board[u"max_field_length"],
            "res_dir": board[u"res_dir"],
        }

    def __repr__(self):  # pragma: no cover
        return "<Settings: %s>" % self.board["shortname"]


class Api(object):
    """Api object"""
    def __init__(self, board=None):
        """
        @param board: board code example( "b" )
        """
        self.logging = False
        self.board = board
        self._url = "http://2ch.so/"
        self.settings = None
        self.captcha_key = None
        self.thread = None

        if board and self.board_exist(board):  # pragma: no cover
            self.settings = self.get_settings()

    def board_exist(self, board):
        """
        Checking exist section on board or not
        @param board: name section. example( "b" )
        @return: boolean
        """
        return True if board in BOARDS_ALL else False

    def get_board(self, board=None):
        """
        Get all threads from board
        @param board: board code
        @return: List of threads on board
        """
        if board and self.board_exist(board):  # pragma: no cover
            self.board = board

        threads = self._get(url="wakaba.json")[u'threads']

        return [Thread(thread) for thread in threads]

    def _get(self, url):
        """
        Get page
        @param url: url for request
        @return: raise or json object
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
        @return: List of Posts object
        """
        if isinstance(thread, Thread):
            thread = thread.num
        self.thread = thread

        posts = self._get("res/" + str(self.thread) + ".json")[u"thread"]

        return [Post(post[0]) for post in posts]

    def get_captcha(self):  # pragma: no cover
        """
        Fetching captcha
        @return: captcha info object
        """
        captcha = Captcha(
            self._get("/wakaba.pl?task=api&code=getcaptcha")
        )
        self.captcha_key = captcha.key
        return captcha

    def get_settings(self):  # pragma: no cover
        """Fetching settings"""
        self.settings = Settings(
            self._get("/wakaba.pl?task=api&code=getsettings")
        )

    def send_post(self, msg):  # pragma: no cover
        """
        Send post
        @param msg: Post object
        @return json:
        """
        params = self.settings.postfields
        post = urlencode({
            "parent": msg.parent,
            params["captcha_key"]: self.captcha_key,
            params["video"]: msg.video,
            params["nofile"]: msg.nofile,
            params["subject"]: msg.subject,
            params["submit"]: msg.submit,
            params["file"]: msg.file,
            params["name"]: msg.name,
            "task": msg.task,
            params["captcha"]: msg.captcha,
            params["email"]: msg.email,
            params["comment"]: msg.comment
        })

        try:
            urllib2.urlopen(self._url + self.board + "/wakaba.pl", data=post)
            return True
        except urllib2.HTTPError:
            print "Error send post"
