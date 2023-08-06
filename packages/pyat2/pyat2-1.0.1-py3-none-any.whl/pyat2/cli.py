import argparse
import datetime
import os
import time


def next_datetime(current: datetime.datetime, hour: int, **kwargs) -> datetime.datetime:
    repl = current.replace(hour=hour, **kwargs)
    while repl <= current:
        repl = repl + datetime.timedelta(days=1)
    return repl


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='command script.')
    parser.add_argument('time', help='time')
    args = parser.parse_args()
    now = datetime.datetime.now()
    hour, minute = map(int, args.time.split(':'))
    dd = next_datetime(now, hour, minute=minute)
    dd = dd.replace(second=0, microsecond=0)
    ddt = dd.timestamp()
    while 1:
        now_t = datetime.datetime.now().timestamp()
        if now_t >= ddt:
            os.system(f"sh {args.f} >> ~/pyat.log")
            break
        time.sleep(1)


if __name__ == '__main__':
    main()
