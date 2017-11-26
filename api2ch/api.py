"""2ch.hk API"""

__all__ = ('DvachApi', 'Message', 'URL')

import api2ch.exceptions as ex
from .boards import *
from .captcha import CaptchaHelper
from .helpers import *
from .session import *


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

        for board in HIDDEN_BOARDS:  # докидываем скрытых борд, на которые Абу не дает настроек
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
            # при наличии файлов- проверяем их
            if message.files != {'': ''}:
                if len(message.files) > 8:
                    raise ex.ExtraFilesError(files_len=len(message.files), passcode=True)
                elif message.filesize.size > 60:
                    raise ex.FileSizeError(files_size=message.filesize.size, passcode=True)

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
                    raise ex.ExtraFilesError(files_len=len(message.files), passcode=False)
                elif message.filesize.size > 20:
                    raise ex.FileSizeError(files_size=message.filesize.size, passcode=False)
        else:
            raise ex.AuthRequiredError()

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

    def board_exist(self, board):
        """
        Проверка существование доски в списке всех досок
        :param board: ИД доски. Например 'b'
        :return: boolean
        """
        return board in self._boards.keys()

    def __repr__(self):
        return f'<Api: {self.board.id}>'
