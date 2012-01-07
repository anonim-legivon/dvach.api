from api2ch import Api, Message

# create object api
dvach = Api()

# select section
dvach.board = 'pr'

# get settings (important)
dvach.get_settings()

# make message
post = Message(96266, "python api 3", "SAGE")

# fetch captcha
captcha = dvach.get_captcha()

# input decrypt captcha code
print captcha.url
cap = raw_input("enter captcha code: ")

# set decrypt captcha code
post.captcha = cap

# send post
dvach.send_post(post)
