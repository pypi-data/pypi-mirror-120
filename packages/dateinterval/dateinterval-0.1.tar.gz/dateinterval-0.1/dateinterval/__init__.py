from typing import Iterable, Iterable
from datetime import datetime, date, timedelta


def summarize_date_ranges(d: Iterable[date], gap_toleration: timedelta = timedelta(1), only_missing=False) -> Iterable[Iterable[date]]:
    result = []
    c = [None, None]

    d = sorted(d)

    # invert the list
    if only_missing:
        min_dt = d[0]
        max_dt = d[-1]

        num_gaps = int((max_dt - min_dt) / gap_toleration)

        _d = {min_dt + i * gap_toleration for i in range(num_gaps)}

        d = list(set(_d) - set(d))

        d = sorted(d)

    for i, v in enumerate(d):
        if i == 0:
            c[0] = v
            continue

        prev_date = d[i - 1]
        if v <= (prev_date + gap_toleration):
            continue
        else:
            c[1] = prev_date
            result.append(c)
            c = [v, None]

    if c[1] == None:
        c[1] = d[-1]
        result.append(c)

    return result


def generate_interval_date_ranges(initial_dt: datetime, td: timedelta = timedelta(hours=6), steps: int = 20):
    last_date = initial_dt
    yield initial_dt

    for i in range(steps):
        next_dt = last_date + td
        last_date = next_dt

        yield next_dt
