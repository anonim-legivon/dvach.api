"""2ch.hk API"""

__all__ = ('Api', 'Board', 'Thread', 'Post', 'Message', 'BOARDS', 'BOARDS_ALL')

from posixpath import join as url_join

import requests
from addict import Dict
from simplejson import JSONDecodeError

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
             'kpop', 'vr', 'arg', 'char', 'obr', 'hv', '2d', 'wwe', 'ch', 'int', 'math', 'test']
}

BOARDS_ALL = listmerge(BOARDS)

URL = 'https://2ch.hk/'


class ApiSession:
    HEADERS = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) '
                      'Gecko/20100101 Firefox/52.0'
    }

    def __init__(self, proxies=None, headers=None):
        self.session = requests.Session()
        self.session.headers.update(headers if headers else self.HEADERS)
        if proxies:
            self.session.proxies.update(proxies)

    def get(self, *args):
        """
        Get url
        :param args: args for request
        :return:
        """
        url = url_join(URL, *args)
        try:
            response = self.session.get(url=url)
        except Exception as e:
            print('Something goes wrong:', e)
            return None
        else:
            try:
                return Dict(response.json())
            except JSONDecodeError:
                return response

    def post(self, **kwargs):
        url = url_join(URL, kwargs['url'])
        try:
            response = self.session.post(url=url, data=kwargs['data'], files=kwargs['files'])
        except Exception as e:
            print('Something goes wrong:', e)
            return None
        else:
            try:
                return Dict(response.json())
            except JSONDecodeError:
                return response

    def update_headers(self, headers):
        self.session.headers.clear()
        self.session.headers.update(headers)


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


# TODO доделать отправку файлов
class Message:
    """Message object"""

    # формирование пайлоада сообщения
    @staticmethod
    def create_payload(captcha_data, board_id, thread_id, comment, email=None, subject=None, name=None):
        payload = {
            'json': 1,
            'task': 'post',
            'board': board_id,
            'thread': thread_id,
            'email': email,
            'comment': comment,
            'subject': subject,
            'name': name,
            'captcha_type': '2chaptcha',
            '2chaptcha_id': captcha_data.captcha_id,
            '2chaptcha_value': captcha_data.captcha_result,
        }

        return payload

    # прикрепление файлов
    @staticmethod
    def add_file(bin_file=None):
        """
        Метод добавляет файл(ы) для отправки их вместе с постом
        :param bin_file: Адрес файла
        :return: Возвращает JSON с файлом, готовый к передаче на сервер
        """
        if bin_file:
            with open(bin_file, 'rb') as user_file:
                file = {'file': user_file}
            return file
        else:
            return {'': ''}


class CaptchaHelper:
    """
    Класс отвечает за работу с капчёй.
    """

    def __init__(self, session):
        """
        Инициализирует подключение для капчи
        :param session: Сессия ApiSession
        """

        self.__Session = session

    # получение изображения капчи
    def get_captcha_img(self):
        """
        Метод отвечает за получение изображения капчи
        :return: Возвращает словарь с полями содержащими ID капчи и изображение, либо же возбуждается ошибка
        """
        # переменная в которой будет содержаться словарь со значениями ID / captcha image link
        captcha_payload = Dict()
        # получаем ID качи
        captcha_response = Dict(self.__Session.get(f'api/captcha/2chaptcha/service_id'))
        if captcha_response.result == 1:
            captcha_payload.captcha_id = captcha_response.id
            # получаем изображение капчи
            captcha_image = self.__Session.get(f'api/captcha/2chaptcha/image/{captcha_response.id}')

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
        response = Dict(self.__Session.get(f'api/captcha/2chaptcha/check/{captcha_id}?value={answer}'))

        # check captcha
        if response.result == 1:
            return True
        else:
            return False


class Api:
    """Api object"""
    _boards = {}

    def __init__(self, board='b', proxies=None, headers=None):
        """
        :param board: board id. For example 'b'
        """

        self.__Session = ApiSession(proxies=proxies, headers=headers)
        self.__get_all_settings()
        self.logging = False
        self.__board = None
        self.board = board
        self.settings = None
        self.thread = None
        self.Captcha = CaptchaHelper(self.__Session)
        self.captcha_data = None
        self.passcode_data = None

    @property
    def board(self):
        return self.__board

    @board.setter
    def board(self, board):
        if board in self._boards.keys():
            self.__board = self._boards[board]
        else:
            self.__board = None

    def __get_all_settings(self):
        all_settings = self.__Session.get('makaba/mobile.fcgi?task=get_boards')

        for key in all_settings.keys():
            for settings in all_settings[key]:
                self._boards[settings['id']] = Board(settings)

        for board in BOARDS_ALL: # докидываем скрытых борд, на которые Абу не дает настроек
            if board not in self._boards.keys():
                self._boards[board] = Board({'id': board})

    def get_board(self):
        if self.board and self.board_exist(self.board):  # pragma: no cover
            self.board = self.board

        threads = self.__Session.get(self.board.id, 'threads.json').threads

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

        posts = self.__Session.get(self.board.id, f'res/{self.thread}.json').threads

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

        threads = self.__Session.get(self.board, 'threads.json').threads

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

    def auth_passcode(self, usercode):
        url = url_join(URL, 'makaba/makaba.fcgi')
        payload = {
            'task': 'auth',
            'usercode': usercode
        }
        response = self.__Session.post(url=url, data=payload)

        self.passcode_data = response.cookies['usercode_nocaptcha']

    def send_post(self, thread, comment, captcha_data, bin_file=None, subject=None, name=None, email=None):
        """
        Метод  в качестве параметров принимает данные для формирования пайлода сообщения
        :param thread: Номер треда
        :param comment: Тело поста
        :param captcha_data: addict.Dict() данные капчи от CaptchaHelper
        :param bin_file: Ссылка на файл для прикрепления к посту
        :param subject: Тема поста
        :param name: Имя
        :param email: Электронный адрес
        :return: Тело ответа сервера, при ошибке - возвращает False(будет возбуждать ошибку)
        """
        if isinstance(thread, Thread):
            thread = thread.num
        self.thread = thread

        if self.board and self.board_exist(self.board):  # pragma: no cover
            self.board = self.board

        message_payload = Message().create_payload(captcha_data=captcha_data,
                                                   board_id=self.board.id,
                                                   thread_id=thread,
                                                   comment=comment,
                                                   email=email,
                                                   subject=subject,
                                                   name=name)

        # TODO доделать отправку файлов
        message_file = {'': ''}  # Message().add_file(bin_file = bin_file)

        try:
            response = self.__Session.post(url='makaba/posting.fcgi',
                                           data=message_payload,
                                           files=message_file)
            return response
        except Exception as e:
            print('Error send post: {msg}'.format(msg=e))
            return False

    def set_headers(self, headers):
        self.__Session.update_headers(headers)

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
