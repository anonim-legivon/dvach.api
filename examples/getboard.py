from api2ch import Api

# create object api
dvach = Api()

# select section
dvach.board = "pr"

# fetch list of threads
for thread in dvach.get_board():
    print thread
