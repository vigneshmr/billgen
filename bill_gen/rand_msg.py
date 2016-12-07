import HTMLParser
import requests

from common_str import DEFAULT_MESSAGE


class RandomMsg:
    def __int__(self):
        pass

    @staticmethod
    def get_message():
        r = requests.get('http://api.irkfdb.in/facts/random')
        if not r:
            # api call failed. return default
            return DEFAULT_MESSAGE
        # call succeeded. Return joke
        msg = r.json()
        html_parser = HTMLParser.HTMLParser()
        joke = str(msg['resultSet']['data'][0]['fact'])
        joke = joke.replace('<b>', '')
        joke = joke.replace('</b>', '')
        return html_parser.unescape(joke)
