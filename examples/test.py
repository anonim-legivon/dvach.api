import api2ch

api = api2ch.Api('pr')

# for thread in api.get_board():
#    print(thread.post.comment)

# for thread in api.get_board():
#     print(thread.num)

for post in api.get_thread(1015124):
    print(post.comment)

captcha = api.get_captcha()
print(api.get_captcha_img(captcha))
value = input()
result = api.set_captcha_answer(captcha, value)
print(result)
