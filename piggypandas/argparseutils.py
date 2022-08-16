from typing import Optional
import datetime
import re


class DateRange:
    from_date: datetime.date
    to_date: datetime.date

    def __init__(self, from_date: datetime.date, to_date: datetime.date):
        self.from_date = from_date
        self.to_date = to_date


def parse_month_range(arg: str, max_range_length: Optional[int] = None) -> DateRange:

    def _make_absolute_month_range(y: int, m: int) -> DateRange:
        d1 = datetime.date(y, m, 1)
        d2 = d1 + datetime.timedelta(days=32)
        d2 = datetime.date(d2.year, d2.month, 1) - datetime.timedelta(days=1)
        return DateRange(d1, d2)

    def _make_relative_month_range(m: int) -> DateRange:
        if m < 1:
            raise ValueError("Month range must not include the current month or the future")
        d2 = datetime.date.today()
        d1 = datetime.date(d2.year, d2.month, 1)
        for _ in range(m):
            d2 = d1 - datetime.timedelta(days=1)
            d1 = datetime.date(d2.year, d2.month, 1)
        return DateRange(d1, d2)

    result: Optional[DateRange] = None
    match = False
    arg = arg.strip()
    mo = re.match(r'^(\d\d\d\d)(\d\d)$', arg)
    if mo:
        result = _make_absolute_month_range(int(mo.group(1)), int(mo.group(2)))
        match = True
    else:
        mo = re.match(r'^(\d\d\d\d)(\d\d)-(\d\d\d\d)(\d\d)$', arg)
        if mo:
            r_from = _make_absolute_month_range(int(mo.group(1)), int(mo.group(2)))
            r_to = _make_absolute_month_range(int(mo.group(3)), int(mo.group(4)))
            if r_from.from_date > r_to.to_date:
                r_from = _make_absolute_month_range(int(mo.group(3)), int(mo.group(4)))
                r_to = _make_absolute_month_range(int(mo.group(1)), int(mo.group(2)))
            result = DateRange(r_from.from_date, r_to.to_date)
            match = True
        else:
            mo = re.match(r'^(\d+)$', arg)
            if mo:
                r_from = _make_relative_month_range(int(mo.group(1)))
                r_to = _make_relative_month_range(1)
                result = DateRange(r_from.from_date, r_to.to_date)
                match = True
            else:
                mo = re.match(r'^(\d+)-(\d+)$', arg)
                if mo:
                    r_to = _make_relative_month_range(int(mo.group(1)))
                    r_from = _make_relative_month_range(int(mo.group(2)))
                    if r_from.from_date > r_to.to_date:
                        r_to = _make_relative_month_range(int(mo.group(2)))
                        r_from = _make_relative_month_range(int(mo.group(1)))
                    result = DateRange(r_from.from_date, r_to.to_date)
                    match = True

    if not match:
        raise ValueError(f"Invalid month range: {ascii(arg)}")

    last_month_end = datetime.date.today()
    last_month_end = datetime.date(last_month_end.year, last_month_end.month, 1) - datetime.timedelta(days=1)
    if result.to_date > last_month_end:
        raise ValueError("Month range must not include the current month or the future")

    if max_range_length is not None:
        delta: datetime.timedelta = result.to_date - result.from_date
        if delta.days > max_range_length:
            raise ValueError(f"Range may not me more than {max_range_length} days")

    return result

