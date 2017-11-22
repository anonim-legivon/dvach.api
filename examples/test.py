import sys

sys.path.append("..")  # for dev
import api2ch

api = api2ch.Api('pr')
print(api.board.name)
print(api.board.category)
thread = api.get_thread(1087578)
for p in thread:
    print(p.comment)

image_data = api2ch.CaptchaHelper().get_captcha_img()
api.captcha_data = image_data

print(api.captcha_data)

'''
Для дальнейшей проверки можно скачать изображение, затем ввести в поле капчу и отправить на проверку, в ответ получен
результат True/False
'''

with open('im.png', 'wb') as out_image:
    out_image.write(api.captcha_data.captcha_img)

api.captcha_data.captcha_result = input('Введите решение капчи: ')

answer = api2ch.CaptchaHelper().check_captcha(captcha_id=api.captcha_data.captcha_id,
                                              answer=api.captcha_data.captcha_result)

print(answer)

# print(api.get_captcha_img(captcha))
# value = input('Captcha answer: ')
# api.set_captcha_answer(captcha, value)
# comment = '''Newfags cannot\n  T\nR E'''
# print(api.send_post(board='b', comment=comment, email='', thread=165433076, captcha=captcha))
