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
    WrongTypeWarning,
)
from pyfygentlescrap.yahoo.yahoo_shared import (
    _get_http_response,
    _strftime,
    _yahoo_regions,
)

logger = logging.getLogger(__name__)


def _empty_dataframe():
    """Returns an empty dataFrame with some columns name."""
    cols = ["earningscount", "economiceventcount", "ipoinfocount", "splitscount"]
    return pandas.DataFrame(columns=cols)


def _body(region, startdatetime, enddatetime):
    # return the body content of the GET request
    # startdatetime, enddatetime: examples "2021-05-16" "2021-05-22"
    startdatetime = _strftime(startdatetime, "%Y-%m-%d")
    enddatetime = _strftime(enddatetime, "%Y-%m-%d")
    return {
        "offset": 0,
        "joinField": "startdatetime",
        "sortField": "startdatetime",
        "includeFields": ["startdatetime"],
        "fillNA": "pad",
        "aggregation": {
            "operator": "date_hist",
            "operands": [
                {"operator": "eq", "operands": ["field", "startdatetime"]},
                {"operator": "eq", "operands": ["interval", "1d"]},
            ],
        },
        "entityIdType": ["earnings", "splits", "IPO_INFO", "ECONOMIC_EVENT"],
        "query": {
            "operator": "and",
            "operands": [
                {
                    "operator": "btwn",
                    "operands": ["startdatetime", startdatetime, enddatetime],
                },
                {"operator": "eq", "operands": ["region", region]},
            ],
        },
    }


def nb_events_available(region="France", from_date=0, to_date=0, session=None):
    """
    Returns the number of events available for the region.

    Args:
        region (str): Region to scrap. The full list is available at
            `<https://finance.yahoo.com/screener/new.>`_.
        event_type (str): either `all`, `earnings`, `splits', `IPO_INFO`,
            `ECONOMIC_EVENT`
        from (): bla bla
        to (): bla bla

    Example:

    >>> import pyfygentlescrap as pfgs
    >>> pfgs.nb_events_available('France', event_type='earnigs')

    """

    if not isinstance(region, str):
        WrongTypeWarning.warn(region, str)
        return _empty_dataframe()
    try:
        region = _yahoo_regions[region]
    except (IndexError, KeyError):
        InvalidRegionWarning.warn(region)
        return _empty_dataframe()

    if session is None:
        session = pfgs.yahoo_session()

    # OPTIONS request on both query servers:
    response = _get_http_response(
        "OPTIONS",
        path="v1/finance/visualization",
        params=session.default_params(),
        headers=session.headers,
    )

    # POST request on both query servers:
    response = _get_http_response(
        "POST",
        path="v1/finance/visualization",
        params=session.default_params(formatted=False),
        headers=session.headers,
        body=_body(region, from_date, to_date),
    )

    # Parsing results:
    try:
        _json = json.loads(response.text)
        _json = _json["finance"]["result"][0]
    except (JSONDecodeError, AttributeError, IndexError, KeyError):
        InvalidResponseWarning.warn("Request")
        return _empty_dataframe()

    try:
        cols = [x["id"] for x in _json["documents"][0]["columns"]]
        df = pandas.DataFrame(_json["documents"][0]["rows"], columns=cols)
    except (IndexError, KeyError):
        InvalidResponseWarning.warn("Request")
        return _empty_dataframe()

    df["startdatetime"] = pandas.to_datetime(df["startdatetime"], utc=True).dt.date
    df.set_index("startdatetime", inplace=True)
    return df
