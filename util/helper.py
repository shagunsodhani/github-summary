import sys
from datetime import datetime

import requests as r


def timestamp_to_formatted_date(timestamp):
    '''Method to convert timestamp into date and print in the format
    Dec 26, 2016'''
    return datetime.utcfromtimestamp(int(timestamp)).strftime('%b %d, %Y')


def get_head_and_reponse(endpoint, headers):
    '''Method to get the head and response given an endpoint and headers'''
    try:
        head = r.head(url=endpoint, headers=headers)
        head.raise_for_status()
        response = r.get(url=endpoint, headers=headers)
        response.raise_for_status()
        return head, response.json()

    except r.exceptions.ConnectionError as e:
        print("Connection Error when accessing url: {url}. Due to a network problem like"
              "DNS failure, refused connection, etc".format(url=e.request.url))
        sys.exit(1)
    except r.exceptions.HTTPError as e:
        print("HTTP Error when accessing url: {url}".format(url=e.request.url))
        sys.exit(1)
    except r.exceptions.Timeout as e:
        print("Request Timeout for url: {url}".format(url=e.request.url))
        sys.exit(1)
    except r.exceptions.TooManyRedirects as e:
        print("Too many redirects for url: {url}".format(url=e.request.url))
        print(e)
        sys.exit(1)
