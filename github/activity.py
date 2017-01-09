from functools import reduce

import requests as r

from github.event import Event
from util.config import parse_config
from util.constant import *
from util.helper import timestamp_to_formatted_date

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
    access_token = config_dict[ACCESS_TOKEN]
    if (client_secret and client_id):
        endpoint = "{base_url}/users/{username}/events?client_id={client_id}" \
                   "&client_secret={client_secret}".format(base_url=base_url,
                                                           username=username,
                                                           client_id=client_id,
                                                           client_secret=client_secret)
    elif (access_token):
        endpoint = "{base_url}/users/{username}/events?access_token={access_token}" \
            .format(base_url=base_url,
                    username=username,
                    access_token=access_token)
    else:
        endpoint = "{base_url}/users/{username}/events".format(base_url=base_url,
                                                               username=username)
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
    commit_list = []
    for event in get_commits_user(config_dict):
        repo_name = event.get_repo_name()
        created_date_timestamp = event.created_date_timestamp()
        for commit in event.get_distinct_commits():
            string_to_insert = "{commit_sha} - {commit_message}" \
                .format(commit_message=commit.get_formatted_message(), commit_sha=commit.get_sha())
            commit_list.append((repo_name, created_date_timestamp, string_to_insert))

    if (config_dict[GROUPY_BY] == 'rd'):
        _summarise_commits_grouped_by_repo_and_date(commit_list)
    elif (config_dict[GROUPY_BY] == 'dr'):
        _summarise_commits_grouped_by_date_and_repo(commit_list)
    else:
        _summarise_commits_grouped_by_repo(commit_list)


def _summarise_commits_grouped_by_repo(commit_list):
    '''Method to group commits by repo and summarise them'''
    data_dict = {}
    for (repo_name, _, string_to_insert) in commit_list:
        if (repo_name not in data_dict):
            data_dict[repo_name] = []
        data_dict[repo_name].append(string_to_insert)
    for repo_name in sorted(data_dict.keys()):
        print_commit_list(data_dict[repo_name], repo_name, created_date_timestamp=None)
        print("=============================================================================\n")


def _summarise_commits_grouped_by_repo_and_date(commit_list):
    '''Method to group commits by repo (and then date) and summarise them'''
    data_dict = {}
    for (repo_name, created_date_timestamp, string_to_insert) in commit_list:
        if (repo_name not in data_dict):
            data_dict[repo_name] = {}
        if (created_date_timestamp not in data_dict[repo_name]):
            data_dict[repo_name][created_date_timestamp] = []
        data_dict[repo_name][created_date_timestamp].append(string_to_insert)
    for repo_name in sorted(data_dict.keys()):
        string_to_print = "In repo {repo_name}:\n\n" \
            .format(repo_name=repo_name)
        print(string_to_print)
        for created_date_timestamp in data_dict[repo_name]:
            print_commit_list(data_dict[repo_name][created_date_timestamp],
                              repo_name=None,
                              created_date_timestamp=created_date_timestamp,
                              prefix_commit_string="\t")
        print("=============================================================================\n")


def _summarise_commits_grouped_by_date_and_repo(commit_list):
    '''Method to group commits by date (and then by repo) and summarise them'''
    data_dict = {}

    for (repo_name, created_date_timestamp, string_to_insert) in commit_list:
        if (created_date_timestamp not in data_dict):
            data_dict[created_date_timestamp] = {}
        if (repo_name not in data_dict[created_date_timestamp]):
            data_dict[created_date_timestamp][repo_name] = []
        data_dict[created_date_timestamp][repo_name].append(string_to_insert)
    for created_date_timestamp in sorted(data_dict.keys()):
        string_to_print = \
            "{created_date}:\n\n" \
                .format(created_date=timestamp_to_formatted_date(created_date_timestamp))
        print(string_to_print)
        for repo_name in sorted(data_dict[created_date_timestamp].keys()):
            print_commit_list(data_dict[created_date_timestamp][repo_name],
                              repo_name=repo_name,
                              created_date_timestamp=None,
                              prefix_commit_string="\t")
        print("=============================================================================\n")


def print_commit_list(commit_list,
                      repo_name=None,
                      created_date_timestamp=None,
                      prefix_commit_string=''):
    '''Method to print the commits from the list of commits'''

    if (repo_name):
        string_to_print = "In repo {repo_name}:\n\n" \
            .format(repo_name=repo_name)
    elif (created_date_timestamp):
        string_to_print = "{created_date}:\n" \
            .format(created_date=timestamp_to_formatted_date(created_date_timestamp))
    string_to_print += reduce(lambda str1, str2: str1 + "\n" + str2,
                              map(lambda index_str_tuple:
                                  prefix_commit_string + str(index_str_tuple[0]) + ": " + index_str_tuple[1],
                                  enumerate(commit_list, start=1))) + "\n"
    print(string_to_print)
