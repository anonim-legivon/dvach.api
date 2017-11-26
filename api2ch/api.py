"""2ch.hk API"""

__all__ = ('DvachApi', 'Message', 'BOARDS', 'BOARDS_ALL', 'URL')

from posixpath import join as url_join

import requests
import os
from addict import Dict
from simplejson import JSONDecodeError

from .exceptions import ExtraFilesError, FileSizeError, AuthRequiredError
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

URL = 'https://2ch.hk'


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

    __slots__ = ('bump_limit', 'category', 'default_name', 'enable_dices',
                 'enable_flags', 'enable_icons', 'enable_likes',
                 'enable_names', 'enable_oekaki', 'enable_posting',
                 'enable_sage', 'enable_shield', 'enable_subject', 'enable_thread_tags',
                 'enable_trips', 'icons', 'id', 'name', 'pages', 'sage', 'tripcodes')

    def __init__(self, settings):
        """
        Create object from dict with settings
        :param settings: dict with settings
        """
        self.bump_limit = settings.bump_limit
        self.category = settings.category
        self.default_name = settings.default_name
        self.enable_dices = settings.enable_dices
        self.enable_flags = settings.enable_flags
        self.enable_icons = settings.enable_icons
        self.enable_likes = settings.enable_likes
        self.enable_names = settings.enable_names
        self.enable_oekaki = settings.enable_oekaki
        self.enable_posting = settings.enable_posting
        self.enable_sage = settings.enable_sage
        self.enable_shield = settings.enable_shield
        self.enable_subject = settings.enable_subject
        self.enable_thread_tags = settings.enable_thread_tags
        self.enable_trips = settings.trips
        self.icons = settings.icons
        self.id = settings.id
        self.name = settings.name
        self.pages = settings.pages
        self.sage = settings.sage
        self.tripcodes = settings.tripcodes

    def __repr__(self):  # pragma: no cover
        return f'<Settings: {self.id}>'


class Thread:
    """Thread object"""
    __slots__ = ('reply_count', 'post', 'num')

    def __init__(self, thread):
        """
        Create object from dict with thread info
        :param thread: dict with thread info
        """
        self.reply_count = thread.posts_count
        self.post = Post(thread)
        self.num = self.post.num

    def __repr__(self):
        return f'<Thread: {self.num}>'


class Post:
    """Post object"""

    __slots__ = ('banned', 'closed', 'comment', 'date', 'email',
                 'endless', 'files', 'lasthit', 'name', 'num',
                 'number', 'op', 'parent', 'sticky', 'subject',
                 'tags', 'timestamp', 'trip')

    def __init__(self, post):
        """
        Create object from dict with post info
        :param post: dict with post info
        """
        self.banned = post.banned
        self.closed = post.closed
        self.comment = post.comment
        self.date = post.date
        self.email = post.email
        self.endless = post.endless
        self.files = [File(Dict(file)) for file in post.files]
        self.lasthit = post.lasthit
        self.name = post.name
        self.num = post.num
        self.number = post.number
        self.op = post.op
        self.parent = post.parent
        self.sticky = post.sticky
        self.subject = post.subject
        self.tags = post.tags
        self.timestamp = post.timestamp
        self.trip = post.trip

    def __repr__(self):
        return f'<Post: {self.num}>'


class File:
    """File object"""

    __slots__ = ('displayname', 'fullname', 'height', 'md5', 'name',
                 'nsfw', 'path', 'size', 'thumbnail', 'tn_height',
                 'tn_width', 'type', 'width')

    def __init__(self, file):
        """
        Create file object from dict of file params
        :param file: dict of file params
        """
        self.displayname = file.displayname
        self.fullname = file.fullname
        self.height = file.height
        self.md5 = file.md5
        self.name = file.name
        self.nsfw = file.nsfw
        self.path = file.path
        self.size = file.size
        self.thumbnail = file.thumbnail
        self.tn_height = file.tn_height
        self.tn_width = file.tn_width
        self.type = file.type
        self.width = file.width

    def __repr__(self):
        return f'<File: {self.name}>'


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
        :param files: Список файлов 1-8 (обрежется до 1-4 без пасскода)
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

        self.files = {}

        # Добавляем файл при наличии
        if files and 0 < len(files) <= 8:
            # а переменной files по ключу filesize - хранится размер файлов для передачи
            self.filesize = Dict({'size': 0})
            try:
                for file_name in files:
                    with open(file_name, 'rb') as file:
                        self.files[file.name] = file.read()
                    # определяем размер файла и добавляем его к общему объёму файлов
                    self.filesize.size += os.path.getsize(file_name) / 1000000
            except Exception as e:
                print("IO error:", e)
        else:
            self.files = {'': ''}

    def __repr__(self):
        return f'<Message: {self.payload}, Files: {self.files.keys() if self.files else []}, ' \
               f'File_Size: {self.filesize if self.files else []}>'


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
        url = f'{URL}/api/captcha/2chaptcha/image/{captcha.captcha_id}'

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
                self._boards[board] = Board(Dict({'id': board}))

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

    def send_post(self, message, captcha=None, passcode=None):
        """
        Отправляет сообщение
        :param message: Объект типа Message
        :param captcha: Объект типа Captcha
        :param passcode: Использовать ли passcode для отправки сообщения
        :return: Ответ сервера в случае успеха
        """
        if passcode:
            message.payload.usercode = self.passcode_data
            # при наличии файлов- проверяем их
            if message.files != {'': ''}:
                if len(message.files) > 8:
                    raise ExtraFilesError(files_len = len(message.files), passcode = True)
                elif message.filesize.size > 60:
                    raise FileSizeError(files_size = message.filesize.size, passcode = True)

        elif captcha:
            captcha_payload = {
                'captcha_type': captcha.captcha_type,
                '2chaptcha_id': captcha.captcha_id,
                '2chaptcha_value': captcha.captcha_value
                }
            message.payload.update(captcha_payload)
            # при наличии файлов проверяем их
            if message.files != {'': ''}:
                if len(message.files) > 4:
                    raise ExtraFilesError(files_len = len(message.files), passcode = False)
                elif message.filesize.size > 20:
                    raise FileSizeError(files_size = message.filesize.size, passcode = False)
        else:
            raise AuthRequiredError()

        try:
            response = self.__Session.post(url='makaba/posting.fcgi',
                                           data=message.payload,
                                           files=message.files)
        except Exception as e:
            print('Error send post: {msg}'.format(msg=e))
            return False
        else:
            return response

    def find(self, board=None, thread=None, patterns=None, antipatterns=None):
        """
        Поиск тредов по заданным строкам в шапке
        :param board: ИД борды на которой нужно искать тред по заданным строкам в ОП-посте
        :param thread: ИД треда или объект типа Thread в постах которого нужно провести поиск
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

        if isinstance(thread, Thread):
            thread = thread.num

        # TODO: Тут покрасивее сделать надо
        if thread:
            posts = self.get_thread(board=board, thread=thread)
            matched = [post for post in posts if any(subs in post.comment.lower() for subs in patterns) and all(
                subs not in post.comment.lower for subs in antipatterns)]
        else:
            threads = self.get_board(board=board)
            matched = [thread for thread in threads if
                       any(subs in thread.post.comment.lower() for subs in patterns) and all(
                           subs not in thread.post.comment.lower() for subs in antipatterns)]

        return matched

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
        return f'<Api: {self.board.id}>'
