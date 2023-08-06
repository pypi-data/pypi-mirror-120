from datetime import datetime

# default application date format string
DATE_FORMAT_STRING = '%Y-%m-%d'
DATETIME_FORMAT_STRING = "%Y-%m-%d %H:%M:%S"


def str_to_date(s):
    """
    Converts given str in application date format to a date
    :param s: string t convert
    :return: str converted to datetime
    """
    return datetime.strptime(s, DATE_FORMAT_STRING)


def str_to_datetime(s):
    """
    Converts given str in application datetime format to a datetime
    :param s: string t convert
    :return: str converted to datetime
    """
    return datetime.strptime(s, DATETIME_FORMAT_STRING)


def date_to_str(d):
    """
    Converts a date to application date string format
    :param d:
    :return:
    """
    return d.strftime(DATE_FORMAT_STRING)


def datetime_to_str(d):
    """
    Converts a datetime to application date string format
    :param d:
    :return:
    """
    return d.strftime(DATETIME_FORMAT_STRING)


def clean_cme_quote(quote):
    """
    Cleans a CME Quote of unneeded charatcers
    :param quote: Quote to clean
    :return: Cleaned quote
    """
    return quote.replace(',', '').replace('A', '').replace('B', '').replace('-', '0')