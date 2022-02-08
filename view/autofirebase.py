#! /usr/bin/env python
# auto firebase
#
# @file: autofirebase
# @time: 2022/02/08
# @author: Mori
#

from tornado.web import HTTPError
from moreover.handler.json import JsonHandler
from service.autofirebase import AutoFirebaseService


class AutoFirebaseHandler(JsonHandler):
    def get(self, action: str):
        data = {}
        if action == "reading_sheet":
            rows = AutoFirebaseService.read_sheet()
            data.update({"row": rows, "total": len(rows)})

        elif action == "compelete_sheet":
            AutoFirebaseService.trans_and_compelete_sheet()

        else:
            raise HTTPError(400, "unknow action")
        self.render_json(data)
