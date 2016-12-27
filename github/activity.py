from datetime import datetime
from functools import reduce

import requests as r

from github.event import Event
from util.config import parse_config
from util.constant import *

config_dict = parse_config(app_name=GITHUB)
base_url = config_dict[BASE_URL]
headers = {
    USERAGENT: config_dict[USERNAME]
}


def get_activity_user(config_dict):
    '''Method to get all the activity of an user on github since `since_date`.
    Github API returns 30 items for each request (page).
    Fetching up to ten pages is supported, for a total of 300 events.
    Only events created within the past 90 days can be retrived.
    From: https://developer.github.com/v3/activity/events/#list-public-events
    '''
    username = config_dict[USERNAME]
    since_date = config_dict[SINCEDATE]
    client_id = config_dict[CLIENT_ID]
    client_secret = config_dict[CLIENT_SECRET]
    endpoint = "{base_url}/users/{username}/events?client_id={client_id}" \
               "&client_secret={client_secret}".format(base_url=base_url,
                                                       username=username,
                                                       client_id=client_id,
                                                       client_secret=client_secret)
    head = r.head(url=endpoint, headers=headers)
    response = r.get(url=endpoint, headers=headers).json()
    while (response):
        for _event in response:
            event = Event(_event)
            try:
                created_at = event.created_at()
                if (created_at < since_date):
                    return
                else:
                    yield event
            except ValueError as e:
                pass
        if (NEXT in head.links):
            endpoint = head.links[NEXT][URL]
            response = r.get(url=endpoint, headers=headers).json()
            head = r.head(url=endpoint, headers=headers)
        else:
            return


def get_commits_user(config_dict):
    '''Method to get all the commits of an user on github since `since_date`.
    Refer get_activity_user method for limits in number of commits that can be retrived.'''
    return filter(
        lambda event: event.check_event_type(PUSHEVENT), get_activity_user(config_dict)
    )


def summarise_commits(config_dict):
    '''Method to summarise the commits since `since_date`.'''
    repo_dict = {}
    for event in get_commits_user(config_dict):
        repo_name = event.get_repo_name()
        if repo_name not in repo_dict:
            repo_dict[repo_name] = []
        for commit in event.get_distinct_commits():
            # string_to_insert = "Commit Message = {commit_message}\nCommit URL = {commit_url}" \
            #     .format(commit_message=commit.get_message(), commit_url=commit.get_url())
            string_to_insert = "{commit_message}\t\t{commit_url}" \
                .format(commit_message=commit.get_message(), commit_url=commit.get_url())
            repo_dict[repo_name].append(string_to_insert)
    for repo_name in repo_dict:
        string_to_print = "In repo {repo_name}:\n" \
                              .format(repo_name=repo_name) \
                          + reduce(lambda str1, str2: str1 + "\n" + str2,
                                   map(lambda index_str_tuple:
                                       str(index_str_tuple[0]) + ": " + index_str_tuple[1],
                                       enumerate(repo_dict[repo_name], start=1))) + "\n"

        print(string_to_print)


config_dict[SINCEDATE] = datetime.now().timestamp() - 604800
summarise_commits(config_dict)
