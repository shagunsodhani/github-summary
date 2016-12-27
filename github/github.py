from datetime import datetime

import iso8601
import requests as r

from util.config import parse_config
from util.constant import *

config_dict = parse_config(app_name=GITHUB)
base_url = config_dict[BASE_URL]
headers = {
    USERAGENT: config_dict[USERNAME]
}


def get_activity_user(username=config_dict[USERNAME],
                      since_date=datetime.now().timestamp() - 604800,
                      client_id=config_dict[CLIENT_ID],
                      client_secret=config_dict[CLIENT_SECRET]):
    '''Method to get all the activity of an user on github since `since_date`.
    Github API returns 30 items for each request (page).
    Fetching up to ten pages is supported, for a total of 300 events.
    Only events created within the past 90 days can be retrived.
    From: https://developer.github.com/v3/activity/events/#list-public-events
    '''

    endpoint = "{base_url}/users/{username}/events?client_id={client_id}" \
               "&client_secret={client_secret}".format(base_url=base_url,
                                                       username=username,
                                                       client_id=client_id,
                                                       client_secret=client_secret)
    head = r.head(url=endpoint, headers=headers)
    response = r.get(url=endpoint, headers=headers).json()
    while (response):
        for event in response:
            if (CREATED_AT in event):
                created_at = iso8601.parse_date(event[CREATED_AT]).timestamp()
                if (created_at < since_date):
                    return
                else:
                    yield event
            else:
                raise ValueError("Could not figure out the created_at time from the event object")
        if (NEXT in head.links):
            endpoint = head.links[NEXT][URL]
            response = r.get(url=endpoint, headers=headers).json()
            head = r.head(url=endpoint, headers=headers)
        else:
            return


