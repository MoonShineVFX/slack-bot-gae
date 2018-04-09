# -*- coding: utf-8 -*-
import logging

from flask import jsonify
from google.appengine.api import taskqueue

import settings


class SlackCommandHandler(object):
    def handle(self, command):
        # 顯示公司資訊地址
        if command.cmd == "/info":
            logging.info(u"顯示公司資訊")
            content = {
                "response_type": "in_channel",
                "attachments": [settings.INFO]
            }
            return jsonify(content)

        # 顯示公司WIFI密碼
        if command.cmd == "/wifi":
            logging.info(u"顯示wifi密碼")
            content = {
                "response_type": "in_channel",
                "attachments": [settings.WIFI]
            }
            return jsonify(content)

        # 查找公司的下午茶
        if command.cmd == "/tea":
            logging.info(u"尋找下午茶")
            string = u"我找一下..."
            if len(command.text) == "":
                string = u"沒輸入名稱喔！"
            else:
                # 增加查找下午茶的task
                taskqueue.add(
                    url="/slack/task",
                    params={
                        "name": "tea",
                        "url": command.url,
                        "find_name": command.text
                    }
                )

            content = {
                "text": string
            }

            logging.debug(u"回傳正在尋找訊息")
            return jsonify(content)
