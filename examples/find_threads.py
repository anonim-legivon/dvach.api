from api2ch import DvachApi

api = DvachApi(board='b')

matched_threads = api.find_threads(patterns=['webm'], antipatterns=['fap'])

for thread in matched_threads:
    print(thread.num, thread.reply_count, thread.post.comment)
