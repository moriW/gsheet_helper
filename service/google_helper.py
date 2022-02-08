#! /usr/bin/env python
# google service
#
# @file: google
# @time: 2022/02/07
# @author: Mori
#

from typing import Callable

import pygsheets
from moreover.base.config import define, global_config

from google.oauth2 import service_account

define(
    "SCOPES",
    default_value=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/cloud-translation",
    ],
)

define("SERVER_ACCOUNT", default_value=None)


def read_credentials() -> service_account.Credentials:
    cred = service_account.Credentials.from_service_account_info(
        global_config.SERVER_ACCOUNT,
        scopes=global_config.SCOPES,
    )
    return cred


def get_or_create_wks(
    cred: service_account.Credentials,
    sheet_id: str,
    wks_name: str,
    template_name: str = None,
    new_create_callback: Callable = None,
) -> pygsheets.Worksheet:
    pygsheet_client = pygsheets.authorize(custom_credentials=cred)
    sheet = pygsheet_client.open_by_key(sheet_id)
    try:
        return sheet.worksheet_by_title(wks_name)
    except pygsheets.WorksheetNotFound:
        if template_name:
            worksheet_id = sheet.worksheet_by_title(template_name).id
            wks = sheet.add_worksheet(wks_name, src_tuple=(sheet_id, worksheet_id))
            if new_create_callback:
                new_create_callback(wks)
            return wks
        else:
            return None
