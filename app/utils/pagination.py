def calc_skips(per_page: int, page: int) -> int:
    return per_page * (page - 1)
