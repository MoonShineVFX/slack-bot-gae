class SlackEvent(object):
    def __init__(self, json):
        self.__json = json

    @property
    def type(self):
        if "challenge" in self.__json["event"]:
            return "challenge"
        elif ("bot_id" not in self.__json["event"] and
                self.__json["event"]["type"] == "message"):
            return "message"
        return None

    @property
    def challenge(self):
        return self.__json.get("challenge", None)

    def check_token(self, token):
        if "token" not in self.__json:
            return False
        elif self.__json["token"] != token:
            return False
        return True
