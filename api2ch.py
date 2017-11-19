"""2ch.hk API"""

__author__ = 'fadedDexofan, slowpojkee'
__version__ = '0.0.3'
__all__ = ('Api', 'Thread', 'Post', 'BOARDS', 'BOARDS_ALL')

import json
from posixpath import join as urlbuild

import requests

from utils import listmerge

# List sections on board
BOARDS = {
    'thematics': ['bi', 'biz', 'bo', 'c', 'em', 'fa', 'fiz', 'fl', 'ftb', 'hi', 'me', 'mg', 'mlp', 'mo', 'ne', 'psy',
                  're', 'sf', 'sci', 'sn', 'sp', 'spc', 'tv', 'un', 'w', 'wh', 'wm', 'mov', 'rf', 'mu', 'au', 'zog',
                  'o'],
    'creation': ['di', 'de', 'diy', 'mus', 'pa', 'p', 'wp', 'wrk'],
    'tech': ['hw', 'pr', 'ra', 's', 't', 'gd', 'mobi'],
    'politics': ['po', 'news'],
    'games': ['bg', 'cg', 'mmo', 'tes', 'vg', 'wr', 'moba', 'v', 'pok', 'ruvn'],
    'japanese': ['a', 'fd', 'ja', 'ma', 'vn'],
    'other': ['b', 'd', 'soc', 'r', 'abu', 'media'],
    'adults': ['fag', 'fg', 'fur', 'gg', 'ga', 'h', 'ho', 'sex', 'fet', 'e', 'hc', 'guro', 'vape'],
    'user': ['ew', 'hh', 'pvc', 'ph', 'tr', 'dom', 'izd', 'td', 'mc', 'aa', 'rm', 'to', 'web', 'br', 'trv', 'gb', 'fs',
             'cul', 'out', 'old', 'cc', 'ussr', 'jsf', 'ukr', 'sw', 'law', 'm', 'ya', 'r34', 'qtr4', 'wow', 'gabe',
             'cute', 'by', 'se', 'kz', '8', 'es', 'alco', 'brg', 'mlpr', 'ro', 'who', 'srv', 'asmr', 'dr', 'electrach',
             'ing', 'got', 'crypt', 'socionics', 'lap', 'smo', 'hg', 'sad', 'fi', 'nvr', 'ind', 'ld', 'fem', 'gsg',
             'kpop', 'vr', 'arg', 'char', 'obr', 'hv', '2d', 'wwe', 'ch', 'int', 'math']
}

BOARDS_ALL = listmerge(BOARDS)


class Post(object):
    """Post object"""
    __rows__ = ('banned', 'closed', 'comment', 'date', 'email',
                'endless', 'files', 'lasthit', 'name', 'num',
                'number', 'op', 'parent', 'sticky', 'subject',
                'tags', 'timestamp', 'trip')

    def __init__(self, post):
        """
        Create object from dict with post info
        :param post: dict with post info
        """
        self.num = None
        for key, value in post.items():
            setattr(self, key, value)

    def __repr__(self):
        return '<Post: {num}>'.format(num=self.num)


# class Message(object):
#     """Message object"""
#
#     def __init__(self, parent='', comment='', subject=''):
#         """
#         :param parent: parent id (№ OP post)
#         :param comment: text your comment
#         :param subject: subject message example( SAGE )
#         :return:
#         """
#         self.captcha_key = ''
#         self.video = ''
#         self.nofile = ''
#         self.subject = subject
#         self.parent = parent
#         self.submit = ''
#         self.file = ''
#         self.name = ''
#         self.task = 'pоst'
#         self.captcha = ''
#         self.email = ''
#         self.comment = comment
#
#     def __repr__(self):
#         return '<Message: "{comment}...">'.format(comment=self.comment[:10])


class Thread(object):
    """Thread object"""

    def __init__(self, thread):
        """
        Create object from dict with thread info
        :param thread: dict with thread info
        """
        self.reply_count = int(thread['posts_count'])
        # print(thread)
        self.post = Post(thread)
        self.num = self.post.num

    def __repr__(self):
        return '<Thread: {num}>'.format(num=self.num)


class Captcha(object):
    """Captcha object"""

    def __init__(self, captcha):
        """
        Create object from dict with captcha info
        :param captcha: dict with captcha info
        """
        self.id = captcha['id']
        self.type = captcha['type']

    def __repr__(self):
        return '<Captcha: {id}>'.format(id=self.id)


# TODO: Доделать класс Top с топом тредов доски
class Top(object):
    """Top object"""

    def __init__(self, board):
        """
        Create object from dict with board top
        :param board:
        """


