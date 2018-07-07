import HTMLParser
import requests

from common_str import DEFAULT_MESSAGE


class RandomMsg:
    def __int__(self):
        pass

    @staticmethod
    def get_message():
        r = requests.get('https://api.chucknorris.io/jokes/random')
        if not r:
            return DEFAULT_MESSAGE

        msg = r.json().get('value', None)
        if not msg:
            return DEFAULT_MESSAGE

        msg=msg.replace('Chuck Norris', 'Rajnikanth')
        return msg
