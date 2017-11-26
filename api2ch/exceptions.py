# TODO: Сделать обработчик исключений
class ChanApiException(Exception):
    pass


class ExtraFilesError(ChanApiException):
    def __init__(self, files_len, passcode):
        ChanApiException.__init__(self, f"""
        \nИсключение пораждается, когда вы пытаетесь передать более 4 файлов, при отсутствии пасскода. 
        Либо же вы передаёте слтшком много файлов.
        Вы передаёте - {files_len} файлов, пасскод - {'присутствует' if passcode else 'отсутствует'}.
        Максимальное количество файлов с пасскодом - 8, а без него - 4.""")
