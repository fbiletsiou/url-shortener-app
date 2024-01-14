import pytest

from .conftest import app, client


class TestsAPI:

    def test_index(self, client):
        resp = client.get('/')
        assert resp.status_code == 200

    def test_index_bad_http_method(self, client):
        resp = client.post('/')
        assert resp.status_code == 405

    test_data_correct = [
        {'url': 'http://www.google.com', 'provider': 'no preference'},
        {'url': 'http://www.google.com', 'provider': 'tinyurl'},
        {'url': 'http://www.google.com', 'provider': 'bitly'},
    ]

    @pytest.mark.parametrize("data", test_data_correct)
    def test_shortlinks_success(self, client, data):
        resp = client.post('/shortlinks', json=data)

        assert resp.status_code == 200
        assert isinstance(resp.json, dict)
        assert resp.json.keys() == {'link', 'url'}
        assert resp.json.get('url') == data['url']
        if data['provider'] == 'bitly':
            assert 'https://bit.ly/' in resp.json.get('link')
        else:
            assert 'https://tinyurl.com/' in resp.json.get('link')

    def test_shortlinks_bad_http_method(self, client):
        resp = client.get('/shortlinks')

        assert resp.status_code == 405

    test_data_field_missing = [
        {'url': 'http://www.google.com'},
        {'provider': 'tinyurl'},
    ]

    @pytest.mark.parametrize("data", test_data_field_missing)
    def test_shortlinks_fields_missing(self, client, data):
        resp = client.post('/shortlinks', json=data)

        assert resp.status_code == 200
        assert isinstance(resp.json, dict)
        assert resp.json.keys() == {'error', 'success'}
        assert resp.json.get('success') is False
        assert resp.json.get('error') == 'Both fields are required.'

    def test_shortlinks_fixing_invalid_url(self, client):
        data = {'url': 'www.google.com', 'provider': 'bitly'}
        resp = client.post('/shortlinks', json=data)

        assert resp.status_code == 200
        assert isinstance(resp.json, dict)
        assert resp.json.keys() == {'link', 'url'}
        assert resp.json.get('url') == data['url']
        if data['provider'] == 'bitly':
            assert 'https://bit.ly/' in resp.json.get('link')

    test_data_invalid = [
        {'url': 'w.google.com', 'provider': 'bitly'},
        {'url': 'http://www..com', 'provider': 'bitly'},
    ]

    @pytest.mark.parametrize("data", test_data_invalid)
    def test_shortlinks_fixing_invalid_url(self, client, data):
       """
       Bitly is the only provider that cares for the url validity
       """
       resp = client.post('/shortlinks', json=data)

       assert isinstance(resp.json, dict)
       assert resp.json.keys() == {'error', 'success'}
       assert resp.json.get('success') is False
       assert resp.json.get('error') == 'Shortening Failed, please try again!'