from dotenv import load_dotenv
from flask import Blueprint, request
from flask import render_template

from src.services.bitly import *
from src.services.tinyurl import *

api = Blueprint('api', __name__, template_folder='templates', static_folder='static')
load_dotenv()


@api.route('/', methods=['GET'])
def user():
    """
    Route to the optional frontend route of the application.
    """
    return render_template('index.html')


@api.route('/shortlinks', methods=['POST'])
def create_shortlink():
    url = None
    provider = None
    # receiving values through JSON
    if request.is_json:
        if request.json.keys() == {'url', 'provider'}:
            url = request.json['url']
            provider = request.json['provider']
    # receiving values through the frontend side of the api
    elif request.form:
        if request.form.keys() == {'url', 'provider'}:
            url = request.form['url']
            provider = request.form['provider']

    # checking if any required field is missing
    if not url or not provider:
        error_message = 'Both fields are required.'
        print(f"[Error] {error_message}.")
        return jsonify({"success": False, "error": error_message})

    # user choose Bitly as their preferred provider
    if provider == 'bitly':
        result = bitly_chosen(url=url)
        if str(type(result)) == "<class 'flask.wrappers.Response'>":
            if result.json.get('success') is False:
                return jsonify(result.json)

    # user choose TinyURL as their preferred provider
    elif provider == 'tinyurl':
        result = tinyurl_chosen(url=url)
        if type(result) is dict:
            if result.get('success') is False:
                return result
    else:
        # No preference
        # The system's default preference is tinyurl since it has no limit restrictions
        result = tinyurl_chosen(url=url)
        if type(result) is dict:
            if result.get('success') is False:
                fallback_result = bitly_chosen(url=url)
                if type(fallback_result) is dict:
                    if fallback_result.get('success') is False:
                        return fallback_result
                result = fallback_result

    # Final check for unexpected errors
    if result is None or result == '' or type(result) is not str:
        error_message = f'Shortening Failed, please try again!Error: {result.json.get('error')}'

        return jsonify({"success": False, "error": error_message})

    return jsonify({"url": url, "link": result})
