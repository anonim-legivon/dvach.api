import sys

sys.path.append("..")  # for dev
import api2ch

api = api2ch.Api(board='pr')
captcha_data = api.Captcha

print(api.board.name)
print(api.board.category)

api.set_headers({
        'User-agent': 'Huita Browser'
                      'Huita/1234.321 Abu Nyasha'
    })
print(api.board.id)
b = api.get_board()
for t in b:
    print(t.post.comment)
thread = api.get_thread(1057688)
for p in thread:
    print(p.num)

image_data = api.Captcha.get_captcha_img()


if captcha_data:

    '''
    Для дальнейшей проверки можно скачать изображение, затем ввести в поле капчу и отправить на проверку, в ответ получен
    результат True/False
    '''

    with open('im.png', 'wb') as out_image:
        out_image.write(captcha_data.captcha_image)

    captcha_data.captcha_answer = input('Введите решение капчи: ')

    answer = api.Captcha.check_captcha(captcha_id=captcha_data.captcha_id, answer=captcha_data.captcha_answer)

    if answer:
        print("Капча решена правильно, отправляем пост ...")
        answer = api.send_post(thread='1057688', captcha_data=captcha_data, comment='Tets', files_list=('im.png','2.jpg','3.jpg'))

        if answer.Status == 'OK':
            print("Пост отправлен успешно")
        else:
            print("Ошибка при оптравке поста")
            print(answer)

# print(api.get_captcha_img(captcha))
# value = input('Captcha answer: ')
# api.set_captcha_answer(captcha, value)
# comment = '''Newfags cannot\n  T\nR E'''
# print(api.send_post(board='b', comment=comment, email='', thread=165433076, captcha=captcha))
