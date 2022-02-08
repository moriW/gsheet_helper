#! /usr/bin/env python
# read from gsheet
#
# @file: gsheet
# @time: 2022/02/07
# @author: Mori
#

import datetime
from typing import Dict, List

import pygsheets
from moreover.base.config import define, global_config

from .google_helper import get_or_create_wks, read_credentials

define(
    "BOOKKEEPING_SHEET_ID", default_value="17Xe7CNIJ3I-f3giRh8ZazuJOoGqMns3WcQjkjqNoxZs"
)
define("BOOKKEEPING_TEMPLATE_NAME", default_value="template")


class BookkeepingService:
    @classmethod
    def wks_set_format(cls, wks: pygsheets.Worksheet):
        first_cell = wks.cell("A14")
        first_cell.set_number_format(pygsheets.FormatType.NUMBER, pattern="YYYY/mm/dd")
        pygsheets.DataRange("A14", "A200", wks).apply_format(first_cell)

    @classmethod
    def append_row(cls, who: str, row: List[Dict]):
        cred = read_credentials()
        wks_name = who + "-" + datetime.datetime.now().strftime("%Y/%m")
        wks = get_or_create_wks(
            cred=cred,
            sheet_id=global_config.BOOKKEEPING_SHEET_ID,
            wks_name=wks_name,
            template_name=global_config.BOOKKEEPING_TEMPLATE_NAME,
            new_create_callback=cls.wks_set_format,
        )
        all_values = wks.get_all_values(
            returnas="cell",
            include_tailing_empty=False,
            include_tailing_empty_rows=False,
        )
        last_row = 0
        for _row in filter(
            lambda x: len(x) > 0 and len(x[0].value.strip()) != 0, all_values
        ):
            last_row = max(last_row, _row[0].row)
        # print(last_row, row)
        wks.append_table(values=row, start=f"A{last_row}")
