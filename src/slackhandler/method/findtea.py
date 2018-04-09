# -*- coding: utf-8 -*-
import logging

import re
from dateutil import tz
import gspread
from datetime import datetime

from ndbmodel import TeaMenu, TeaMenuItems

import settings


# 取得符合試算表標題的日期
def get_date():
    utc_zone = tz.tzutc()
    local_zone = tz.gettz("Asia/Taipei")

    now = datetime.utcnow().replace(tzinfo=utc_zone)
    now = now.astimezone(local_zone)

    return int(now.strftime("%Y%m%d"))


# 取得下午茶品項跟細部選項
def get_menu(sheet):
    # 取得品項跟細項的欄數
    name_list = sheet.row_values(4)

    # 將每行的選項填滿
    menu_list = []
    for idx, name in enumerate(name_list):
        if name == "" or name[0].isdigit():
            continue

        value_list = []
        last_value = ""
        for col_idx, value in enumerate(sheet.col_values(idx + 1)):
            if value != "":
                last_value = value
            else:
                value = last_value
            value_list.append(value)

            if col_idx > 100:
                break

        menu_list.append((name, value_list))

    # 改成資料庫的格式
    names = []
    content = []

    for name, values in menu_list:
        names.append(name)
        content.append(values)

    return names, content


def find_tea(name):
    logging.debug(u"開始查找下午茶")

    google_client = gspread.authorize(settings.GOOGLE_AUTH)
    spreadsheet = google_client.open_by_key(settings.SHEET_KEY)
    sheet_list = spreadsheet.worksheets()

    # Get Current Sheet
    sheet = sheet_list[0]
    cur = get_date()
    for sht in sheet_list:
        if sht.title.isdigit():
            title = int(sht.title)
            if title == cur:
                sheet = sht
                break
            elif title < cur:
                break
        sheet = sht

    # Find Menu
    menu = TeaMenu.get_by_id(sheet.title)
    if menu is None:
        # 找不到實體，於是新建一個並放入資料庫
        names, content = get_menu(sheet)
        item_list = []
        for con in content:
            item_list.append(TeaMenuItems(content=con))

        menu = TeaMenu(
            id=sheet.title,
            names=names,
            title=content[0][0],
            items=item_list
        )

        menu.put()

    # Search Name
    search_word = re.compile(".*?" + name + ".*?", flags=re.IGNORECASE)
    cell_find_result = sheet.findall(search_word)
    cell_list = []

    for cell in cell_find_result:
        logging.debug(u"找到座標 {}, {}".format(cell.row, cell.col))
        if cell.row < 100:
            cell_list.append(cell.row)

    title = ""
    subtitle = ""
    for cell in cell_list:
        names_count = len(menu.names)
        for idx in range(names_count):
            if idx == 0:
                title += menu.items[idx].content[cell] + "\n"
                continue

            subtitle += menu.names[idx] + ": "
            subtitle += menu.items[idx].content[cell]
            if idx == names_count - 1:
                subtitle += "      "
            else:
                subtitle += "  /  "

    # send response
    if title != "":
        content = {
            "response_type": "ephemeral",
            "attachments": [{
                "fallback": u"{} 點了\n{}".format(name, title),
                "color": "good",
                "author_name": u"{} 點了".format(name),
                "title": title,
                "title_link": settings.SHEET_URL,
                "fields": [{
                    "title": subtitle
                }],
                "footer": menu.title.split(u"：")[-1].strip()
            }]
        }
    else:
        content = {
            "response_type": "ephemeral",
            "text": u"{}沒有點東西!".format(name)
        }
    logging.info(u"搜尋完成")

    return content