#! /usr/bin/env python
# gsheet_service
# web entry
#
# @file: web
# @time: 2022/2/5
# @author: Mori
#


import tornado.web
import tornado.ioloop
import tornado.httpserver
from view.router import HANDLERS
from moreover.base.config import define, parse_config_file, global_config
from moreover.base.logger import debug_log

define("HOST", default_value="0.0.0.0")
define("PORT", default_value=8888)
define("DEBUG", default_value=True)

if global_config.DEBUG:
    debug_log()

MAIN_APP = tornado.web.Application(
    handlers=HANDLERS,
    default_host=global_config.HOST,
    gzip=True,
    debug=global_config.DEBUG,
)

if __name__ == "__main__":
    parse_config_file("config.json")
    ioloop = tornado.ioloop.IOLoop.current()
    http_server = tornado.httpserver.HTTPServer(MAIN_APP)
    http_server.listen(global_config.PORT)
    ioloop.start()
