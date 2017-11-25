"""2ch.hk API"""

__all__ = ('DvachApi', 'Board', 'Thread', 'Post', 'Message', 'BOARDS', 'BOARDS_ALL')

from posixpath import join as url_join

import requests
from addict import Dict
from simplejson import JSONDecodeError

from .utils import listmerge

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
        """
        Post url
        :param kwargs: kwargs for request
        :return: request response
        """
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
        if headers:
            self.session.headers.clear()
            self.session.headers.update(headers if headers else self.HEADERS)

    def update_proxies(self, proxies):
        if proxies:
            self.session.proxies.clear()
            self.session.proxies.update(proxies)


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
        self.comment = None
        self.num = None
        for key, value in post.items():
            setattr(self, key, value)

    def __repr__(self):
        return '<Post: {num}>'.format(num=self.num)


class Message:
    """Message object"""

    # формирование пайлоада сообщения
    def __init__(self, board_id, thread_id, comment='', email='', subject='', name='', sage=False, files=None):
        """
        Офрмируется пайлоад, добавляются файлы при наличии
        :param board_id: Доска
        :param thread_id: Номер треда
        :param comment: Тело сообщения
        :param email: email
        :param subject: Тема
        :param name: Имя
        :param sage: Вкл/Выкл сажу
        :param files: Список файлов 1-4 (1-8 при наличии соответствующего пасскода)
        """
        # формируем пайлоад
        self.payload = Dict({
            'json': 1,
            'task': 'post',
            'board': board_id,
            'thread': thread_id,
            'email': email,
            'name': name,
            'subject': subject,
            'comment': comment,
            'sage': 1 if sage else 0
        })

        # Добавляем файл при наличии
        # TODO: Тут еще глянуть, однострочник мне нравится, надо подумать с условием if
        if files and 0 < len(files) <= 8:
            self.files = {f'image{idx}': open(file, 'rb') for idx, file in enumerate(files, 1)}
        else:
            self.files = {'': ''}

    def __repr__(self):
        return f'<Message: {self.payload}, Files: {self.files}>'


class Captcha:
    """Объект Captcha"""

    def __init__(self, captcha_id):
        self.captcha_type = '2chaptcha'
        self.captcha_id = captcha_id
        self.captcha_value = None

    def set_answer(self, answer):
        self.captcha_value = int(answer)

    def __repr__(self):
        return f'Captcha type: {self.captcha_type}, Captcha ID: {self.captcha_id}, Captcha value: {self.captcha_value}>'


class CaptchaHelper:
    """Класс помошник при работе с капчёй."""

    def __init__(self, session):
        """
        Инициализирует сессию для капчи
        :param session: Сессия ApiSession
        """
        self.__Session = session

    def get_captcha(self):
        """
        Метод отвечает за получение капчи
        :return: Объект типа Captcha
        """
        captcha_response = self.__Session.get(f'api/captcha/2chaptcha/service_id')
        if captcha_response.result == 1:
            captcha_id = captcha_response.id

            return Captcha(captcha_id)
        else:
            return False

    def get_captcha_img(self, captcha):
        """
        Метод для получения изображение капчи
        :param captcha: Объект типа Captcha
        :return: Словарь с ссылкой на капчу и её бинарное представление
        """
        captcha_image = self.__Session.get(f'api/captcha/2chaptcha/image/{captcha.captcha_id}').content
        url = f'{URL}api/captcha/2chaptcha/image/{captcha.captcha_id}'

        return Dict({'url': url, 'binary': captcha_image})

    def check_captcha(self, captcha):
        """
        Метод отвечает за проверку правельности решения капчи
        :return: Возвращает True/False в зависимости от праильности решения капчи
        """
        response = self.__Session.get(f'api/captcha/2chaptcha/check/{captcha.captcha_id}?value={captcha.captcha_value}')

        if response.result == 1:
            return True
        else:
            return False


