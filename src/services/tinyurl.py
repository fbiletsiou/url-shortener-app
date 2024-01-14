import requests
import urllib
from http import HTTPStatus
from flask import jsonify


def tinyurl_chosen(url):
    """
    Actions for the api to do if the user choose TinyURL as their preferred provider
    Return: A str of the shorter url result or a json obj with the error message.
    """
    tinyurl = TinyUrlConnection()
    # shorten the given url
    try:
        result = tinyurl.shorten_url(url_to_convert=url)
    except Exception as e:
        # TinyURL failed to shorten the url. Notifying the user
        print(f"[Error] TinyURL failed \nError message: {e}")
        error_message = f'{e}. Please try again.'

        return jsonify({"success": False, "error": error_message})
    return result


class TinyUrlConnection:
    """
    Class responsible to establish the connection with the TinyURL API and provide the related shortening function.
    """

    def __init__(self):
        self.create_url_base = "http://tinyurl.com/api-create.php"

    def shorten_url(self, url_to_convert):
        """
        Function that executes the link shortening.
        """
        try:
            url = self.create_url_base + "?" + urllib.parse.urlencode({"url": url_to_convert})
            response = requests.get(url)
            if response.status_code == HTTPStatus.OK:
                return response.text
            else:
                raise Exception(f'Error: {response.status_code} msg: {response.reason}')
        except Exception as e:
            raise e
