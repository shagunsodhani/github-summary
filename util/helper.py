from datetime import datetime


def timestamp_to_formatted_date(timestamp):
    '''Method to convert timestamp into date and print in the format
    Dec 26, 2016'''
    return datetime.utcfromtimestamp(int(timestamp)).strftime('%b %d, %Y')