class DvachApi:
    """Объект DvachApi"""

    _boards = {}

    def __init__(self, board='b', proxies=None, headers=None):
        """
        Инициализация Api
        :param board: ИД доски
        """

        self.__Session = ApiSession(proxies=proxies, headers=headers)
        self.__get_all_settings()
        self.__board = None
        self.board = board
        self.settings = None
        self.CaptchaHelper = CaptchaHelper(self.__Session)
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

        for board in BOARDS_ALL:  # докидываем скрытых борд, на которые Абу не дает настроек
            if board not in self._boards.keys():
                self._boards[board] = Board({'id': board})

        return True

    def get_board(self, board=None):
        """
        Получение списка тредов доски
        :param board: ИД доски
        :return: Список объектов типа Thread
        """
        if not (board and self.board_exist(board)):  # pragma: no cover
            board = self.board.id

        threads = self.__Session.get(board, 'threads.json').threads

        return [Thread(thread) for thread in threads]

    def get_thread(self, thread, board=None):
        """
        Получения списка постов в треде
        :param thread: Номер треда
        :param board: ИД доски
        :return: Список объектов типа Post
        """
        if isinstance(thread, Thread):
            thread = thread.num

        if not (board and self.board_exist(board)):  # pragma: no cover
            board = self.board.id

        posts = self.__Session.get(board, f'res/{thread}.json').threads

        return [Post(post) for post in posts[0].posts]

    def get_top(self, board=None, method='views', num=5):
        """
        Топ тредов доски по заданным критериям
        :param board: Доска на которой нужно узнать топ тредов
        :param method: Метод сортировки (views, score, posts)
        :param num: Число тредов в топе
        :return: Список объектов типа Thread
        """
        if not (board and self.board_exist(board)):  # pragma: no cover
            board = self.board.id

        threads = self.__Session.get(board, 'threads.json').threads

        if method == 'views':
            threads = sorted(threads, key=lambda thread: (thread['views'], thread['score']), reverse=True)
        elif method == 'score':
            threads = sorted(threads, key=lambda thread: (thread['score'], thread['views']), reverse=True)
        elif method == 'posts':
            threads = sorted(threads, key=lambda thread: (thread['posts_count'], thread['views']), reverse=True)
        else:
            return []

        return [Thread(thread) for thread in threads[:num]]

    def auth_passcode(self, usercode):
        """
        Авторизация пасскода
        :param usercode: Пасскод
        """
        url = url_join(URL, 'makaba/makaba.fcgi')
        payload = {
            'task': 'auth',
            'usercode': usercode
        }
        response = self.__Session.post(url=url, data=payload)
        self.passcode_data = response.cookies['usercode_nocaptcha']

        return True

    def send_post(self, message, captcha=None, passcode=False):
        """
        Отправляет сообщение
        :param message: Объект типа Message
        :param captcha: Объект типа Captcha
        :param passcode: Использовать ли passcode для отправки сообщения
        :return: Ответ сервера в случае успеха
        """
        if passcode:
            message.payload.usercode = self.passcode_data
        elif captcha:
            captcha_payload = {
                'captcha_type': captcha.captcha_type,
                '2chaptcha_id': captcha.captcha_id,
                '2chaptcha_value': captcha.captcha_value
            }
            message.payload.update(captcha_payload)
        else:
            return False

        try:
            response = self.__Session.post(url='makaba/posting.fcgi',
                                           data=message.payload,
                                           files=message.files)
        except Exception as e:
            print('Error send post: {msg}'.format(msg=e))
            return False
        else:
            return response
        finally:
            # TODO: Вот тут глянуть надо, может как нибудь упростить получиться.
            if len(message.files):
                for file in message.files.values():
                    try:
                        file.close()
                    except AttributeError:
                        continue

    def find_threads(self, board=None, patterns=None, antipatterns=None):
        """
        Поиск тредов по заданным строкам в шапке
        :param board: ИД борды
        :param patterns: Список фраз для поиска в шапке
        :param antipatterns: Список фраз которые не должны всречаться в шапке
        :return: Список тредов удовлетворяющих условиям
        """
        if patterns is None:
            patterns = []
        if antipatterns is None:
            antipatterns = []

        if not (board and self.board_exist(board)):  # pragma: no cover
            board = self.board.id

        threads = self.get_board(board)

        matched_threads = [thread for thread in threads if
                           any(subs in thread.post.comment.lower() for subs in patterns) and all(
                               subs not in thread.post.comment.lower() for subs in antipatterns)]

        return matched_threads

    def set_headers(self, headers=None):
        """
        Установка заголовка запросов на лету
        :param headers:
        """
        self.__Session.update_headers(headers)
        return True

    def set_proxies(self, proxies=None):
        """
        Установка прокси на лету
        :param proxies:
        """
        self.__Session.update_proxies(proxies)
        return True

    @staticmethod
    def board_exist(board):
        """
        Проверка существование доски в списке всех досок
        :param board: ИД доски. Например 'b'
        :return: boolean
        """
        return board in BOARDS_ALL

    def __repr__(self):
        return '<Api: {board}>'.format(board=self.board.id)
