# -*- coding: utf-8 -*-
from ndbmodel import draw_entity


def draw_attachment(model, boob=None):
    # 抽出實體
    entity = draw_entity(model, boob)

    model_type = model.__name__

    # 如果是Dcard，返回連結訊息
    if model_type == "Dcard":
        attachments = [{
            "fallback": "Dcard Post.",
            "title": u"{} - Dcard".format(entity.title),
            "title_link": entity.url,
            "image_url": entity.images[0].url
        }]
    else:
        attachments = [{
            "fallback": "Draw Image",
            "image_url": entity.image_url
        }]

        # 如果是表特圖，附加推文資訊
        if model_type == "beauty_images":
            post = entity.key.parent().get()
            rank = post.rank
            if rank == 100:
                attachments[0]["title"] = "爆"
                attachments[0]["color"] = "#ff0000"
            else:
                attachments[0]["author_name"] = "{}推".format(post.rank)

    return attachments
