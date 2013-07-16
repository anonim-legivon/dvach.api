import random
from api2ch import Api

# create object api
dvach = Api()

# select section
dvach.board = "pr"

# fetch list of threads
threads = dvach.get_board()

# select random thread and fetch posts
for post in dvach.get_thread(random.choice(list(threads))):
    print post
