import api2ch

api = api2ch.DvachApi('b')

# Top 10 threads sorted by posts count
top = api.get_top(method='posts', num=10)

for thread in top:
    print(thread.num, thread.reply_count, thread.post.comment)
