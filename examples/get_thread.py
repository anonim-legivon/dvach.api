import api2ch

api = api2ch.DvachApi('test')

thread = api.get_thread(6476)

print(f'Total {len(thread)} posts in thread')

for post in thread:
    print(post.num, post.comment, post.files if post.files else 'No files')

print('\nФайлы в треде:')
for post in thread:
    for file in post.files:
        print(file.fullname, f'({file.name})', api2ch.URL + file.path)
