# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2018 by xmz                                           *
# * ********************************************************************* *

__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

###############################################################################
# Import(s)                                                                   #
###############################################################################

import datetime


###############################################################################
# Class                                                                       #
###############################################################################


class JscCommon:
    """
    The class for all misc tools.
    """

    @staticmethod
    def get_timestamp(time=True, seconds=False, microseconds=False, utc=False):
        """
        Get timestamp with predefined format.

        Parameters
        ----------
        time : bool
            Show time with date
        seconds : bool
            Show seconds
        microseconds : bool
            Show microseconds
        utc : bool
            Use UTC format

        Returns
        -------
        string
            Timestamp with required format.

        """

        if utc:
            today_date = datetime.datetime.utcnow()
        else:
            today_date = datetime.datetime.now()
        timestamp = today_date.strftime("%Y-%m-%d")
        if time:
            timestamp += today_date.strftime(" %H:%M")
            if seconds:
                timestamp += today_date.strftime(".%S")
                if microseconds:
                    timestamp += today_date.strftime(".%f")
        return timestamp


###############################################################################
#                                End of file                                  #
###############################################################################
