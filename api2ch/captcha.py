from addict import Dict

from .settings import CHAN_URL


class Captcha:
    """Объект Captcha"""

    def __init__(self, captcha_id):
        self.captcha_type = '2chaptcha'
        self.captcha_id = captcha_id
        self.captcha_value = None

    def set_answer(self, answer):
        self.captcha_value = answer

    def __repr__(self):
        return f'Captcha type: {self.captcha_type}, ' \
               f'Captcha ID: {self.captcha_id}, ' \
               f'Captcha value: {self.captcha_value}>'


class CaptchaHelper:
    """Класс помошник при работе с капчёй."""

    def __init__(self, client):
        """
        Инициализирует сессию для капчи
        :param client: Сессия ApiSession
        """
        self.__ApiClient = client

    def get_captcha(self):
        """
        Метод отвечает за получение капчи
        :return: Объект типа Captcha
        """
        url = f'{CHAN_URL}/api/captcha/2chaptcha/service_id'
        captcha_response = Dict(
            self.__ApiClient.request(method='get', url=url).json())

        if captcha_response.result == 1:
            captcha_id = captcha_response.id
            return Captcha(captcha_id)

        return None

    def get_captcha_img(self, captcha):
        """
        Метод для получения изображение капчи
        :param captcha: Объект типа Captcha
        :return: Словарь с ссылкой на капчу и её бинарное представление
        """
        url = f'{CHAN_URL}/api/captcha/2chaptcha/image/{captcha.captcha_id}'
        captcha_image = self.__ApiClient.request(method='get', url=url).content

        return Dict({'url': url, 'binary': captcha_image})

    def check_captcha(self, captcha):
        """
        Метод отвечает за проверку правельности решения капчи
        :return: Возвращает bool в зависимости от праильности решения капчи
        """
        url = f'{CHAN_URL}/api/captcha/2chaptcha/check/{captcha.captcha_id}?' \
              f'value={captcha.captcha_value}'
        response = Dict(self.__ApiClient.request(method='get', url=url).json())

        if response.result == 1:
            return True

        return False
