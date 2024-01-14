import os

import bitlyshortener
import validators
from flask import jsonify


def bitly_chosen(url):
    """
    Actions for the api to do if the user choose Bitly as their preferred provider
    Return: A str of the shorter url result or a json obj with the error message.
    """
    bitly_provider = BitlyConnection(token=os.environ.get('BITLY_ACCESS_TOKEN'))
    # shorten the given url
    try:
        result = bitly_provider.shorten_url(url_to_convert=url)
    except Exception as e:
        # Fallback option
        # check if format is valid and get the corrected version
        is_url_valid = valid_format(url)
        if not is_url_valid['valid'] and is_url_valid['corrected']:
            # there is a new corrected url value
            url_corrected = is_url_valid['corrected']
            try:
                result = bitly_provider.shorten_url(url_to_convert=url_corrected)
            except Exception as fallback_e:
                # Attempt to shorten the corrected url failed
                print(f'[Error] Second Bitly attempt failed.\nError:{fallback_e}')
                error_message = f'Second Bitly attempt failed. Error:{fallback_e}. Please try again.'

                return jsonify({"success": False, "error": error_message})

        else:
            # Bitly failed to shorten the url. Notifying the user
            print(f"[Error] Bitly failed \nError message: {e}")
            error_message = f'{e}. Please try again.'

            return jsonify({"success": False, "error": error_message})

    return result


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
            corrected_url = 'http://' + url_to_convert
        # To add more corrections in the future

        return {'valid': False, 'corrected': corrected_url}


class BitlyConnection:
    """
    Class responsible to establish the connection with the Bitly API and provide the related shortening function.
    """

    def connect(self):
        """
        Function that establishes the connection with the Bilty API.
        The Bitly Access Token is required for the connection to be successfully.
        Please make sure the token is stored at the .env file.
        """
        try:
            conn = bitlyshortener.Shortener(tokens=[self.BITLY_ACCESS_TOKEN, ])
            return conn
        except Exception as e:
            raise e

    def __init__(self, token):
        self.BITLY_ACCESS_TOKEN = token
        self.connection = self.connect()

    def shorten_url(self, url_to_convert):
        """
        Function that executes the link shortening.
        """
        try:
            response = self.connection.shorten_urls([url_to_convert])
            return response[0]
        except bitlyshortener.exc.RequestError as e:
            # Tell the user their URL's format is invalid
            raise e
        except Exception as e:
            # unexpected error
            raise e
