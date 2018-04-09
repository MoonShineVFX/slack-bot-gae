class SlackCommand(object):
    def __init__(self, json):
        self.__json = json

    @property
    def cmd(self):
        return self.__json["command"]

    @property
    def text(self):
        return self.__json["text"]

    @property
    def url(self):
        return self.__json["response_url"]

    def check_token(self, token):
        if "token" not in self.__json:
            return False
        elif self.__json["token"] != token:
            return False
        return True
