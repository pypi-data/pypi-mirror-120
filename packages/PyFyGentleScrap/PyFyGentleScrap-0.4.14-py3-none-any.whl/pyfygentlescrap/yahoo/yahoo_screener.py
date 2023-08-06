# coding: utf-8
# !/usr/bin/python3

import json
import logging
import pandas
import pyfygentlescrap as pfgs
from json.decoder import JSONDecodeError
from pyfygentlescrap import (
    InvalidRegionWarning,
    InvalidResponseWarning,
    MarketOpenWarning,
    WrongTypeWarning,
)
from pyfygentlescrap.yahoo.yahoo_shared import _get_http_response, _yahoo_regions

logger = logging.getLogger(__name__)


def _parse_query_to_pandas(json_response):
    """
    pre-parsed requests to convert the data into a ``pandas.DataFrame``.

    Args:
        json_response: a valid json response

    Returns:
        DataFrame
    """
    df = pandas.DataFrame()
    quotes = json_response["finance"]["result"][0]["quotes"]
    for quo in quotes:
        df1 = pandas.DataFrame.from_dict(quo)
        df1 = df1.loc[["raw"]]
        df1.index = df1["symbol"]
        df1 = df1.drop(columns=["symbol"])
        df = pandas.concat([df, df1])
    return df


def _body(region):
    return {
        "size": 25,
        "offset": 0,
        "sortField": "intradaymarketcap",
        "sortType": "DESC",
        "quoteType": "EQUITY",
        "topOperator": "AND",
        "query": {
            "operator": "AND",
            "operands": [
                {
                    "operator": "or",
                    "operands": [{"operator": "EQ", "operands": ["region", region]}],
                }
            ],
        },
        "userId": "",
        "userIdType": "guid",
    }


def nb_equities_available(region="France", session=None):
    """Returns the number of equities available for the region.

    Args:
        region (str): Region to scrap. The full list is available at
            `<https://finance.yahoo.com/screener/new.>`_.

    Example:

    >>> import pyfygentlescrap as pfgs
    >>> pfgs.nb_equities_available('France')
    5085
    >>> pfgs.nb_equities_available('United States')
    15819
    """

    if not isinstance(region, str):
        WrongTypeWarning.warn(region, str)
        return 0
    try:
        region = _yahoo_regions[region]
    except (IndexError, KeyError):
        InvalidRegionWarning.warn(region)
        return 0

    if session is None:
        session = pfgs.yahoo_session()

    # POST request on both query servers:
    response = _get_http_response(
        "POST",
        path="v1/finance/screener/total",
        params=session.default_params(),
        headers=session.headers,
        body=_body(region),
    )

    # Parsing results:
    try:
        _json = json.loads(response.text)
    except (JSONDecodeError, AttributeError):
        InvalidResponseWarning.warn("Request")
        return 0
    try:
        total = _json["finance"]["result"][0]["total"]
    except (IndexError, KeyError):
        InvalidResponseWarning.warn("Request")
        return 0
    try:
        _json["finance"]["result"][0]["code"]
        InvalidResponseWarning.warn(region)
    except (IndexError, KeyError):
        return total


