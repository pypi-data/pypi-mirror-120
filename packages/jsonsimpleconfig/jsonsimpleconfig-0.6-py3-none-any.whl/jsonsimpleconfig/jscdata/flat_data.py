# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2018 by xmz                                           *
# * ********************************************************************* *

__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

###############################################################################
# Import(s)                                                                   #
###############################################################################

from .jsc_section import JscSection


###############################################################################
# Class                                                                       #
###############################################################################


class FlatData:
    """
    The JSC data container.
    """

    GLOBAL_SECTION_NAME = "_"

    def __init__(self):
        self.__section_table = []
        self.__section_item = JscSection()
        self.__flat = {}

    @property
    def data(self):
        return self.__section_table

    def __section_from_json(self, section_data):
        if isinstance(section_data, dict):
            keys = list(section_data.keys())
            if not keys:
                self.__section_item.go_down()
            else:
                self.__iterate_section_data(section_data)

                if len(self.__section_item.data) == 1 and self.__flat:
                    self.__section_table.append(self.__flat)
                    self.__flat = {}

        elif isinstance(section_data, (list, tuple)):
            for index, value in enumerate(section_data):
                self.__section_item.go_up(index)
                self.__section_from_json(value)
                self.__section_item.go_down()

    def __iterate_section_data(self, section_data):
        for key, value in section_data.items():
            if isinstance(value, dict):
                self.__section_item.go_up(FlatData.GLOBAL_SECTION_NAME)
                self.__flat[self.__section_item.str()] = key
                self.__section_from_json(value)
                self.__section_item.go_down()
            else:
                self.__section_item.go_up(key)
                section_name = self.__section_item.str()
                if section_name is None:
                    section_name = FlatData.GLOBAL_SECTION_NAME

                if isinstance(value, (list, tuple)):
                    self.__section_from_json(value)
                else:
                    if section_name not in self.__flat:
                        self.__flat[section_name] = {}
                    self.__flat[section_name] = value

                self.__section_item.go_down()

    def convert_from_json(self, json_data):
        """
        Converts JSC data section from JSON

        Parameters
        ----------
        json_data : dict
            JSON data to convert as dict
        """
        self.__section_from_json(json_data)

    @staticmethod
    def from_json(json_data):
        """
        Get flat data structure from JSON

        Parameters
        ----------
        json_data : dict
            JSON data to convert as dict

        Returns
        -------
        string
            Flat data structure from provided JSON.
        """
        flat_data = FlatData()
        flat_data.convert_from_json(json_data)
        return flat_data


###############################################################################
#                                End of file                                  #
###############################################################################
