from datetime import datetime, timedelta

def week_range(dt: datetime):
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=7)
    return start, end
