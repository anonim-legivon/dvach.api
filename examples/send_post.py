from api2ch.api import DvachApi, ApiSession
from api2ch.boards import Message
from api2ch.captcha import CaptchaHelper

api = DvachApi(board='test')

# искусственный пример пораждения ошибки ExtraFilesError(переизбыток файлов при отсутствии пасскода)
'''
files = ['2.jpg', '3.jpg', '2.jpg', '3.jpg', '3.jpg', '2.jpg', '3.jpg', '3.jpg', '2.jpg', '3.jpg']

message = Message(board_id=api.board.id, thread_id=6476, comment='Abu nyasha', sage=True, files=files)

print(api.send_post(message = message, captcha = True))

print(api.send_post(message = message, passcode = True))

'''
api_session = ApiSession()

helper = CaptchaHelper(api_session.session)
captcha = helper.get_captcha()

print(helper.get_captcha_img(captcha).url)
captcha.set_answer(input('Answer: '))

message = Message(board_id=api.board.id, thread_id=6476, comment='Abu nyasha', sage=True, files=['19Mb_file.webm'])

if helper.check_captcha(captcha):
    print(api.send_post(message = message, captcha = captcha))

# искусстыенный пример для тестирования отправки файлом при наличии пасскода
'''
message = Message(board_id=api.board.id, thread_id=6476, comment='Abu nyasha', sage=True, files=['12Mb_file.mp4', 
                                                                                                 '18Mb_file.mp4', 
                                                                                                 '19Mb_file.webm'
                                                                                                 ])

print(api.send_post(message = message, passcode = True))

message = Message(board_id=api.board.id, thread_id=6476, comment='Abu nyasha', sage=True, files=['75mb_file.mp4'])

print(api.send_post(message = message, passcode = True))

'''