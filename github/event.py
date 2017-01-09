import datetime
import re
import time
from functools import reduce

import iso8601

from util.constant import *


class Commit:
    '''Class to handle the commit object'''

    def __init__(self, commit_dict):
        self.commit_dict = commit_dict

    def is_distinct(self):
        return self.commit_dict[DISTINCT]

    def is_merge_commit(self):
        return self.get_message().startswith("Merge pull request") \
               or self.get_message().startswith("Merge branch")

    def get_message(self):
        return self.commit_dict[MESSAGE]

    def get_formatted_message(self):
        def format_line(_line):
            line = _line
            if (_line[0].islower()):
                line = _line[0].upper() + line[1:]
            if _line[-1] == DOT:
                line += DOT
            return line

        return reduce(lambda str1, str2: str1 + ". " + str2,
                      map(lambda line: format_line(line),
                          re.sub('\n+', '\n', self.get_message()).split('\n')))

    def get_sha(self):
        return self.commit_dict[SHA]

    def get_url(self):
        return self.commit_dict[URL] \
            .replace(APIDOT, EMPTYSTRING) \
            .replace(REPOSSLASH, EMPTYSTRING) \
            .replace(COMMITS, COMMIT)


class Event:
    '''Class to handle events returned by github api.'''

    def __init__(self, event_dict):
        self.event_dict = event_dict

    def created_at(self):
        '''Return the time the event was created'''
        if (CREATED_AT in self.event_dict):
            return iso8601.parse_date(self.event_dict[CREATED_AT]).timestamp()
        else:
            raise ValueError("Could not figure out the created_at time from the event object")

    def created_date_timestamp(self):
        '''Return the timestamp for the date the event was created.
        This method basically rounds of the timestamp to the date level'''
        if (CREATED_AT in self.event_dict):
            dt = iso8601.parse_date(self.event_dict[CREATED_AT])
            return int(time.mktime(datetime.date(dt.year, dt.month, dt.day).timetuple()))
        else:
            raise ValueError("Could not figure out the created_at time from the event object")

    def check_event_type(self, type_to_check):
        '''Check if the event type is same as type_to_check'''
        return self.event_dict[TYPE] == type_to_check

    def get_repo_name(self):
        '''Method to return the repo name'''
        return self.event_dict[REPO][URL] \
            .replace(APIDOT, EMPTYSTRING) \
            .replace(REPOSSLASH, EMPTYSTRING) \
            .replace(HTTPS, EMPTYSTRING) \
            .replace(HTTP, EMPTYSTRING)

    def get_distinct_commits(self):
        '''Method to return a list of commits belonging to the event.'''
        if COMMITS in self.event_dict[PAYLOAD]:
            return (filter
                    (lambda commit: commit.is_distinct() and not commit.is_merge_commit(),
                     map(lambda commit: Commit(commit),
                         self.event_dict[PAYLOAD][COMMITS])))
