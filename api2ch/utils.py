"""2ch.hk API Utils"""


def list_merge(boards_dict):
    """
    Merge dict of boards into list
    :param boards_dict: dict of boards
    :return: list of boards
    """
    return sum(boards_dict.values(), [])
