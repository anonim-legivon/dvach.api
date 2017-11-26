from api2ch import DvachApi

api = DvachApi(board='b')

print('Поиск тредов на доске:')
matched_threads = api.find(patterns=['webm'], antipatterns=['fap'])

for thread in matched_threads:
    print(thread.num, thread.reply_count, thread.post.comment)

print('\nПоиск постов в треде:')
matched_posts = sum([api.find(thread=thread.num, patterns=['бамп']) for thread in matched_threads], [])

for post in matched_posts:
    print(post.num, post.comment)
