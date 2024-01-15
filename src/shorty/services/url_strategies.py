import urllib
from abc import ABC, abstractmethod
from http import HTTPStatus

import bitlyshortener
import requests
import validators


def valid_format(url_to_convert):
    """
    Function that performs validation checks on the url provided.
    If the url is not valid (e.g. ww.google.com), attempting to fix it.
    Current solution is just indicative, more to be added.
    """
    if validators.url(url_to_convert):
        return {'valid': True}
    else:
        corrected_url = None
        if url_to_convert[:4] == 'www.':
            corrected_url = 'https://' + url_to_convert
        # To add more corrections in the future

        return {'valid': False, 'corrected': corrected_url}


class UrlShortenerStrategy(ABC):
    """
    Interface for URL shortening strategies.
    """

    @abstractmethod
    def shorten_url(self, url_to_convert):
        """
        Method to shorten a URL.
        """
        pass


class BitlyShortener(UrlShortenerStrategy):
    """
    Implementation of UrlShortenerStrategy for Bitly.
    """

    def __init__(self, token):
        self.BITLY_ACCESS_TOKEN = token
        self.connection = self.connect()

    def connect(self):
        """
        Establish the connection with the Bitly API.
        The Bitly Access Token is required for the connection to be successful.
        """
        try:
            conn = bitlyshortener.Shortener(tokens=[self.BITLY_ACCESS_TOKEN, ])
            return conn
        except Exception as e:
            raise e

    def shorten_url(self, url_to_convert):
        """
        Execute the link shortening using Bitly.
        """
        try:
            response = self.connection.shorten_urls([url_to_convert])
            return response[0]
        except bitlyshortener.exc.RequestError as e:
            raise e
        except Exception as e:
            raise e


class TinyUrlShortener(UrlShortenerStrategy):
    """
    Implementation of UrlShortenerStrategy for TinyURL.
    """

    def shorten_url(self, url_to_convert):
        """
        Execute the link shortening using TinyURL.
        """
        try:
            url = "http://tinyurl.com/api-create.php?" + urllib.parse.urlencode({"url": url_to_convert})
            response = requests.get(url)
            if response.status_code == HTTPStatus.OK:
                return response.text
            else:
                raise Exception(f'{response.status_code} - {response.reason}')
        except Exception as e:
            raise e
