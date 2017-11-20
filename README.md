# api2ch for 2ch.hk
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6d3154f7d4514d10ac95495e0e06965b)](https://www.codacy.com/app/fadedDexofan/dvach.api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=anonim-legivon/dvach.api&amp;utm_campaign=Badge_Grade)

2ch.hk API Wrapper

## Requirements

* Python (3.5, 3.6)

## Install

    pip install api2ch

## Usage

#### Getting threads on board
    from api2ch import Api

    api = Api('b')

    board = api.get_board()

    for thread in board:
    print(f'Num: {thread.num}, Replies: {thread.reply_count}, Post: {thread.post.comment}')

#### Getting posts in thread

    from api2ch import Api

    api = Api('abu')

    thread = api.get_thread(42375)

    for post in thread:
    print(post.comment)

#### Getting top of threads on board
    from api2ch import Api

    api = Api()

    # board='доска', method='метод сортировки (views, score, posts), num=количество тредов
    top = api.get_top(board='pr', method='posts', num=10)

    for thread in top:
    print(thread)

## Bug tracker

Warm welcome for suggestions and concerns

https://github.com/anonim-legivon/dvach.api/issues

## License

Apache License 2.0 - https://www.apache.org/licenses/LICENSE-2.0