# TODO: Вот это надо перепилить. Так просто настройки борды не получить теперь.
# class Settings(object):
#     """Settings object"""
#     __postfields__ = ('captcha_key', 'video', 'nofile', 'subject', 'submit',
#                       'file', 'name', 'task', 'captcha', 'email', 'comment')
#
#     __board__ = ('bump_limit', 'category', 'default_name',
#                  'enable_dices', 'enable_flags', 'enable_icons', 'enable_likes',
#                  'enable_names', 'enable_oekaki', 'enable_posting',
#                  'enable_sage', 'enable_shield', 'enable_subject', 'enable_thread_tags',
#                  'enable_trips', 'id', 'name', 'pages', 'sage', 'tripcodes')
#
#     def __init__(self, settings):
#         """
#         Create object from dict with settings info
#         :param settings: dict with settings info
#         """
#         self.query_interval = settings['query_interval']
#         self.query_limit = settings['query_limit']
#         self.ban_time = settings['ban_time']
#
#         postfields = settings['postfields']
#         self.postfields = {key: value for key, value in postfields.items()}
#
#         board = settings['board']
#         self.board = {key: value for key, value in board.items()}
#
#     def __repr__(self):  # pragma: no cover
#         return '<Settings: {board}>'.format(board=self.board['shortname'])


class Api(object):
    """Api object"""

    def __init__(self, board=None):
        """
        :param board: board code example('b')
        """
        self.logging = False
        self.board = board
        self._url = 'https://2ch.hk/'
        self.settings = None
        self.captcha_key = None
        self.thread = None

        # if board and self.board_exist(board):  # pragma: no cover
        #     self.settings = self.get_settings()

    def _get(self, *args):
        """
        Get page
        :param url: url for request
        :return: raise or json object
        """
        if not self.board:
            raise ValueError('Board is not selected')
        else:
            print(args)
            url = urlbuild(self._url, *args)
            print(url)
            js = requests.get(url).text
            return json.loads(js)

    def get_board(self, board=None):
        """
        Get all threads from board
        :param board: board code
        :return: List of threads on board
        """
        if board and self.board_exist(board):  # pragma: no cover
            self.board = board

        threads = self._get(self.board, 'threads.json')['threads']

        return (Thread(thread) for thread in threads)

    def get_thread(self, thread):
        """
        Get thread
        :param thread: id of thread
        :return: List of Posts object
        """
        if isinstance(thread, Thread):
            thread = thread.num
        self.thread = thread

        posts = self._get(self.board, f'res/{self.thread}.json')['threads']

        return (Post(post) for post in posts[0]['posts'])

    # TODO: Доделать класс Top с топом тредов доски
    def get_top(self, board=None):
        """
        Get top of threads
        :param board: 
        :return: 
        """
        pass

    def get_captcha_settings(self, board=None):
        pass

    # def get_captcha(self):  # pragma: no cover
    #     """
    #     Fetching captcha
    #     :return: captcha info object
    #     """
    #     captcha = Captcha(
    #         self._get('/wakaba.pl?task=api&code=getcaptcha')
    #     )
    #     self.captcha_key = captcha.key
    #     return captcha

    # def get_settings(self):  # pragma: no cover
    #     """Fetching settings"""
    #     return Settings(self._get('/wakaba.pl?task=api&code=getsettings'))

    # def send_post(self, msg):  # pragma: no cover
    #     """
    #     Send post
    #     :param msg: Post object
    #     :return json:
    #     """
    #     params = self.settings.postfields
    #     post = urlencode({
    #         'parent': msg.parent,
    #         params['captcha_key']: self.captcha_key,
    #         params['video']: msg.video,
    #         params['nofile']: msg.nofile,
    #         params['subject']: msg.subject,
    #         params['submit']: msg.submit,
    #         params['file']: msg.file,
    #         params['name']: msg.name,
    #         'task': msg.task,
    #         params['captcha']: msg.captcha,
    #         params['email']: msg.email,
    #         params['comment']: msg.comment
    #     })
    #
    #     try:
    #         url = os.path.join(self._url, self.board, '/wakaba.pl')
    #         urlopen(url, data=post)
    #         return True
    #     except HTTPError as e:
    #         print('Error send post: {msg}'.format(msg=e))

    @staticmethod
    def board_exist(board):
        """
        Checking exist section on board or not
        :param board: name section. example('b')
        :return: boolean
        """
        return board in BOARDS_ALL

    def __repr__(self):
        return '<Api: {board}>'.format(board=self.board)
