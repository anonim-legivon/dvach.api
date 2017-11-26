import json
from addict import Dict
from posixpath import join as url_join
from .exceptions import CaptchaValueError

URL = 'https://2ch.hk'


class Captcha:
    """Объект Captcha"""

    def __init__(self, captcha_id):
        self.captcha_type = '2chaptcha'
        self.captcha_id = captcha_id
        self.captcha_value = None

    def set_answer(self, answer):
        self.captcha_value = answer

        if not type(self.captcha_value) == int:
            raise CaptchaValueError

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

        captcha_response = self.__Session.get(url_join(URL, f'api/captcha/2chaptcha/service_id')).content
        if json.loads(captcha_response)['result'] == 1:
            captcha_id = json.loads(captcha_response)['id']

            return Captcha(captcha_id)
        else:
            return False

    def get_captcha_img(self, captcha):
        """
        Метод для получения изображение капчи
        :param captcha: Объект типа Captcha
        :return: Словарь с ссылкой на капчу и её бинарное представление
        """
        captcha_image = self.__Session.get(
            url_join(URL, f'api/captcha/2chaptcha/image/{captcha.captcha_id}')
        ).content
        url = f'{URL}/api/captcha/2chaptcha/image/{captcha.captcha_id}'

        return Dict({'url': url, 'binary': captcha_image})

    def check_captcha(self, captcha):
        """
        Метод отвечает за проверку правельности решения капчи
        :return: Возвращает True/False в зависимости от праильности решения капчи
        """
        response = self.__Session.get(
            url_join(URL, f'api/captcha/2chaptcha/check/{captcha.captcha_id}?value={captcha.captcha_value}')
        ).content

        if json.loads(response)['result'] == 1:
            return True
        else:
            return False
