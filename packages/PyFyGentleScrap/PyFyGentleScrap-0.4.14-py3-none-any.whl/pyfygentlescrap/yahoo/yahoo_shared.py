# coding: utf-8
# !/usr/bin/python3

import datetime as dt
import json
import logging
import pandas
import pyfygentlescrap as pfgs
import pytz
import re
import requests
import urllib
from pyfygentlescrap import (
    InvalidResponseWarning,
    NoInternetWarning,
    InvalidParameterWarning,
)
from requests.cookies import RequestsCookieJar
from requests.exceptions import ConnectTimeout, ConnectionError, RequestException


logger = logging.getLogger(__name__)


# List of Regions as defined in the yahoo screener, and its associated code:
_yahoo_regions = {
    "Argentina": "ar",
    "Austria": "at",
    "Australia": "au",
    "Belgium": "be",
    # "Bahrain": "bh",
    "Brazil": "br",
    "Canada": "ca",
    "Switzerland": "ch",
    "Chile": "cl",
    "China": "cn",
    "Czech Republic": "cz",
    "Germany": "de",
    "Denmark": "dk",
    "Egypt": "eg",
    "Spain": "es",
    "Finland": "fi",
    "France": "fr",
    "United Kingdom": "gb",
    "Greece": "gr",
    "Hong Kong": "hk",
    "Hungary": "hu",
    "Indonesia": "id",
    "Ireland": "ie",
    "Israel": "il",
    "India": "in",
    "Italy": "it",
    # "Jordan": "jo",
    "Japan": "jp",
    "South Korea": "kr",
    # "Kuwait": "kw",
    "Sri Lanka": "lk",
    # "Luxembourg": "lu",
    "Mexico": "mx",
    "Malaysia": "my",
    "Netherlands": "nl",
    "Norway": "no",
    "New Zealand": "nz",
    # "Peru": "pe",
    # "Philippines": "ph",
    # "Pakistan": "pk",
    # "Poland": "pl",
    "Portugal": "pt",
    "Qatar": "qa",
    "Russia": "ru",
    "Sweden": "se",
    "Singapore": "sg",
    # "Suriname": "sr",
    # "French Southern Territories": "tf",
    "Thailand": "th",
    # "Timor-Leste": "tl",
    # "Tunisia": "tn",
    "Turkey": "tr",
    "Taiwan": "tw",
    "United States": "us",
    "Venezuela": "ve",
    # "Vietnam": "vn",
    "South Africa": "za",
}


