# coding: utf-8
# !/usr/bin/python3
""" Custom warnings messages. """

import warnings
import pyfygentlescrap as pfgs


def _full_msg(msg, additionnal_message):
    if additionnal_message is not None:
        return f"{msg} {additionnal_message}"
    return msg


class InvalidParameterWarning(Warning):
    """This warning is raised when a parameter has't the expected format."""

    def __init__(self, param, additionnal_message=None):
        self.msg = f"Parameter '{param}' is invalid."
        self.msg = _full_msg(self.msg, additionnal_message)

    def warn(region=None, additionnal_message=None):
        _warning = InvalidParameterWarning(region)
        warnings.warn(_warning.msg, category=InvalidParameterWarning)


class InvalidRegionWarning(UserWarning):
    """This warning is raised when the region parameter is not valid.

    Example:

        >>> import pyfygentlescrap as pfgs
        >>> pfgs.nb_equities_available(region='toto')
        pyfygentlescrap/warnings.py:54: InvalidRegionWarning: Region code
        'toto' is invalid. The available regions are: Argentina, Austria,
        Australia, Belgium, Brazil, (...), Venezuela, South Africa.
        warnings.warn(_warning.msg, category=InvalidRegionWarning)
        0
    """

    def __init__(self, region, additionnal_message=None):
        regions = ", ".join(pfgs.yahoo.yahoo_screener._yahoo_regions)
        self.msg = (
            f"Region code '{region}' is invalid. The available regions are: {regions}"
        )
        self.msg = _full_msg(self.msg, additionnal_message)

    def warn(region=None, additionnal_message=None):
        _warning = InvalidRegionWarning(region)
        warnings.warn(_warning.msg, category=InvalidRegionWarning)


class InvalidResponseWarning(UserWarning):
    """This warning is raised when the two servers
    https://query.finance.yahoo.com/ return unparsable or invalid responses.
    This warning may means that yahoo servers target ``pyfygentlescrap`` as a
    bot."""

    def __init__(self, subject, additionnal_message=None):
        self.msg = f"{subject} did not return a valid response."
        self.msg = _full_msg(self.msg, additionnal_message)

    def warn(subject, additionnal_message=None):
        _warning = InvalidResponseWarning(subject, additionnal_message)
        warnings.warn(_warning.msg, category=InvalidResponseWarning)


class MarketOpenWarning(Warning):
    """This warning is raised when calling the ``yahoo_equity_screener``
    screener while the market is open. This warning is raised because equity
    screener results are sorted according to ``intradaymarketcap``
    (Capitalization for each ticker). Theses values are constantly changing
    when market is open. As a consequence, the screener will miss values and
    duplicate other ones. To avoid such a warning, insure the screener is run
    when the market is closed."""

    def __init__(self, region=None):
        txt = "" if region is None else f"for region {region} "
        self.msg = (
            f"The market {txt} is open. The equity screener is sorted according to "
            f"``intradaymarketcap`` (Capitalization for each ticker). Theses values "
            f"are constantly changing when market is open. As a consequence, the "
            f"screener will miss values and duplicate other ones. To avoid such a "
            f"warning, insure the screener is run when the market is closed."
        )

    def warn(region=None):
        _warning = MarketOpenWarning(region)
        warnings.warn(_warning.msg, category=MarketOpenWarning)


class NoInternetWarning(UserWarning):
    """The internet connection is down."""

    def __init__(self, additionnal_message=None):
        self.msg = "Internet connection seems to be down."
        self.msg = _full_msg(self.msg, additionnal_message)

    def warn(additionnal_message=None):
        _warning = NoInternetWarning(additionnal_message)
        warnings.warn(_warning.msg, category=NoInternetWarning)


class WrongTypeWarning(UserWarning):
    """This warning is raised when a parameter has't the expected type."""

    def __init__(self, param=None, _type=None, additionnal_message=None):
        self.msg = f"Parameter {param}, type={type(param)} must be of type {_type}."
        self.msg = _full_msg(self.msg, additionnal_message)

    def warn(param=None, _type=None, additionnal_message=None):
        _warning = WrongTypeWarning(param, _type, additionnal_message)
        warnings.warn(_warning.msg, category=WrongTypeWarning)
