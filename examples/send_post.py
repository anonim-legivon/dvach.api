from api2ch import DvachApi, Message

api = DvachApi(board='test')

helper = api.CaptchaHelper()
captcha = helper.get_captcha()

print(helper.get_captcha_img(captcha).url)
captcha.set_answer(input('Answer: '))

message = Message(board_id=api.board.id, thread_id=6476, comment='Abu nyasha', sage=True, files=['2.jpg', '3.jpg'])

if helper.check_captcha(captcha):
    print(api.send_post(message, captcha))
