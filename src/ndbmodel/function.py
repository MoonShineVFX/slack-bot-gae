# -*- coding: utf-8 -*-
import logging
import random


def draw_entity(model, boob=None):
    logging.info(u"抽取實體 {}".format(model.__name__))

    # Query初始化 跟 如果是表特的話看是不是奶特
    if boob is not None:
        query_init = model.query(model.boob == boob)
    else:
        query_init = model.query()

    # 找到資料庫最低的count數值
    query_min = query_init.order(model.count)
    entity_min = query_min.fetch(1, projection=[model.count])[0]
    min_count = entity_min.count

    query_count = query_init.filter(model.count == min_count)

    # 隨機取出實體
    rand_num = int(random.random() * 10000000)
    if random.random() > 0.5:
        query_rand = query_count.filter(model.rand >= rand_num)
    else:
        query_rand = query_count.filter(model.rand < rand_num)

    result = list(query_rand.fetch(1))

    # 如果隨機取出實體是空的，取第一個match的
    if len(result) != 0:
        logging.debug(u"成功取得實體")
        entity = result[0]
    else:
        logging.debug(u"隨機實體是空的，以優先符合實體取代")
        entity = query_count.fetch(1)[0]

    entity.count += 1
    entity.put()

    entity_id = entity.key.id()
    if isinstance(entity_id, basestring):
        entity_id = unicode(entity_id, "utf-8")

    logging.info(
        u"抽取結果: {}, {}".format(
            entity.key.kind(),
            entity_id
        )
    )

    return entity
