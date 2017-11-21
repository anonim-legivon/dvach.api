"""2ch.hk API"""

__all__ = ('Api', 'Thread', 'Post', 'Captcha', 'BOARDS', 'BOARDS_ALL')

import json
from posixpath import join as url_join

import requests

from api2ch.utils import listmerge

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


# TODO: Сделать класс сообщения для отправки
class Message(object):
    """Message object"""

    def __init__(self, thread='', comment='', subject='', email=''):
        """
        :param thread: thread id (№ OP post)
        :param comment: text your comment
        :param subject: subject message example( SAGE )
        :param email: user email
        """
        self.captcha_type = '2chaptcha'
        self.captcha_key = ''
        self.json = 1
        self.task = 'post'
        self.subject = subject
        self.thread = thread
        self.submit = ''
        self.file = ''
        self.name = ''
        self.captcha = ''
        self.email = email
        self.comment = comment

    def __repr__(self):
        return '<Message: "{comment}...">'.format(comment=self.comment[:10])


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
        self.img = f'https://2ch.hk/api/captcha/2chaptcha/image/{self.id}'
        self.answer = None

    def __repr__(self):
        return '<Captcha: {id}>'.format(id=self.id)


# TODO: Прикрутить работу с пасскодом, там нужны куки
class Passcode(object):
    """Passcode object"""

    def __init__(self, passcode):
        """

        :param passcode:
        """
        pass


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
        self.captcha_id = None
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
            url = url_join(self._url, *args)
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

    def get_top(self, board=None, method='views', num=5):
        """
        Top threads on board
        :param board: board to get top
        :param method: sorting method (views, score, posts)
        :param num: num of threads to return
        :return: list
        """
        if board and self.board_exist(board):  # pragma: no cover
            self.board = board

        threads = self._get(self.board, 'threads.json')['threads']

        if method == 'views':
            threads = sorted(threads, key=lambda thread: (thread['views'], thread['score']), reverse=True)
        elif method == 'score':
            threads = sorted(threads, key=lambda thread: (thread['score'], thread['views']), reverse=True)
        elif method == 'posts':
            threads = sorted(threads, key=lambda thread: (thread['posts_count'], thread['views']), reverse=True)
        else:
            return []

        sorted_threads = []

        for i in range(num):
            sorted_threads.append(threads[i])

        return sorted_threads

    def get_captcha(self):  # pragma: no cover
        """
        Fetching captcha
        :return: captcha object
        """
        captcha = Captcha(
            self._get('api/captcha/2chaptcha/service_id')
        )
        self.captcha_id = captcha.id
        return captcha

    def get_captcha_img(self, captcha):
        """
        Get url for captcha image
        :param captcha: captcha object or captcha id
        :return: url for captcha image
        """
        if isinstance(captcha, Captcha):
            captcha = captcha.id

        return f'{self._url}api/captcha/2chaptcha/image/{captcha}'

    def set_captcha_answer(self, captcha, value):
        """
        Check captcha answer
        :param captcha: captcha object
        :param value: captcha answer
        :return: bool
        """
        if self._get(f'api/captcha/2chaptcha/check/{captcha.id}?value={value}')['result'] == 1:
            captcha.answer = value
            return True
        else:
            raise Exception('Wrong captcha')

        # def get_settings(self):  # pragma: no cover
        #     """Fetching settings"""
        #     return Settings(self._get('/wakaba.pl?task=api&code=getsettings'))

    def send_post(self, board, thread, comment, email, captcha):  # pragma: no cover
        if isinstance(thread, Thread):
            thread = thread.num
        self.thread = thread

        if board and self.board_exist(board):  # pragma: no cover
            self.board = board

        post = {
            'json': 1,
            'task': 'post',
            'board': self.board,
            'thread': self.thread,
            'email': email,
            'comment': comment,
            'captcha_type': captcha.type,
            '2chaptcha_id': captcha.id,
            '2chaptcha_value': captcha.answer
        }

        try:
            url = url_join(self._url, 'makaba/posting.fcgi')
            print(post)
            response = requests.post(url, data=post, files={'': ''})
            return response.json()
        except requests.HTTPError as e:
            print('Error send post: {msg}'.format(msg=e))

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
