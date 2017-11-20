from api2ch import api2ch

api = api2ch.Api('b')

captcha = api.get_captcha()
print(api.get_captcha_img(captcha))
value = input('Captcha answer: ')
api.set_captcha_answer(captcha, value)
print(api.send_post(board='b', comment='test test test', email='', thread=165363341, captcha=captcha))
