import api2ch

api = api2ch.Api('b')

board = api.get_board()

print(f'Total {len(board)} threads in {api.board.id}')

for thread in board:
    print(thread.num, thread.reply_count, thread.post.comment)
