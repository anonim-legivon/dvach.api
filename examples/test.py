import api2ch

api = api2ch.Api('b')

thread = api.get_thread(165433076)
captcha = api.get_captcha()
print(api.get_captcha_img(captcha))
value = input('Captcha answer: ')
api.set_captcha_answer(captcha, value)
comment = '''Newfags cannot\n  T\nR E'''
print(api.send_post(board='b', comment=comment, email='', thread=165433076, captcha=captcha))
