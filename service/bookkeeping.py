#! /usr/bin/env python
# read from gsheet
#
# @file: gsheet
# @time: 2022/02/07
# @author: Mori
#

import csv
import datetime
from dateutil.relativedelta import relativedelta
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
    def get_wks_name(
        cls, who: str, target_date: datetime.datetime = datetime.datetime.now()
    ):
        return who + "-" + target_date.strftime("%Y/%m")

    @classmethod
    def wks_set_format(cls, wks: pygsheets.Worksheet):
        first_cell = wks.cell("A14")
        first_cell.set_number_format(pygsheets.FormatType.NUMBER, pattern="YYYY/mm/dd")
        pygsheets.DataRange("A14", "A200", wks).apply_format(first_cell)

    @classmethod
    def append_row(cls, who: str, row: List[Dict]):
        cred = read_credentials()
        wks_name = cls.get_wks_name(who)
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

        wks.append_table(values=row, start=f"A{last_row}")

    @classmethod
    def parse_ali_csv(cls, csv_data: List) -> List:
        data = []
        csv_reader = csv.reader(csv_data[2:])
        for line in csv_reader:
            if len(line) == 1:
                break
            if line[0].strip() != "支出":
                line[0] = "收入"
            data.append(
                [
                    line[-2][:10],
                    line[7].strip(),
                    line[3].strip(),
                    float(line[5].strip()),
                    line[0].strip(),
                    line[1].strip(),
                ]
            )
        return data

    @classmethod
    def parse_wechat_csv(cls, csv_data: List) -> List:
        data = []
        csv_reader = csv.reader(csv_data)
        for line in csv_reader:
            if (
                len(list(filter(lambda x: len(x.strip()), line))) <= 1
                or line[0] == "交易时间"
            ):
                continue

            line[5] = line[5][1:]

            if line[4].strip() != "支出":
                line[4] = "收入"

            data.append(
                [
                    line[0][:10].strip(),
                    line[1].strip(),
                    line[2].strip(),
                    float(line[5].strip()),
                    line[4],
                    line[3],
                ]
            )
        return data

    @classmethod
    def csv_diff(
        cls,
        current_csv: List,
        from_csv: List,
    ) -> List:
        lines = []
        for from_line in from_csv:
            is_exists = False
            for current_line in current_csv:
                same_count = 0
                for x, y in zip(current_line, from_line):
                    same_count += x == y
                if same_count >= 3:
                    is_exists = True
            if not is_exists:
                lines.append(from_line)
        return lines

    @classmethod
    def sync_csv_to_wks(
        cls,
        who: str,
        csv_data: List,
        csv_from: str,
        target_date: datetime.datetime = datetime.datetime.now(),
    ):
        cred = read_credentials()
        wks_name = cls.get_wks_name(who, target_date=target_date)
        wks = get_or_create_wks(
            cred=cred,
            sheet_id=global_config.BOOKKEEPING_SHEET_ID,
            wks_name=wks_name,
            template_name=global_config.BOOKKEEPING_TEMPLATE_NAME,
            new_create_callback=cls.wks_set_format,
        )

        if csv_from == "ali":
            datas = cls.parse_ali_csv(csv_data)
        else:
            datas = cls.parse_wechat_csv(csv_data)

        min_date = datetime.datetime(
            year=target_date.year, month=target_date.month, day=1
        )
        max_date = min_date + relativedelta(months=1)

        datas = [
            item
            for item in datas
            if max_date > datetime.datetime.strptime(item[0], "%Y-%m-%d") >= min_date
        ]

        all_values = wks.get_all_values(
            returnas="cell",
            include_tailing_empty=False,
            include_tailing_empty_rows=False,
        )

        current_datas, last_row = [], 0
        for row in all_values[14:]:
            if len(row) < 6:
                break
            a_row = [item.value for item in row]
            current_datas.append(a_row)
            last_row = max(last_row, row[0].row)

        append_lines = cls.csv_diff(current_datas, datas)
        if len(append_lines) > 1:
            wks.append_table(append_lines, f"A{last_row}")
