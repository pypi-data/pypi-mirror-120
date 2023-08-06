"""
JSON Simple Config

The simple idea to prepare and manage configuration for your application.
"""

# * ********************************************************************* *
# *   Copyright (C) 2020 by xmz                                           *
# * ********************************************************************* *

###############################################################################
# Import(s)                                                                   #
###############################################################################

from jsonsimpleconfig.jsccommon import JscComments, JscCommon
from jsonsimpleconfig.jscdata import JscData, JscSection, FlatData
from jsonsimpleconfig.jscparser import Json, JscParser
from jsonsimpleconfig.jscextractor import JscExtractor, JscHeader, JsonExtractor
from jsonsimpleconfig.jschelper import (
    Jsc,
    Json2JscHelper,
    Json2CsvHelper,
    Jsc2JsonHelper,
    JscConfig,
    JscConfigManaged as JscDataFromFile,
)


###############################################################################
# Module                                                                      #
###############################################################################


def load(jsc_file, refresh=False):
    """
    load
    :param jsc_file:
    :param refresh:
    :return:
    """
    return Jsc.get(jsc_file, refresh)


def loads(jsc_string):
    """
    loads
    :param jsc_string:
    :return:

    >>> import jsonsimpleconfig
    >>> jsonsimpleconfig.loads('"variable_root":"value_root"') # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    <jsonsimpleconfig.jscdata.jsc_data.JscData object at 0x...
    >>> jsonsimpleconfig.loads('"variable_root":"value_root"').print()
    <BLANKLINE>
    * Section (Global):
    *** [variable_root] : [value_root]
    <BLANKLINE>
    """
    return Jsc.gets(jsc_string)


def load_json(json_file):
    """
    load_json
    :param json_file:
    :return:

    >>> import jsonsimpleconfig
    >>> root = jsonsimpleconfig.loads('"variable_root":"value_root"')
    >>> json_extractor = jsonsimpleconfig.JsonExtractor(root)
    >>> json_extractor.extract_data_to_json()
    >>> root_json = json_extractor.get_json()
    >>> print(root_json)
    {'variable_root': 'value_root'}
    """
    return Json.parse_file_json(json_file)


def loads_json(json_string):
    """
    loads_json
    :param json_string:
    :return:
    """
    return Json.parse_string_json(json_string)


__all__ = (
    "JscCommon",
    "JscComments",
    "Json2JscHelper",
    "Json2CsvHelper",
    "Jsc2JsonHelper",
    "Json",
    "JscParser",
    "JscData",
    "FlatData",
    "JscSection",
    "JscExtractor",
    "JscExtractor",
    "JscHeader",
    "JsonExtractor",
    "JscDataFromFile",
    "JscConfig",
    "Jsc",
)

###############################################################################
#                                End of file                                  #
###############################################################################
