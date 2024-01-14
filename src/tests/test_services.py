import pytest

from src.services.bitly import *
from src.services.tinyurl import *


class TestServices:

    tinyURL = TinyUrlConnection()
    bitly = BitlyConnection(token=os.environ.get('BITLY_ACCESS_TOKEN'))

    test_data_correct = [
        ('http://www.google.com', "https://tinyurl.com/8wa5w2o"),
        ('www.google.com', "https://tinyurl.com/8wa5w2o"),
        ('http://www.google.com', 'https://bit.ly/3M1gsLx'),
    ]

    @pytest.mark.parametrize("data, expected", test_data_correct[:2])
    def test_tinyURL(self, data, expected):
        resp = self.tinyURL.shorten_url(data)

        assert isinstance(resp, str)
        assert resp == expected

    @pytest.mark.parametrize("data, expected", test_data_correct[2:])
    def test_bitly(self, data, expected):
        resp = self.bitly.shorten_url(data)

        assert isinstance(resp, str)
        assert resp == expected
