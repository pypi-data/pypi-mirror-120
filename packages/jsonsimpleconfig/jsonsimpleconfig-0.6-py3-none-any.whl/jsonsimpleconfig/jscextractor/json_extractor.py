# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2018 by xmz                                           *
# * ********************************************************************* *

__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

###############################################################################
# Import(s)                                                                   #
###############################################################################

import json
import logging

from jsonsimpleconfig import JscData, JscSection


###############################################################################
# Class                                                                       #
###############################################################################


class JsonExtractor:
    def __init__(self, jsc_data, options=None):
        self.__jsc_data = jsc_data
        self.__json_data = {}
        self.__file = None
        self.__version = "1.0"

    def get_version(self):
        return self.__version

    def get_json(self):
        return self.__json_data

    def __extract_section_to_json(self, section_name):
        branches = section_name.split(JscSection.SECTION_GLUE)
        json_data = self.__json_data
        if isinstance(branches, (list, tuple)):
            for branch in branches:
                branch = branch.strip().strip('"')
                if branch != JscSection.GLOBAL_SECTION_NAME:
                    if branch not in json_data:
                        json_data[branch] = {}
                    json_data = json_data[branch]
        section = self.__jsc_data.get_section(section_name)
        if isinstance(section, dict):
            for item_key, item_value in section.items():
                json_data[item_key] = item_value

    def extract_data_to_json(self):
        if JscSection.GLOBAL_SECTION_NAME in self.__jsc_data.get_section_names():
            self.__extract_section_to_json(JscSection.GLOBAL_SECTION_NAME)
        for section_name in self.__jsc_data.get_section_names():
            if section_name != JscSection.GLOBAL_SECTION_NAME:
                self.__extract_section_to_json(section_name)

    def extract_to_file(self, file_path):
        if self.__jsc_data is not None and isinstance(self.__jsc_data, JscData):
            self.extract_data_to_json()
            try:
                json_string = json.dumps(self.__json_data, ensure_ascii=False, indent=4)
                if json_string is not None:
                    with open(file_path, "w", encoding="utf-8") as self.__file:
                        self.__file.write(json_string)

            except json.JSONDecodeError as error:
                logging.debug(error)


###############################################################################
#                                End of file                                  #
###############################################################################
