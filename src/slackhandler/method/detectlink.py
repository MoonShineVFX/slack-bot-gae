# -*- coding: utf-8 -*-
import logging
import re


def detect_link(text):
    # 設定搜尋pattern
    link_pattern = r'\b[a-zA-Z]:[\\|/][^\n|"]+'
    link_result = re.findall(link_pattern, text)

    if len(link_result) > 0:
        # 開始篩選連結
        logging.info(u"找到疑似連結")
        actions = []
        for idx, link in enumerate(link_result):
            # 過濾中文
            try:
                link.decode("ascii")
            except Exception:
                continue

            # 過濾空白連結
            if link.find(" ") != -1:
                continue

            # 過濾按鈕數量上限
            if idx > 4:
                break

            # 按鈕文字縮減
            if len(link) <= 30:
                button_text = link
            else:
                button_text = link[0:12] + "..." + link[-14:len(link)]

            # 產生按鈕
            link = link.replace("\\", "/")
            button = {
                "type": "button",
                "text": button_text,
                "url": "file://" + link
            }
            actions.append(button)

        if len(actions) != 0:
            logging.info(u"產生連結按鈕")
            attachments = [{
                "fallback": "Detected link button",
                "actions": actions,
                "footer": u"在按鈕上按右鍵打開連結/檔案"
            }]

            return attachments
        else:
            logging.info(u"連結無效")
            return None
    else:
        return None
