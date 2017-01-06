from datetime import datetime

from github.activity import summarise_commits
from util.config import parse_config
from util.constant import *

config_dict = parse_config(app_name=GITHUB)

lookback_time = 604800

if (config_dict[LOOKBACK_TIME]):
    time_unit = config_dict[LOOKBACK_TIME][-1]
    time_unit_map = {
        's': 1,
        'm': 60,
        'h': 60 * 60,
        'd': 60 * 60 * 24,
        'w': 60 * 60 * 24 * 7
    }
    if(time_unit in time_unit_map):
        lookback_time = int(config_dict[LOOKBACK_TIME][:-1]) * time_unit_map[time_unit]

config_dict[SINCEDATE] = datetime.now().timestamp() - lookback_time

summarise_commits(config_dict)
