# coding: utf-8
# !/usr/bin/python3

import json
import logging
import pandas
import pyfygentlescrap as pfgs
from json.decoder import JSONDecodeError
from pyfygentlescrap.yahoo.yahoo_shared import (
    _timestamp_to_datetime,
    _to_utc_timestamp,
    _get_http_response,
)
from pyfygentlescrap import InvalidResponseWarning, WrongTypeWarning


logger = logging.getLogger(__name__)


def _empty_dataframe():
    """Returns an empty dataFrame with some columns name."""
    cols = ["open", "high", "low", "close", "adjclose", "volume", "dividend", "split"]
    return pandas.DataFrame(columns=cols)


def _parse_query_to_pandas(http_response_text):
    """
    Parse the argument into ``json`` format and convert all the data
    into a ``pandas.DataFrame``.

    Args:
        http_response_text (str): a http requests.text response.

    Returns:
        ``pandas.DataFrame``
    """

    # Convert the parameter to json:
    try:
        _json = json.loads(http_response_text)
    except (JSONDecodeError, AttributeError):
        InvalidResponseWarning.warn("Request")
        return _empty_dataframe()

    try:
        _json = _json["chart"]["result"][0]
        # Creating a list of date based on timestamp:
        _date = list(map(_timestamp_to_datetime, _json["timestamp"]))
    except (IndexError, KeyError):
        InvalidResponseWarning.warn("Request")
        return _empty_dataframe()
    # Building the DataFrame with open/high/low/close/adjclose/volume :
    df = pandas.DataFrame(
        {
            "open": _json["indicators"]["quote"][0]["open"],
            "high": _json["indicators"]["quote"][0]["high"],
            "low": _json["indicators"]["quote"][0]["low"],
            "close": _json["indicators"]["quote"][0]["close"],
            "adjclose": _json["indicators"]["adjclose"][0]["adjclose"],
            "volume": _json["indicators"]["quote"][0]["volume"],
            "dividend": 0.0,
            "split": 1.0,
        },
        index=_date,
    )
    # Retrieving dividends:
    try:
        for timestamp, dividend in _json["events"]["dividends"].items():
            df.loc[_timestamp_to_datetime(timestamp), "dividend"] = dividend["amount"]
    except KeyError:
        pass
    # Retrieving splits:
    try:
        for timestamp, split in _json["events"]["splits"].items():
            split_ratio = float(split["numerator"]) / float(split["denominator"])
            df.loc[_timestamp_to_datetime(timestamp), "split"] = split_ratio
    except KeyError:
        pass
    # Flooring index to keep only days:
    df.index = df.index.floor("d")
    return df


