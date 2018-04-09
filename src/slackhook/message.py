class SlackMessage(object):
    def __init__(self, json_event, debug_channel, adult_channel):
        self.__json_event = json_event
        self.__debug_channel = debug_channel
        self.__adult_channel = adult_channel

    @property
    def user(self):
        return self.__json_event["event"].get("user", None)

    @property
    def text(self):
        return self.__json_event["event"]["text"]

    @property
    def channel(self):
        return self.__json_event["event"]["channel"]

    @property
    def thread(self):
        return self.__json_event["event"].get("thread_ts", None)

    @property
    def is_debug(self):
        return (self.__json_event["event"]["channel"] == self.__debug_channel)

    @property
    def is_adult(self):
        return (self.__json_event["event"]["channel"] == self.__adult_channel)

    @property
    def is_direct(self):
        return (self.__json_event["event"]["channel"].startswith("D") and
                not self.is_debug)
