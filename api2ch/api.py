"""2ch.hk API"""

__all__ = ('Api', 'Board', 'Thread', 'Post', 'Message', 'Captcha', 'BOARDS', 'BOARDS_ALL', 'URL')

from posixpath import join as url_join

import requests
from addict import Dict

from .utils import listmerge

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

URL = 'https://2ch.hk/'


class Board:
    """Board object"""
    __rows__ = ('bump_limit', 'category', 'default_name', 'enable_dices',
                'enable_flags', 'enable_icons', 'enable_likes',
                'enable_names', 'enable_oekaki', 'enable_posting',
                'enable_sage', 'enable_shield', 'enable_subject', 'enable_thread_tags',
                'enable_trips', 'icons', 'id', 'name', 'pages', 'sage', 'tripcodes')

    def __init__(self, settings):
        """
        Create object from dict with settings
        :param settings: dict with settings
        """
        self.id = None
        for key, value in settings.items():
            setattr(self, key, value)

    def __repr__(self):  # pragma: no cover
        return '<Settings: {board}>'.format(board=self.id)


class Thread:
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


class Post:
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
class Message:
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


# TODO: Допил нужен блед
class Captcha:
    """
    Класс отвечает за работу с капчёй.
    """

    # получение изображения капчи
    def get_captcha_img(self, url):
        """
        Метод отвечает за получение изображения капчи
        :return: Возвращает словарь с полями содержащими ID капчи и изображение, либо же возбуждается ошибка
        """
        # переменная в которой будет содержаться словарь со значениями ID / captcha image link
        captcha_payload = Dict()
        # получаем ID качи
        captcha_response = Dict(requests.get(f'{url}api/captcha/2chaptcha/service_id').json())
        if captcha_response.result == 1:
            captcha_payload.captcha_id = captcha_response.id
            # получаем изображение капчи
            captcha_image = requests.get(f'{url}api/captcha/2chaptcha/image/{captcha_response.id}')

            captcha_payload.captcha_img = captcha_image.content

            return captcha_payload
        else:
            # TODO вызывать исключение при ошибке
            return False

    # проверка капчи
    def check_captcha(self, captcha_id, answer):
        """
        Метод отвечает за проверку правельности решения капчи
        :param captcha_id: ID капчи из метода get_captcha_img
        :param answer: Ответ пользователя на капчу
        :return: Возвращает True/False в зависимости от праильности решения
        """
        # check captcha
        result = requests.get(f'{URL}api/captcha/2chaptcha/check/{captcha_id}?value={answer}')

        json_result = result.json()

        # check captcha
        if json_result['result'] == 1:
            return True

        else:
            return False


# TODO: Прикрутить работу с пасскодом, там нужны куки
# class Passcode(object):
#     """Passcode object"""
#
#     def __init__(self, passcode):
#         """
#
#         :param passcode:
#         """
#         pass


class Api:
    """Api object"""
    _boards = {}

    def __init__(self, board=None):
        """
        :param board: board id. For example 'b'
        """
        self._http = requests.Session()
        self._http.headers.update({
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) '
                          'Gecko/20100101 Firefox/52.0'
        })
        self._get_all_settings()  # Подгружаем настройки всех борд, которые дают, дабы не дёргать каждый раз
        self.logging = False
        self.__board = None
        self.board = board
        self.settings = None
        self.thread = None
        self.captcha_data = None
        # if board and self.board_exist(board):  # pragma: no cover
        #     self.settings = self.get_settings()

    def _get(self, *args):
        """
        Get page
        :param url: url for request
        :return: raise or json object
        """
        url = url_join(URL, *args)
        try:
            response = self._http.get(url)
        except Exception as e:
            print('Something goes wrong:', e)
            return None
        else:
            return Dict(response.json())

    @property
    def board(self):
        return self.__board

    @board.setter
    def board(self, board):
        if board in self._boards.keys():
            self.__board = self._boards[board]
        else:
            self.__board = None

    def _get_all_settings(self):
        all_settings = self._get('makaba/mobile.fcgi?task=get_boards')
        for key in all_settings.keys():
            for settings in all_settings[key]:
                self._boards[settings['id']] = Board(settings)

    def get_board(self, board=None):
        """
        Get all threads from board
        :param board: board code
        :return: List of threads on board
        """
        if board and self.board_exist(board):  # pragma: no cover
            self.board = board

        threads = self._get(self.board.id, 'threads.json').threads

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

        posts = self._get(self.board.id, f'res/{self.thread}.json').threads

        return (Post(post) for post in posts[0].posts)

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

        threads = self._get(self.board, 'threads.json').threads

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
        Метод получает данные капчи (ID + изображение капчи)
        :return:
        """
        captcha = Captcha().get_captcha_img(URL)

        # проверка на наличие данных в ответе
        if captcha:
            self.captcha_data = captcha

    def send_post(self, board, thread, comment, email, captcha_answer):  # pragma: no cover
        if isinstance(thread, Thread):
            thread = thread.num
        self.thread = thread

        if board and self.board_exist(board):  # pragma: no cover
            self.board = board

        # отправляем капчу на проверку
        if self.captcha_data:
            captcha_result = Captcha().check_captcha(captcha_id=self.captcha_data.captcha_id, answer=captcha_answer)

            # проверка решения капчи
            if captcha_result:
                post = {
                    'json': 1,
                    'task': 'post',
                    'board': self.board.id,
                    'thread': self.thread,
                    'email': email,
                    'comment': comment,
                    'captcha_type': '2chaptcha',
                    '2chaptcha_id': self.captcha_data.captcha_id,
                    '2chaptcha_value': captcha_result
                }

                try:
                    url = url_join(URL, 'makaba/posting.fcgi')
                    response = self._http.post(url, data=post, files={'': ''})
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
        return '<Api: {board}>'.format(board=self.board.id)
