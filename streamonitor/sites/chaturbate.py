import requests
from streamonitor.bot import Bot


class Chaturbate(Bot):
    site = 'Chaturbate'
    siteslug = 'CB'

    def __init__(self, username):
        super().__init__(username)
        self.sleep_on_offline = 30
        self.sleep_on_error = 60

    def getVideoUrl(self):
        return self.getWantedResolutionPlaylist(self.lastInfo['url'])

    def getStatus(self):
        headers = {"X-Requested-With": "XMLHttpRequest"}
        data = {"room_slug": self.username, "bandwidth": "high"}

        try:
            r = requests.post("x", headers=headers, data=data)
            req = r.request
            print('{}\n{}\r\n{}\r\n\r\n{}'.format(
                '-----------START-----------',
                req.method + ' ' + req.url,
                '\r\n'.join('{}: {}'.format(k, v)
                            for k, v in req.headers.items()),
                req.body,
            ))
            print(r)
            self.lastInfo = r.json()
            if self.lastInfo["room_status"] == "public":
                status = self.Status.PUBLIC
            elif self.lastInfo["room_status"] in ["private", "hidden"]:
                status = self.Status.PRIVATE
            else:
                status = self.Status.OFFLINE
        except Exception as e:
            print("Thrown exception")
            print(e)
            status = self.Status.RATELIMIT

        self.ratelimit = status == self.Status.RATELIMIT
        return status


Bot.loaded_sites.add(Chaturbate)
