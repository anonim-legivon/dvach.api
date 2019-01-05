from api2ch import DvachApi

api = DvachApi(board='b')

print('Поиск тредов на доске:')
matched_threads = api.find(patterns=['webm', 'fap', 'фап'],
                           anti_patterns=['trap', 'трап', 'black'])

for thread in matched_threads:
    print(thread.num, thread.reply_count, thread.post.comment)

print(f'\nПоиск постов в тредах {[thread.num for thread in matched_threads]}:')
matched_posts = sum(
    [api.find(thread=thread.num, patterns=['соус']) for thread in
     matched_threads], [])

for post in matched_posts:
    print(post.num, post.comment)
