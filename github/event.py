import iso8601

from util.constant import *


class Commit:
    '''Class to handle the commit object'''

    def __init__(self, commit_dict):
        self.commit_dict = commit_dict

    def is_distinct(self):
        return self.commit_dict[DISTINCT]

    def get_message(self):
        return self.commit_dict[MESSAGE]

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
                    (lambda commit: commit.is_distinct(),
                     map(lambda commit: Commit(commit),
                         self.event_dict[PAYLOAD][COMMITS])))
            return
