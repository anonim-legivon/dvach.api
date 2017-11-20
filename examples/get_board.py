from api2ch import Api

api = Api('b')

board = api.get_board()

for thread in board:
    print(f'Num: {thread.num}, Replies: {thread.reply_count}, Post: {thread.post.comment}')
