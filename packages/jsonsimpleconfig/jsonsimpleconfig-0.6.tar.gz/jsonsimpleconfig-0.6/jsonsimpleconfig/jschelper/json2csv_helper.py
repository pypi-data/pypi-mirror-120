# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2021 by xmz                                           *
# * ********************************************************************* *

__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

###############################################################################
# Import(s)                                                                   #
###############################################################################

import logging

import pandas

from jsonsimpleconfig import Json, FlatData


###############################################################################
# Class                                                                       #
###############################################################################


class Json2CsvHelper:
    @staticmethod
    def convert(json_file, csv_file):

        json_parser = Json(json_file)
        json_data = json_parser.parse()

        if json_data["data"] is not None:
            if isinstance(json_data["data"], dict):
                logging.info("JSON file is correct. Generating CSV ...")
                logging.info("CSV location: %s", csv_file)
                flat_data = FlatData.from_json(json_data["data"])
                pandas_data = pandas.json_normalize(flat_data.data)
                pandas_data.to_csv(csv_file, sep=";", index=False, encoding="utf-8")
            else:
                logging.error("JSON data without root name cannot be converted into CSV.")

        else:
            logging.error("Incorrect JSON or file is empty.")
            if json_data["status"] is not None:
                logging.debug(json_data["status"])


###############################################################################
#                                End of file                                  #
###############################################################################
