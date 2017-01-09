"""Github-Summary.

Usage:
  main.py [-p profile] [-t lookbackTime] [-g groupBy]
  main.py (-h | --help)

Options:
  -h --help     Show this screen.
  -p profile    Choose which profile to use from config [default: github]
  -t lookbackTime  lookbackTime with units
  -g groupBy  group commits by repo or repo followed by date or date followed by repo.
"""

from datetime import datetime

from docopt import docopt

from github.activity import summarise_commits
from util.config import parse_config
from util.constant import *

if __name__ == '__main__':
    arguments = docopt(__doc__)
    appname = arguments['-p']
    config_dict = parse_config(app_name=appname)
    lookback_time = 604800

    if ('-t' in arguments and arguments['-t']):
        config_dict[LOOKBACK_TIME] = arguments['-t']

    if ('-g' in arguments and arguments['-g']):
        config_dict[GROUPY_BY] = arguments['-g']

    if (config_dict[LOOKBACK_TIME]):
        time_unit_map = {
            's': 1,
            'm': 60,
            'h': 60 * 60,
            'd': 60 * 60 * 24,
            'w': 60 * 60 * 24 * 7
        }
        time_unit = config_dict[LOOKBACK_TIME][-1]
        if (time_unit in time_unit_map):
            lookback_time = int(config_dict[LOOKBACK_TIME][:-1]) * time_unit_map[time_unit]

    config_dict[SINCEDATE] = datetime.now().timestamp() - lookback_time

    summarise_commits(config_dict)
