import api2ch

api = api2ch.Api('abu')

thread = api.get_thread(42375)

print(f'Total {len(thread)} posts in thread')

for post in thread:
    print(post.num, post.comment, post.files if post.files else 'No files')
