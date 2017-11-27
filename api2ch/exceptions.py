class ChanApiException(Exception):
    pass


class ExtraFilesError(ChanApiException):
    def __init__(self, files_len, passcode):
        ChanApiException.__init__(self, f"""
        \nПораждается, при передаче слишком большого числа файлов.
        Вы передаёте - {files_len} файлов, пасскод - {'присутствует' if passcode else 'отсутствует'}.
        Максимальное количество файлов с пасскодом - 8, а без него - 4.""")


class FileSizeError(ChanApiException):
    def __init__(self, files_size, passcode):
        ChanApiException.__init__(self, f"""
        \nПораждается, при превышении лимита размера файла.
        Общий размер файлов - {files_size} , пасскод - {'присутствует' if passcode else 'отсутствует'}.
        Максимальное размер файлов с пасскодом - 40-60 Mb, а без него - 20 Mb.""")


class AuthRequiredError(ChanApiException):
    def __init__(self):
        ChanApiException.__init__(self, """\nПораждается, при отсутствии капчи и пасскода. Или их невалидности.""")
