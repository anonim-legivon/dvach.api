from addict import Dict

from .models import Board
from .settings import HIDDEN_BOARDS, CHAN_URL


def get_all_board_settings(client):
    boards = {}

    all_settings = client.request(
        url=f'{CHAN_URL}/makaba/mobile.fcgi?task=get_boards')

    for key in all_settings.keys():
        for settings in all_settings[key]:
            boards[settings['id']] = Board(settings)

    # докидываем скрытых борд, на которые Абу не дает настроек
    for board in HIDDEN_BOARDS:
        if board not in boards.keys():
            boards[board] = Board(Dict({'id': board}))

    return boards
