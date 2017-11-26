from .utils import listmerge
from addict import Dict
import os


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