def yahoo_historical_data(ticker="", from_date=0, to_date=0, session=None):
    """
    Downloads historical end of day values for a single ticker and returns
    a `DataFrame` object. This function mirrors the GET request that is sent
    when opening `<https://finance.yahoo.com/quote/^AAPL/history>`_ for
    example. If the `ticker` is not valid or if the GET request fails, then
    the returned value is a void DataFrame.

    Parameters:
        ticker (str): Yahoo ticker to download
        from_date, to_date (str, int, datetime): defines the starting and
            finishing dates period to download data. The order between
            ``from_date`` and ``to_date`` does not matter.

            ``int`` parameter is assumed to be an epoch UTC timestamp. For
            example ``1577836800`` is converted to 01/01/2020 00:00:00.

            ``str`` parameter is assumed to be ``YYYY-MM-DD`` or
            ``YYYY/MM/DD``.
        yahoo_session (pfgs.yahoo_session, optional):  Existing yahoo
            session. If no yahoo_session is provided, the function
            will open one for the duration of the function execution.
            The latter session will be lost when `yahoo_historical_data`
            function exit. For large data scrapping, the use of
            `yahoo_session` is higly recommended to reuse existing
            cookies and crumb values. It will also reduce the cpu
            usage.

    Returns:
        Return a ``pandas.DataFrame``. If the function fails, a
        void DataFrame is returned. No exception is raised.

    Example:
        Basic download of the ticker AAPL

        >>> import pyfygentlescrap as pfgs
        >>> pfgs.yahoo_historical_data('AAPL', "2020/01/01", "2020/12/31")
                     open   high    low ...     volume  dividend  split
        2020-01-02  74.06  75.15  73.80 ...  135480400      0.00   1.00
        2020-01-03  74.29  75.14  74.12 ...  146322800      0.00   1.00
        2020-01-06  73.45  74.99  73.19 ...  118387200      0.00   1.00
        2020-01-07  74.96  75.22  74.37 ...  108872000      0.00   1.00
        2020-01-08  74.29  76.11  74.29 ...  132079200      0.00   1.00
        ...           ...    ...    ... ...        ...       ...    ...
        2020-12-07 122.31 124.57 122.25 ...   86712000      0.00   1.00
        2020-12-08 124.37 124.98 123.09 ...   82225500      0.00   1.00
        2020-12-09 124.53 125.95 121.00 ...  115089200      0.00   1.00
        2020-12-10 120.50 123.87 120.15 ...   81312200      0.00   1.00
        2020-12-11 122.43 122.76 120.55 ...   86860000      0.00   1.00
        [240 rows x 8 columns]

    Example:
        Two years download of EOD for the ticker AAPL, then printing
        the dividend values.

        >>> import pyfygentlescrap as pfgs
        >>> df = pfgs.yahoo_historical_data('AAPL', "2019/01/01",
                 "2020/12/31")
        >>> print(df.loc[ df.dividend > 0])
                     open   high    low ...    volume  dividend  split
        2019-02-08  42.25  42.67  42.10 ...  95280000      0.18   1.00
        2019-05-10  49.35  49.71  48.19 ... 164834800      0.19   1.00
        2019-08-09  50.33  50.69  49.82 ...  98478800      0.19   1.00
        2019-11-07  64.68  65.09  64.53 ...  94940400      0.19   1.00
        2020-02-07  80.59  80.85  79.50 ... 117684000      0.19   1.00
        2020-05-08  76.41  77.59  76.07 ...  33512000      0.82   1.00
        2020-08-07 113.21 113.68 110.29 ... 198045600      0.20   1.00
        2020-11-06 118.32 119.20 116.13 ... 114457900      0.20   1.00
    """
    if not isinstance(ticker, str):
        WrongTypeWarning.warn(ticker, str, "A void DataFrame will be return.")
        return _empty_dataframe()

    if session is None:
        session = pfgs.yahoo_session()

    from_date = _to_utc_timestamp(from_date)
    to_date = _to_utc_timestamp(to_date)
    if from_date > to_date:
        (from_date, to_date) = (to_date, from_date)
    to_date = to_date + 86399  # 24h == 86400 seconds

    # Building url requests:
    params = session.default_params()
    params["events"] = "div|split"
    params["includeAdjustedClose"] = True
    params["interval"] = "1d"
    params["period1"] = int(from_date)
    params["period2"] = int(to_date)
    params["events"] = "div|split"

    # POST request on both query servers:
    # example POST https://query1.finance.yahoo.com/v8/finance/chart/AAPL?
    #              formatted=true&crumb=sNMjrPA8yqY&lang=en-US&region=US&
    #              events=div|split&includeAdjustedClose=true&interval=1d&
    #              period1=1588291200&period2=1621641600
    response = _get_http_response(
        "GET",
        path=f"v8/finance/chart/{ticker}",
        params=params,
        headers=session.headers,
    )

    # Parsing result:
    try:
        response = response.text
    except (AttributeError, IndexError):
        InvalidResponseWarning.warn("POST http request")
        return _empty_dataframe()
    else:
        df = _parse_query_to_pandas(response)
        logger.debug(f"Request was parsed. {len(df)} value(s) were found.")
        return df
