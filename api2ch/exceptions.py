class ChanApiException(Exception):
    pass


class ExtraFilesError(ChanApiException):
    def __init__(self, files_len, passcode):
        passcode_status = 'присутствует' if passcode else 'отсутствует'
        super().__init__(self, f"""
        Превышено максимальное количество файлов.
        Вы передаёте - {files_len} файлов, пасскод - {passcode_status}.
        Максимальное количество файлов с пасскодом - 8, а без него - 4.""")


class FileSizeError(ChanApiException):
    def __init__(self, files_size, passcode):
        passcode_status = 'присутствует' if passcode else 'отсутствует'
        super().__init__(self, f"""
        Превышен лимита размера файла.
        Общий размер файлов - {files_size} , пасскод - {passcode_status}.
        Максимальное размер файлов с пасскодом - 40-60 Mb, без него - 20 Mb.""")


class AuthRequiredError(ChanApiException):
    def __init__(self):
        super().__init__(self,
                         """Отсутствует или невалидны капча или пасскод.""")
