import iso8601

from util.constant import *


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
        return self.event_dict[REPO][NAME]
