# -*- coding: utf-8 -*-
import logging

from ndbmodel import (
    faces, mslife, beauty_images, Dcard, Reddit
)

from .method import detect_link, draw_attachment


class SlackMessageHandler(object):
    def __init__(self, client):
        self.client = client

    def handle(self, message):
        # 刪除訊息
        if message.thread and message.text == "del":
            logging.info(u"嘗試刪除訊息: {}".format(message.thread))
            self.client.api_call(
                "chat.delete",
                channel=message.channel,
                ts=message.thread
            )

        # 過濾訊息
        if message.thread or message.is_direct:
            return

        # 處理訊息
        # 抽公司生活照片
        if message.text == u"夢想":
            attachments = draw_attachment(mslife)
            self.client.api_call(
                "chat.postMessage",
                channel=message.channel,
                attachments=attachments
            )

        # 在一般頻道抽同事照片 或者 抽表特版圖片
        elif message.text == u"抽":
            if (message.is_adult or message.is_debug):
                attachments = draw_attachment(beauty_images, boob=False)
                self.client.api_call(
                    "chat.postMessage",
                    channel=message.channel,
                    attachments=attachments
                )
            else:
                attachments = draw_attachment(faces)
                self.client.api_call(
                    "chat.postMessage",
                    channel=message.channel,
                    attachments=attachments
                )

        # 抽奶特圖片
        elif message.text == u"奶" and (message.is_adult or message.is_debug):
            attachments = draw_attachment(beauty_images, boob=True)
            self.client.api_call(
                "chat.postMessage",
                channel=message.channel,
                attachments=attachments
            )

        # 抽Reddit圖片
        elif message.text == u"老外" and (message.is_adult or message.is_debug):
            attachments = draw_attachment(Reddit)
            self.client.api_call(
                "chat.postMessage",
                channel=message.channel,
                attachments=attachments
            )

        # 抽Dcard連結
        elif message.text == u"卡" and (message.is_adult or message.is_debug):
            attachments = draw_attachment(Dcard)
            self.client.api_call(
                "chat.postMessage",
                channel=message.channel,
                attachments=attachments
            )

        # 偵測文章是否含有連結並且產生按鈕
        else:
            attachments = detect_link(message.text)
            if attachments:
                self.client.api_call(
                    "chat.postMessage",
                    channel=message.channel,
                    attachments=attachments
                )
