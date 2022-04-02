#! /usr/bin/env python
# bookkeeping
#
# @file: bookkeeping
# @time: 2022/02/07
# @author: Mori
#

import schema
import datetime
from typing import List
from tornado.ioloop import IOLoop
from tornado.web import HTTPError
from moreover.handler.json import JsonHandler
from service.bookkeeping import BookkeepingService


payload_schema = schema.Schema(
    {
        "date": schema.Use(
            lambda x: datetime.datetime.strptime(x, "%d/%m/%Y"), error="date_error"
        ),
        "go_to_type": schema.Schema(
            lambda x: x
            in [
                "房屋水电",
                "通讯",
                "交通",
                "游戏娱乐",
                "旅游娱乐",
                "衣",
                "蔬菜食品",
                "零食",
                "日用品",
                "化妆品",
                "人际交往",
                "医疗",
                "学习",
                "影音娱乐",
                "水果",
                "工资",
                "奖金",
                "生产力/工具",
            ],
            error="type_error",
        ),
        "content": schema.Schema(lambda x: len(x) > 0, error="content_error"),
        "price": schema.Use(float, error="price_error"),
        "pay_or_gain": schema.Schema(
            lambda x: x in ["收入", "支出"], error="pay_or_gain_error"
        ),
        "ext": schema.Schema(lambda x: len(x) >= 0, error="ext_error"),
    },
)


class BookkeepingHandler(JsonHandler):
    @property
    def parsed_payload(self) -> List:
        try:
            data = payload_schema.validate(self.data)
            return [
                data["date"].date().isoformat(),
                data["go_to_type"],
                data["content"],
                data["price"],
                data["pay_or_gain"],
                data["ext"],
            ]
        except Exception as e:
            raise HTTPError(400, reason=str(e))

    def post(self):
        who = self.request.headers.get("who", None)
        if who not in ["jae", "mori"]:
            raise HTTPError(400, log_message="unknow user")
        IOLoop.current().call_later(
            delay=0,
            callback=BookkeepingService.append_row,
            who=who,
            row=self.parsed_payload,
        )
        # BookkeepingService.append_row(who=who, row=self.parsed_payload)
        return self.render_json({})
