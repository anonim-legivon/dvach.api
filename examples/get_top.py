import api2ch

api = api2ch.Api('abu')

# Top 10 threads sorted by posts count
top = api.get_top(method='post', num=10)

for thread in top:
    print(thread)
