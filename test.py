from api2ch import api2ch
api = api2ch.Api('test')

captcha = api.get_captcha()
print(api.get_captcha_img(captcha))
value = input('Captcha answer: ')
api.set_captcha_answer(captcha, value)
comment = '''Newfags cannot\n  T\nR E'''
print(api.send_post(board='test', comment=comment, email='', thread=1309, captcha=captcha))
