# -*- coding: utf-8 -*-
import logging

import settings

from flask import Flask, request, jsonify, abort
from slackclient import SlackClient

from slackhook import SlackCommand, SlackEvent, SlackMessage
from slackhandler import (
    SlackMessageHandler, SlackCommandHandler, SlackTaskHandler
)

app = Flask(__name__)


# 執行器設定
slack_client = SlackClient(settings.BOT_TOKEN)
message_handler = SlackMessageHandler(slack_client)
command_handler = SlackCommandHandler()
task_handler = SlackTaskHandler()


# 接收event訊息
@app.route("/slack/event", methods=["POST"])
def slack_event():
    data = request.get_json()
    event = SlackEvent(data)

    # 驗證token
    if not event.check_token(settings.HOOK_TOKEN):
        logging.error(u"接收的token不正確")
        abort(401)

    # event類型是chanllenge
    if event.type == "challenge":
        return jsonify({"challenge": event.chanllenge})

    # event類型是message
    elif event.type == "message":
        message = SlackMessage(
            data, settings.DEBUG_CHANNEL, settings.ADULT_CHANNEL
        )
        logging.info(
            u"收到訊息: <{}> [{}]: {}".format(
                message.channel, message.user, message.text
            )
        )
        message_handler.handle(message)
    return jsonify({})


# 接收command訊息
@app.route("/slack/command", methods=["POST"])
def slack_command():
    data = request.form.to_dict()
    command = SlackCommand(data)

    # 驗證token
    if not command.check_token(settings.HOOK_TOKEN):
        logging.error(u"接收的token不正確")
        abort(401)

    # 運行command
    logging.info(u"收到指令 [{}]: {}".format(command.cmd, command.text))
    response = command_handler.handle(command)
    return response


# 接收task任務
@app.route("/slack/task", methods=["POST"])
def slack_task():
    task = request.form.to_dict()
    """
    task架構
    {
        name: "task_name"
        arg: {dict}
    }
    """

    logging.info(u"收到任務: {}".format(task["name"]))
    task_handler.handle(task)
    return jsonify({})


# 伺服器錯誤
@app.errorhandler(500)
def server_error(e):
    logging.exception(u"遇到不知名的錯誤")
    return "An internal error occurred.", 500