class yahoo_session:
    """
    When initializiing a ``yahoo_session`` object, it automatically scrap
    the `crumb` value, as well as relevant `cookies`. Theses two values are
    stored in:

        - ``self.crumb`` (str): crumb value.
        - ``self.cookies`` (requests.cookies.RequestsCookieJar): cookies.
        - ``self.cookies_msg`` (str): string compilation of the cookies values
            that is directly used by the ``requests`` package.

    A ``yahoo_session`` object is higly recommeded for an intense usage as
    it will be reusing the same cookies and crumb value (as well as probably
    IP adress !). Yahoo server has then less clues to detect
    ``PyFyGentleScrap`` as a scrapping software. It will also reduce cpu usage.

    Example:

        >>> import pyfygentlescrap as pfgs
        >>> s = pfgs.yahoo_session()
        >>> print(s.crumb)
        mnLBCbcZQrp
        >>> df = s.yahoo_ticker('AAPL')
        >>> print(df['shortName'])
        symbol
        AAPL    Apple Inc.
        Name: shortName, dtype: object

    Example:

        To illustrate CPU usage, with the ``timeit`` module.

        >>> module = "import pyfygentlescrap as pfgs"
        >>> code = "pfgs.yahoo_ticker('AAPL')"
        >>> print(timeit.timeit(stmt=code, setup=module, repeat=10))
        73.34050052800012

        >>> module = "import pyfygentlescrap as pfgs; s = pfgs.yahoo_session()"
        >>> code = "s.yahoo_ticker('AAPL')"
        >>> print(timeit.timeit(stmt=code, setup=module, repeat=10))
        5.578921830001491

        The reason behind is when directly calling a pyfygentlescrap function,
        the module will open a new session if not provided. This means a
        request is sent, and the response is parsed with the module ``re`` to
        find the ``crumb`` value as well as the cookies. This operation is
        long because an http request is sent, and the response needs to be
        completely parsed to find the ``crumb`` value.
    """

    def __init__(self, url="https://finance.yahoo.com/screener/new"):
        logger.debug("Initializing Yahoo session.")
        getYahoo = _get_yahoo_headers_and_crumb(url)
        self.crumb = getYahoo["crumb"]
        self.cookies = getYahoo["cookies"]
        self.headers = getYahoo["headers"]
        # self.default_params = _param(self.crumb)
        cookies = "" if len(self.cookies) == 0 else self.headers["Cookie"]
        logger.debug(
            f"Found crumb value: {self.crumb} / Found {len(self.cookies)} "
            f"cookie(s): {cookies}"
        )

    def default_params(self, formatted=True):
        return _param(self.crumb, formatted)

    def yahoo_equity_screener(self, region):
        return pfgs.yahoo_equity_screener(region, self)

    def nb_equities_available(self, region):
        return pfgs.nb_equities_available(region, self)

    def yahoo_historical_data(self, ticker, from_date, to_date):
        return pfgs.yahoo_historical_data(ticker, from_date, to_date, self)

    def yahoo_ticker(self, ticker):
        return pfgs.yahoo_ticker(ticker, self)


def _param(crumb, formatted=True):
    if formatted:
        return {
            "crumb": crumb,
            "lang": "en-US",
            "region": "US",
            "formatted": True,
            "corsDomain": "finance.yahoo.com",
        }
    else:
        return {
            "crumb": crumb,
            "lang": "en-US",
            "region": "US",
            "corsDomain": "finance.yahoo.com",
        }


def _headers(cookies=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) "
        "Gecko/20100101 Firefox/83.0",
        "Connection": "keep-alive",
        "Expires": "-1",
        "Upgrade-Insecure-Requests": "1",
    }
    if type(cookies) is RequestsCookieJar:
        cookies = [f"{x.name}={x.value}" for x in cookies]
        if len(cookies) > 0:
            headers["Cookie"] = "; ".join(cookies)
    return headers


def _get_yahoo_headers_and_crumb(
    url="https://finance.yahoo.com/screener/new",
    max_recursion=5,
    current_recursion=None,
):
    """
    Open https://finance.yahoo.com/screener/new by default, or any other
    adress, and returns a dict containing cookies and the crumb value.
    """
    current_recursion = 1 if current_recursion is None else current_recursion + 1
    if current_recursion > max_recursion:
        logger.warning("No valid crumb was found (RecursionWarning).")
        return {"crumb": "", "cookies": "", "headers": _headers()}
    with requests.session():
        headers = _headers()
        try:
            response = requests.get(url, headers=headers)
        except (ConnectTimeout, ConnectionError, RequestException):
            NoInternetWarning.warn()
            return {"crumb": "", "cookies": "", "headers": headers}
        txt = response.content.decode("utf-8")
        crumb = re.findall('"CrumbStore":{"crumb":"(.+?)"}', txt)
        crumb = crumb[0] if len(crumb) > 0 else ""
        if ("\\u002" in crumb) or (crumb == ""):
            return _get_yahoo_headers_and_crumb(url, max_recursion, current_recursion)
        return {
            "crumb": crumb,
            "cookies": response.cookies,
            "headers": _headers(response.cookies),
        }


