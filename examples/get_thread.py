from api2ch import Api

api = Api('abu')

thread = api.get_thread(42375)

for post in thread:
    print(post.comment)
