# -*- coding: utf-8 -*-
import logging

import requests

from .method import find_tea


class SlackTaskHandler(object):
    def handle(self, task):
        task_name = task["name"]

        # 查找下午茶
        if task_name == "tea":
            logging.info(u"執行尋找下午茶任務")
            content = find_tea(task["find_name"])
            # 利用respond_url回傳結果
            requests.post(task["url"], json=content)
            return
