import requests
import argparse
import time
import curses
import re


def main():
    parser = argparse.ArgumentParser(
        description="Print per second stats from expvars")
    parser.add_argument("--url", default="http://localhost:6060",
                        help="The URL from where to read the values")
    parser.add_argument("--filter", default=None,
                        help="Filter metrics by this search regexp")
    args = parser.parse_args()

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    last_vals = {}

    # running average for last 30 measurements
    N = 30
    avg_vals = {}
    now = time.time()
    reset = True

    while True:
        try:
            time.sleep(1.0)

            r = requests.get(args.url + "/debug/vars")
            json = r.json()

            stdscr.erase()

            if reset:
                now = time.time()
                last_vals = {}
                reset = False

            last = now
            now = time.time()
            dt = now - last

            for key, total in json.items():
                if args.filter is not None:
                    if re.search(args.filter, key) is None:
                        continue

                if isinstance(total, (int, long, float)):
                    if key in last_vals:
                        per_sec = (total - last_vals[key])/dt
                        if key not in avg_vals:
                            avg_vals[key] = []
                        avg_vals[key].append(per_sec)
                        if len(avg_vals[key]) > N:
                            avg_vals[key] = avg_vals[key][1:]
                        avg_sec = sum(avg_vals[key])/len(avg_vals[key])
                    else:
                        per_sec = "na"
                        avg_sec = "na"
                    last_vals[key] = total
                    try:
                        stdscr.addstr("{}: {}/s (avg: {}/s) (total: {})\n"
                                      .format(key, per_sec, avg_sec, total))
                    except Exception, e:
                        raise Exception("curses.addstr fail. Resize the " +
                                        "terminal window or use the filter" +
                                        "option: {}".format(e))
            stdscr.refresh()
        except requests.ConnectionError:
            reset = True
            last_vals = {}
            avg_vals = {}

if __name__ == "__main__":
    main()