def _to_utc_timestamp(date_arg, tzone="UTC", raise_error=False):
    """
    Returns the timestamp of an object given a timezone. This function is
    particularly used to define starting/ending timestamp of yahoo.com
    historical data url.

    Args:
        date_arg: Object to convert.
        tzone: timezone as string, the list is defined in the ``pytz`` module.
            Type ``pytz.all_timezones`` to see all the available tz.
        raise_error (bool): raise an error if set to ``True``

    Returns:
        A timestamp value (type: `int`).
    """
    if tzone is None:
        tzone = "UTC"
    try:
        if isinstance(date_arg, bool):
            raise ValueError
        elif isinstance(date_arg, (float, int)):
            return date_arg
        elif isinstance(date_arg, dt.datetime):
            return date_arg.replace(tzinfo=pytz.timezone(tzone)).timestamp()
        elif isinstance(date_arg, dt.date):
            ts = dt.datetime.combine(
                date_arg, dt.time(0, 0), tzinfo=pytz.timezone(tzone)
            )
            return ts.timestamp()
        return dt.datetime.timestamp(pandas.Timestamp(date_arg, tz=tzone))
    except ValueError:
        InvalidParameterWarning.warn(date_arg)
        if raise_error:
            raise ValueError
        return 0


def _timestamp_to_datetime(timestamp, tzone="UTC"):
    """
    Returns the datetime an object given a timestamp. This function gives
    the reverse value of `_to_utc_timestamp`.

    Args:
        timestamp: Timestamp to be converted
        tzone: timezone as string, the list is defined in the ``pytz`` module.
            Type ``pytz.all_timezones`` to see all the available tz.

    Returns:
        A datetime object.
    """
    # Note, the localization has yet to be programmed:
    if tzone is None:
        tzone = "UTC"
    try:
        date = dt.datetime.fromtimestamp(int(timestamp))
    except ValueError:
        return None
    date = date.astimezone(pytz.timezone(tzone)).replace(tzinfo=None)
    return date


def _strftime(obj, fmt):
    """
    Convert the parameter `obj` to a formatted date
    """
    try:
        obj = _to_utc_timestamp(obj, raise_error=True)
        obj = _timestamp_to_datetime(obj)
        return obj.strftime(fmt)
    except (ValueError, TypeError, InvalidParameterWarning):
        InvalidParameterWarning.warn(obj)
        return None


def _get_query_url(server_number, path, params=None):
    url = f"https://query{server_number}.finance.yahoo.com/" + path
    if params is not None:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    return url


def _get_http_response(method, path, params=None, headers=None, body=None):
    """Yahoo POST requests are actually:
    - Yahoo ticker detail download:
      https://queryX.finance.yahoo.com/v7/finance/quote?{params}
    - Yahoo equity screener:
      https://queryX.finance.yahoo.com/v7/finance/quote?{params}
    - Yahoo historical data:
      https://queryX.finance.yahoo.com/v8/finance/chart/{ticker}?"{params}

    This function send a POST or GET request on the 2 servers https://query1...
    and if fail on https://query2...
    """
    encoded_body = json.dumps(body).encode("UTF-8")

    # Sending the request on query1 server:
    url = _get_query_url(1, path, params)
    logger.debug(f"Sending requests {method.upper()} {url}.")
    try:
        if method.lower() == "get":
            response = requests.get(url, headers=headers, data=encoded_body)
        elif method.lower() == "post":
            response = requests.post(url, headers=headers, data=encoded_body)
        elif method.lower() == "options":
            response = requests.options(url, headers=headers, data=encoded_body)
    except (ConnectTimeout, ConnectionError, RequestException):
        pass
    else:
        if response.status_code == 200:
            return response

    logger.debug("Server 'query1' didn't responsed correctly.")

    # Sending the request on query2 server:
    url = _get_query_url(2, path, params)
    logger.debug(f"Sending requests {method.upper()} {url}.")
    try:
        if method.lower() == "get":
            response = requests.get(url, headers=headers, data=encoded_body)
        elif method.lower() == "post":
            response = requests.post(url, headers=headers, data=encoded_body)
    except (ConnectTimeout, ConnectionError, RequestException):
        NoInternetWarning.warn()
        return ""
    else:
        if response.status_code == 200:
            return response
    InvalidResponseWarning("Both servers query1 and query2")
    return ""
