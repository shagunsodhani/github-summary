from datetime import datetime

from github.activity import summarise_commits
from util.config import parse_config
from util.constant import *

config_dict = parse_config(app_name=GITHUB)

config_dict[SINCEDATE] = datetime.now().timestamp() - 604800
summarise_commits(config_dict)
