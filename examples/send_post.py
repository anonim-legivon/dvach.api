from api2ch import DvachApi, Message
from api2ch import exceptions

# искусственный пример пораждения ошибки ExtraFilesError(переизбыток файлов при отсутствии пасскода)
files = ['2.jpg', '3.jpg', '2.jpg', '3.jpg', '3.jpg','2.jpg', '3.jpg', '3.jpg','2.jpg', '3.jpg']
passcode = True

if passcode and len(files) < 9:
    print('GJ!')
elif len(files) > 4 and not passcode:
    # TODO в рабочем коде `print` заменить на `raise`
    print(exceptions.ExtraFilesError(files_len = len(files), passcode = False))
elif passcode and len(files) > 9:
    # TODO в рабочем коде `print` заменить на `raise`
    raise exceptions.ExtraFilesError(files_len = len(files), passcode = True)
# конец искусственного примера

api = DvachApi(board='test')

helper = api.CaptchaHelper
captcha = helper.get_captcha()

print(helper.get_captcha_img(captcha).url)
captcha.set_answer(input('Answer: '))

message = Message(board_id=api.board.id, thread_id=6476, comment='Abu nyasha', sage=True, files=['2.jpg', '3.jpg'])

if helper.check_captcha(captcha):
    print(api.send_post(message, captcha))
