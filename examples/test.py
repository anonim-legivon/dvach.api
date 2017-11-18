import api2ch

api = api2ch.Api()

api.board = 'pr'

# for thread in api.get_board():
#    print(thread.post.comment)

# for thread in api.get_board():
#    print(thread.num)

for post in api.get_thread(1015124):
    print(post.comment)
