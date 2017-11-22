import sys

sys.path.append("..")  # for dev
import api2ch

api = api2ch.Api('pr')
print(api.board.name)
print(api.board.category)
thread = api.get_thread(1087578)
for p in thread:
    print(p.comment)
api.get_captcha()
print(api.captcha_data)
# print(api.get_captcha_img(captcha))
# value = input('Captcha answer: ')
# api.set_captcha_answer(captcha, value)
# comment = '''Newfags cannot\n  T\nR E'''
# print(api.send_post(board='b', comment=comment, email='', thread=165433076, captcha=captcha))
