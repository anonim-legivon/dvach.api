# -*- coding:utf-8 -*-

"""2ch.so API"""

__author__ = 'd1ffuz0r'
__version__ = '0.0.2'
__all__ = ('Api', 'Thread', 'Post', 'Captcha',
           'Settings', 'BOARDS', 'BOARDS_ALL')

import json
import os
try:
    from urllib2 import urlopen
    from urllib import urlencode
except ImportError:
    from urllib.request import urlopen
    from urllib.parse import urlencode
    from functools import reduce


# List sections on board
BOARDS = {
    'thematics': ['app', 'au', 'bi', 'biz', 'bo', 'c', 'em', 'ew',
                  'fa', 'fiz', 'fl', 'ftb', 'gd', 'hh', 'hi', 'hw',
                  'me', 'mg', 'mlp', 'mo', 'mu', 'ne', 'pvc', 'ph',
                  'po', 'pr', 'psy', 'ra', 're', 's', 'sf', 'sci',
                  'sn', 'sp', 'spc', 't', 'tr', 'tv', 'un', 'w',
                  'web', 'wh', 'wm'],
    'creation': ['di', 'de', 'diy', 'dom', 'f', 'izd', 'mus', 'o',
                 'pa', 'p', 'wp', 'td'],
    'games': ['bg ,cg ,gb', 'mc', 'mmo', 'tes', 'vg', 'wr'],
    'japanese': ['a', 'aa', 'fd', 'ja', 'ma', 'rm', 'to', 'vn'],
    'other': ['d', 'b', 'fag', 'soc', 'r', 'cp', 'abu', '@', 'int', 'mdk'],
    'adults': ['fg', 'fur', 'g', 'ga', 'h', 'ho', 'per', 'sex'],
    'test': ['gif', 'mov']
}


listmerge = lambda s: reduce(lambda d, el: d.extend(el) or d, s, [])
BOARDS_ALL = listmerge(BOARDS)


class Post(object):
    """Post object"""
    __rows__ = ('lasthit', 'comment', 'name', 'parent', 'timestamp',
                'banned', 'sticky', 'height', 'width', 'num',
                'video', 'tn_height', 'closed', 'tn_width', 'date',
                'subject', 'image', 'thumbnail', 'op', 'size')

    def __init__(self, post):
        """
        Create object from dict with post info
        @param post: dict with post info
        """
        for key, value in post.items():
            setattr(self, key, value)

    def __repr__(self):
        return '<Post: {num}>'.format(num=self.num)


class Message(object):
    """Message object"""
    def __init__(self, parent='', comment='', subject=''):
        """
        @param parent: parent id (№ OP post)
        @param comment: text your comment
        @param subject: subject message example( SAGE )
        @return:
        """
        self.captcha_key = ''
        self.video = ''
        self.nofile = ''
        self.subject = subject
        self.parent = parent
        self.submit = ''
        self.file = ''
        self.name = ''
        self.task = 'pоst'
        self.captcha = ''
        self.email = ''
        self.comment = comment

    def __repr__(self):
        return '<Message: "{comment}...">'.format(comment=self.comment[:10])


class Thread(object):
    """Thread object"""
    def __init__(self, thread):
        """
        Create object from dict with thread info
        @param thread: dict with thread info
        """
        self.reply_count = int(thread['reply_count'])
        self.post = Post(thread['posts'][0][0])
        self.num = self.post.num

    def __repr__(self):
        return '<Thread: {num}>'.format(num=self.num)


class Captcha(object):
    """Captcha object"""
    def __init__(self, captcha):
        """
        Create object from dict with captcha info
        @param captcha: dict with captcha info
        """
        self.key = captcha['key']
        self.url = captcha['url']

    def __repr__(self):
        return '<Captcha: {key}>'.format(key=self.key)


class Settings(object):
    """Settings object"""
    __postfields__ = ('captcha_key', 'video', 'nofile', 'subject', 'submit',
                      'file', 'name', 'task', 'captcha', 'email', 'comment')
    __board__ = ('thumb_dir', 'shortname', 'wakaba_version',
                 'enable_wakabamark', 'imagesize', 'favicon', 'name',
                 'charset', 'max_comment_length', 'enable_bbcode',
                 'threads_per_page', 'img_dir', 'page_ext', 'image_h',
                 'image_w', 'max_field_lengt', 'res_dir',)

    def __init__(self, settings):
        """
        Create object from dict with settings info
        @param settings: dict with settings info
        """
        self.query_interval = settings['query_interval']
        self.query_limit = settings['query_limit']
        self.ban_time = settings['ban_time']

        postfields = settings['postfields']
        self.postfields = {key: value for key, value in postfields.items()}

        board = settings['board']
        self.board = {key: value for key, value in board.items()}

    def __repr__(self):  # pragma: no cover
        return '<Settings: {board}>'.format(board=self.board['shortname'])


class Api(object):
    """Api object"""
    def __init__(self, board=None):
        """
        @param board: board code example( 'b' )
        """
        self.logging = False
        self.board = board
        self._url = 'http://2ch.hk/'
        self.settings = None
        self.captcha_key = None
        self.thread = None

        if board and self.board_exist(board):  # pragma: no cover
            self.settings = self.get_settings()

    def board_exist(self, board):
        """
        Checking exist section on board or not
        @param board: name section. example( 'b' )
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

        threads = self._get(url='wakaba.json')['threads']

        return (Thread(thread) for thread in threads)

    def _get(self, url):
        """
        Get page
        @param url: url for request
        @return: raise or json object
        """
        if not self.board:
            raise ValueError('Board is not selected')
        else:
            url = os.path.join(self._url, self.board, url)
            js = urlopen(url).read().decode('utf8')
            return json.loads(js)

    def get_thread(self, thread):
        """
        Get thread
        @param thread: id of thread
        @return: List of Posts object
        """
        if isinstance(thread, Thread):
            thread = thread.num
        self.thread = thread

        posts = self._get('res/' + str(self.thread) + '.json')[u'thread']

        return (Post(post[0]) for post in posts)

    def get_captcha(self):  # pragma: no cover
        """
        Fetching captcha
        @return: captcha info object
        """
        captcha = Captcha(
            self._get('/wakaba.pl?task=api&code=getcaptcha')
        )
        self.captcha_key = captcha.key
        return captcha

    def get_settings(self):  # pragma: no cover
        """Fetching settings"""
        self.settings = Settings(
            self._get('/wakaba.pl?task=api&code=getsettings')
        )

    def send_post(self, msg):  # pragma: no cover
        """
        Send post
        @param msg: Post object
        @return json:
        """
        params = self.settings.postfields
        post = urlencode({
            'parent': msg.parent,
            params['captcha_key']: self.captcha_key,
            params['video']: msg.video,
            params['nofile']: msg.nofile,
            params['subject']: msg.subject,
            params['submit']: msg.submit,
            params['file']: msg.file,
            params['name']: msg.name,
            'task': msg.task,
            params['captcha']: msg.captcha,
            params['email']: msg.email,
            params['comment']: msg.comment
        })

        try:
            url = os.path.join(self._url, self.board, '/wakaba.pl')
            urlopen(url, data=post)
            return True
        except urllib2.HTTPError as e:
            print('Error send post: {msg}'.format(msg=e))

    def __repr__(self):
        return '<Api: {board}>'.format(board=self.board)
