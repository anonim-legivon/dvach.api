# TODO: Сделать обработчик исключений
class ChanApiException(Exception):
    pass


class ChanApiError(ChanApiException):
    __slots__ = ['Error', 'Reason']

    def __init__(self, chan_error_data):
        super(ChanApiError, self).__init__()
        self.error_data = chan_error_data
        pass
