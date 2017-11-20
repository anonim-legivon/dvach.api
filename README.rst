api2ch for 2ch.hk
=================

|License|
|Contribs|
|Codacy Badge|
|Shield.io issues|

2ch.hk API Wrapper

Requirements
------------

-  Python (3.4, 3.5, 3.6)

Install
-------

::

    pip install dvach.api

Usage
-----

Getting threads on board
~~~~~~~~~~~~~~~~~~~~~~~~

::

    from api2ch import Api

    api = Api('b')

    board = api.get_board()

    for thread in board:
        print(f'Num: {thread.num}, Replies: {thread.reply_count}, Post: {thread.post.comment}')

Getting posts in thread
~~~~~~~~~~~~~~~~~~~~~~~

::

    from api2ch import Api

    api = Api('abu')

    thread = api.get_thread(42375)

    for post in thread:
        print(post.comment)

Getting top of threads on board
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from api2ch import Api

    api = Api()

    # board='доска', method='метод сортировки (views, score, posts), num=количество тредов
    top = api.get_top(board='pr', method='posts', num=10)

    for thread in top:
        print(thread)

Bug tracker
-----------

Warm welcome for suggestions and concerns

https://github.com/anonim-legivon/dvach.api/issues

License
-------

Apache License 2.0 - https://www.apache.org/licenses/LICENSE-2.0

.. |License| image:: https://img.shields.io/github/license/mashape/apistatus.svg
    :target: https://github.com/anonim-legivon/dvach.api
.. |Contribs| image:: https://img.shields.io/github/contributors/cdnjs/cdnjs.svg
    :target: https://github.com/anonim-legivon/dvach.api
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/6d3154f7d4514d10ac95495e0e06965b
    :target: https://www.codacy.com/app/fadedDexofan/dvach.api?utm_source=github.com&utm_medium=referral&utm_content=anonim-legivon/dvach.api&utm_campaign=Badge_Grade
.. |Shield.io issues| image:: https://img.shields.io/github/issues/badges/shields.svg
    :target: https://github.com/anonim-legivon/dvach.api
