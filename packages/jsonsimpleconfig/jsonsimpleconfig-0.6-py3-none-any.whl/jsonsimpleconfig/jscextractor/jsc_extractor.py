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
import os

from jsonsimpleconfig import JscData, JscSection, JscCommon
from .jsc_header import JscHeader


###############################################################################
# Class                                                                       #
###############################################################################


class JscExtractor:
    def __init__(self, jsc_data, options=None):
        self.__jsc_data = jsc_data
        self.__file = None
        self.__version = "1.0"

    def get_version(self):
        return self.__version

    def __extract_section_to_file(self, section_name):
        section = self.__jsc_data.get_section(section_name)
        if self.__file and isinstance(section, dict):
            for item_key, item_value in section.items():
                self.__file.write(json.dumps({item_key: item_value}).strip().lstrip("{").rstrip("}") + os.linesep)
            self.__file.write(os.linesep)

    def __extract_data_to_file(self):
        if JscSection.GLOBAL_SECTION_NAME in self.__jsc_data.get_section_names():
            self.__extract_section_to_file(JscSection.GLOBAL_SECTION_NAME)
        for section_name in self.__jsc_data.get_section_names():
            if self.__file and section_name != JscSection.GLOBAL_SECTION_NAME:
                self.__file.write("[" + section_name + "]" + os.linesep)
                self.__extract_section_to_file(section_name)

    def extract_to_file(self, file_path):
        if self.__jsc_data is not None and isinstance(self.__jsc_data, JscData):
            with open(file_path, "w", encoding="utf-8") as self.__file:
                jsc_header = JscHeader(
                    {
                        "defaultHeader": True,
                        "allowCustomHeader": True,
                        "customHeaderFilePath": "/etc/jsonsimpleconfig/header.template",
                        "headerTemplateData": {
                            "JscExtractor_version": self.__version,
                            "Jsc_timestamp": JscCommon.get_timestamp(),
                        },
                    }
                ).str()
                if jsc_header is not None:
                    self.__file.write(jsc_header)
                self.__extract_data_to_file()


###############################################################################
#                                End of file                                  #
###############################################################################
