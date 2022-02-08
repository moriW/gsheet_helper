#! /usr/bin/env python
# gsheet_service
# router entry
#
# @file: web
# @time: 2022/2/5
# @author: Mori
#

from tornado.web import RequestHandler
from .bookkeeping import BookkeepingHandler
from .autofirebase import AutoFirebaseHandler


class HealthHandler(RequestHandler):
    async def get(self):
        self.write("health")
        await self.flush()


HANDLERS = [
    (r"/_health", HealthHandler),
    (r"/bookkeeping", BookkeepingHandler),
    (r"/autofirebase/(reading_sheet|compelete_sheet)", AutoFirebaseHandler),
]

__all__ = ["HANDLERS"]
