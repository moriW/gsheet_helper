#! /usr/bin/env python
# auto firebase
#
# @file: autofirebase
# @time: 2022/02/08
# @author: Mori
#
import datetime

from typing import List, Dict
from itertools import chain
from google.cloud import translate_v2
from .google_helper import read_credentials, get_or_create_wks
from moreover.base.config import define, global_config
from moreover.base.logger import gen_logger

define(
    "FIREBASE_SHEET_ID", default_value="1vXqHdA6RTD9cMMv8CvRQMW-jM9GSajAZOVcdJMwEFDM"
)
define("FIREBASE_WORKSHEET_NAME", default_value="lite填色通知配置记录")

IS_CONFIG_KEY = "已配置"
PUSHDATE_KEY = "发布日期"
PUSHTIME_KEY = "发布时间"
PUSH_TIMEZONE_KEY = "发布时区"
TITLE_KEY = "标题"
DESC_KEY = "描述"
NAME_KEY = "名称"
PIC_KEY = "配图链接"
CATE_KEY = "配图"
I18NS = ["de", "es", "fr", "pt", "ru"]
I18N_MAP = {
    "de": ["German"],
    "es": ["Spanish"],
    "fr": ["French"],
    "pt": ["Portuguese"],
    "ru": ["Russian"],
}

ALPHA_ASIC_START = 64
DATETIME_FMT = "%Y/%m/%d"


LOGGER = gen_logger("AutoFirebaseService")


class AutoFirebaseService:
    @classmethod
    def trans_and_compelete_sheet(cls):
        cred = read_credentials()
        wks = get_or_create_wks(
            cred=cred,
            sheet_id=global_config.FIREBASE_SHEET_ID,
            wks_name=global_config.FIREBASE_WORKSHEET_NAME,
        )

        header = wks.get_row(1, returnas="cell", include_tailing_empty=False)
        first_i18n_index = [
            x.col for x in header if "title" in x.value or "desc" in x.value
        ][0] - 1
        payload = wks.get_all_records()

        now = datetime.datetime.now()
        translate_client = translate_v2.Client(credentials=cred)
        for index, line_dict in enumerate(payload):
            try:
                pushdate = datetime.datetime.strptime(
                    line_dict[PUSHDATE_KEY], DATETIME_FMT
                )
                assert pushdate > now
            except Exception:
                continue

            if line_dict[IS_CONFIG_KEY] == "是":
                continue

            if (
                len(line_dict[TITLE_KEY].strip()) == 0
                or len(line_dict[DESC_KEY].strip()) == 0
            ):
                continue

            if (
                len(
                    [v for k, v in line_dict.items() if "title" in k and v == ""]
                    + [v for k, v in line_dict.items() if "desc" in k and v == ""]
                )
                == 0
            ):
                continue

            title, desc = line_dict[TITLE_KEY], line_dict[DESC_KEY]
            update_values = (
                ["否"] +
                [
                    translate_client.translate(
                        values=title, source_language="en", target_language=lan
                    )["translatedText"]
                    for lan in I18NS
                ]
                + [
                    translate_client.translate(
                        values=desc, source_language="en", target_language=lan
                    )["translatedText"]
                    for lan in I18NS
                ]
            )
            update_values = [x.replace("C&#39;est l&#39;", "") for x in update_values]
            update_values = [x.replace("&#39;", "") for x in update_values]
            update_values = [x.replace("&amp;", "") for x in update_values]
            wks.update_row(index + 2, values=update_values, col_offset=first_i18n_index - 1)
            LOGGER.info(f"{index + 2}, {update_values}")

    @classmethod
    def parse_line_dict(cls, line_dict: Dict) -> List[Dict]:
        push_date = datetime.datetime.strptime(line_dict[PUSHDATE_KEY], "%Y/%m/%d")
        hour, minute = list(line_dict[PUSHTIME_KEY].split(":"))
        pic_url = line_dict[PIC_KEY]
        cate_name = line_dict[CATE_KEY]
        return_date = {
            "year": push_date.strftime("%Y"),
            "month": {"str": push_date.strftime("%b").upper(), "int": push_date.month},
            "day": str(push_date.day),
        }
        return_time = {
            "hour": hour,
            "minute": minute,
        }
        name_prefix = f"{push_date.month}-{push_date.day}" + " / " + cate_name
        return [
            {
                "push_date": return_date,
                "push_time": return_time,
                "title": line_dict[TITLE_KEY],
                "desc": line_dict[DESC_KEY],
                "lan": {
                    "operation": "not in",
                    "lan_list": list(chain(*I18N_MAP.values())),
                },
                "pic": pic_url,
                "name": name_prefix + " / en",
            }
        ] + [
            {
                "push_date": return_date,
                "push_time": return_time,
                "title": line_dict[f"{i18n_item}_title"],
                "desc": line_dict[f"{i18n_item}_desc"],
                "lan": {
                    "operation": "in",
                    "lan_list": I18N_MAP[i18n_item],
                },
                "pic": pic_url,
                "name": name_prefix + " / " + i18n_item,
            }
            for i18n_item in I18NS
        ]

    @classmethod
    def read_sheet(cls):
        cred = read_credentials()
        wks = get_or_create_wks(
            cred=cred,
            sheet_id=global_config.FIREBASE_SHEET_ID,
            wks_name=global_config.FIREBASE_WORKSHEET_NAME,
        )
        now = datetime.datetime.now()

        paresed_lines = []
        for line_dict in wks.get_all_records():
            try:
                pushdate = datetime.datetime.strptime(
                    line_dict[PUSHDATE_KEY], DATETIME_FMT
                )
                assert pushdate > now
            except Exception:
                continue
            if line_dict[IS_CONFIG_KEY] in ["是", ""]:
                continue
            if (
                len(
                    [v for k, v in line_dict.items() if "title" in k and v == ""]
                    + [v for k, v in line_dict.items() if "desc" in k and v == ""]
                )
                != 0
            ):
                continue
            paresed_lines.extend(cls.parse_line_dict(line_dict))
        return paresed_lines


if __name__ == "__main__":
    from moreover.base.config import parse_config_file

    parse_config_file("config.json")
    print(AutoFirebaseService.trans_and_compelete_sheet())
    # print(AutoFirebaseService.read_sheet())
