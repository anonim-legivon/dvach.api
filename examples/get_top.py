from api2ch import Api

api = Api()

# board='доска', method='метод сортировки (views, score, posts), num=количество тредов
top = api.get_top(board='pr', method='posts', num=10)

for thread in top:
    print(thread)