def yahoo_equity_screener(region="France", session=None):
    """
    Downloads live (or delayed) equities data given a region. This function
    mirrors the GET request that is returned by yahoo screener available at
    `<https://finance.yahoo.com/screener/new.>`_. The result type is a
    `pandas.DataFrame`. If the region parameter is not a valid country, order
    if the function fails for whaterver reason, the function will return a
    void DataFrame. No exception is raised.

    Args:
        region (str): Region to scrap. The full list is available at
            `<https://finance.yahoo.com/screener/new.>`_.
        yahoo_session (pfgs.yahoo_session, optional):  Existing yahoo
            session. If no yahoo_session is provided, the function
            will open one for the duration of the function execution.
            The latter session will be lost when `yahoo_historical_data`
            function exit. For large data scrapping, the use of
            `yahoo_session` is higly recommended to reuse existing
            cookies and crumb values. It will also reduce the cpu
            usage.

    Returns:
        `pandas.DataFrame` containing all the scrapped data.

    Example:
        The following example shows the download of all the tickers for
        Belgium. The returned DataFrame colums are particularely interesting:

            - ``regularMarketOpen``, ``regularMarketDayHigh``,
                ``regularMarketDayLow``, ``regularMarketPrice``: theses columns
                gives EOD data. Note that `regularMarketPrice` returns the
                live or delayed data if the market is openned.
            - ``regularMarketVolume``: volume for the current session.
            - ``marketCap``: capitalization.
            - ``marketState``: current market status.
            - ``regularMarketPreviousClose``: close for the previous session.

        >>> import pyfygentlescrap as pfgs
        >>> df = pfgs.yahoo_equity_screener(region='Belgium')
        >>> print(len(df))  # 200 values are returned
        200
        >>> print(df.columns)
        Index(['twoHundredDayAverageChangePercent',
               'fiftyTwoWeekLowChangePercent', 'language',
               'regularMarketDayRange', 'regularMarketDayHigh',
               'twoHundredDayAverageChange', 'askSize', 'twoHundredDayAverage',
               'bookValue', 'marketCap', 'fiftyTwoWeekHighChange',
               'fiftyTwoWeekRange', 'fiftyDayAverageChange',
               'firstTradeDateMilliseconds', 'exchangeDataDelayedBy',
               'averageDailyVolume3Month', 'trailingAnnualDividendRate',
               'fiftyTwoWeekLow', 'regularMarketVolume', 'market',
               'messageBoardId', 'priceHint', 'regularMarketDayLow',
               'exchange', 'sourceInterval', 'region', 'shortName',
               'fiftyDayAverageChangePercent', 'fullExchangeName',
               'financialCurrency', 'gmtOffSetMilliseconds',
               'regularMarketOpen', 'regularMarketTime',
               'regularMarketChangePercent', 'quoteType',
               'trailingAnnualDividendYield', 'averageDailyVolume10Day',
               'fiftyTwoWeekLowChange', 'fiftyTwoWeekHighChangePercent',
               'trailingPE', 'tradeable', 'currency', 'sharesOutstanding',
               'regularMarketPreviousClose', 'fiftyTwoWeekHigh',
               'exchangeTimezoneName', 'bidSize', 'regularMarketChange',
               'fiftyDayAverage', 'exchangeTimezoneShortName', 'marketState',
               'regularMarketPrice', 'ask', 'epsTrailingTwelveMonths', 'bid',
               'priceToBook', 'triggerable', 'longName',
               'earningsTimestampEnd', 'epsForward', 'earningsTimestampStart',
               'forwardPE', 'earningsTimestamp', 'newListingDate'],
              dtype='object')
        >>> print(df[['shortName', 'marketCap', 'exchange', 'currency']])
                           shortName      marketCap exchange currency
        symbol
        MSF.BR    MICROSOFT CORP SPL  1637461000192      BRU      USD
        INCO.BR           INTEL CORP   205712080896      BRU      USD
        CIS.BR      CISCO SYSTEM INC   186497761280      BRU      USD
        BOEI.BR       BOEING COMPANY   125048283136      BRU      USD
        ABI.BR              AB INBEV   113554939904      BRU      EUR
        ...                      ...            ...      ...      ...
        ROU.BR              ROULARTA      181946000      BRU      EUR
        EXM.BR                 EXMAR      162237696      BRU      EUR
        TISN.BR              TISCALI      161285680      BRU      EUR
        INCLU.BR                 NaN      159204448      BRU      EUR
        TEXF.BR                TEXAF      131889560      BRU      EUR
        [200 rows x 4 columns]
    """

    if not isinstance(region, str):
        WrongTypeWarning.warn(region, str, "A void DataFrame will be return.")
        return pandas.DataFrame()
    try:
        region = _yahoo_regions[region]
    except KeyError:
        InvalidRegionWarning.warn(region, "A void DataFrame will be return.")
        return pandas.DataFrame()

    # Get Yahoo session:
    if session is None:
        session = pfgs.yahoo_session()

    # POST request on both query servers:
    body = _body(region)
    response = _get_http_response(
        "POST",
        path="v1/finance/screener",
        params=session.default_params(),
        headers=session.headers,
        body=body,
    )

    # Parsing results:
    try:
        _json = json.loads(response.text)
    except (JSONDecodeError, AttributeError):
        InvalidResponseWarning.warn("Request", "A void DataFrame will be return.")
        return pandas.DataFrame()

    try:
        total = _json["finance"]["result"][0]["total"]  # Total number of equities
    except (IndexError, KeyError):
        InvalidResponseWarning.warn("Request", "A void DataFrame will be return.")
        return pandas.DataFrame()
    logger.debug(f"Yahoo POST response says {total} equities are available.")

    # Looping to scrap all equities:
    df = pandas.DataFrame()
    body["offset"] = 0
    body["size"] = 100
    while body["offset"] < total:
        # POST request on both query servers:
        response = _get_http_response(
            "POST",
            path="v1/finance/screener",
            params=session.default_params(),
            headers=session.headers,
            body=body,
        )
        # Parsing results:
        _json = json.loads(response.text)
        _df = _parse_query_to_pandas(_json)
        df = pandas.concat([df, _df])
        logger.debug(f"Scrapped equites: {len(df)}/{total}.")
        body["offset"] += 100

    if "REGULAR" in _df["marketState"].values:
        MarketOpenWarning.warn(region)
    df.drop_duplicates()
    return df
