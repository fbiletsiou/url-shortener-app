import os

from src.shorty.services.url_strategies import BitlyShortener, TinyUrlShortener, valid_format


def shorten_url(url: str, provider: str) -> str:
    """
    Shorten a URL using the specified provider.

    :param url: The original URL to be shortened.
    :param provider: The preferred URL shortening provider ('bitly', 'tinyurl', or None for fallback).
    :return: The shortened URL or a dictionary with an error message.
    """
    url_shortener = None
    # Choose the appropriate strategy based on the selected provider
    if provider == 'bitly':
        url_shortener = BitlyShortener(token=os.environ.get('BITLY_ACCESS_TOKEN'))
    elif provider == 'tinyurl':
        url_shortener = TinyUrlShortener()
    # If the selected provider is invalid or None, use a fallback strategy (e.g., TinyURL)
    if url_shortener is None:
        url_shortener = TinyUrlShortener()
    try:
        result = url_shortener.shorten_url(url_to_convert=url)
    except Exception as e:
        is_url_valid = valid_format(url)
        if not is_url_valid['valid'] and is_url_valid['corrected']:
            url_corrected = is_url_valid['corrected']
            try:
                result = url_shortener.shorten_url(url_to_convert=url_corrected)
                return result
            except Exception:
                # Handle any unexpected errors here
                error_message = f'URL shortening failed. Error: {e}'
                print(error_message)
                return ''

    return result
