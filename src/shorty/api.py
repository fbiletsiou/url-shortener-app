from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from flask import render_template
from flask import Response


from src.shorty.utils.url_tools import shorten_url

api = Blueprint('api', __name__, template_folder='templates', static_folder='static')
load_dotenv()


@api.route('/', methods=['GET'])
def main():
    """
    Route to the frontend route of the application.
    """
    return render_template('index.html')


@api.route('/shortlinks', methods=['POST'])
def create_shortlink():
    """
    Endpoint to create a short link using JSON for API use.

    JSON Payload:
    {
        "url": "original_url",
        "provider": "selected_provider"
    }

    """
    # receiving values through API
    if request.is_json and request.json.keys() == {'url', 'provider'}:
        url = request.json['url']
        provider = request.json['provider']

        # checking if any required field is missing
        if not url or not provider:
            error_message = 'Both fields:url, provider are required.'
            return Response(
                error_message,
                status=400,
            )

        result = shorten_url(url=url, provider=provider)

        # Final check for unexpected errors
        if result == '' or not isinstance(result, str):
            error_message = "Failed to shorten the URL"
            return Response(
                error_message,
                status=404,
            )

        return jsonify({"success": True, "url": url, "link": result})

    else:
        return Response(
            "Invalid payload",
            status=400,
        )


@api.route('/ui-shortlinks', methods=['POST'])
def create_shortlink_for_web():
    """
    Endpoint to create a short link for the web UI.

    Form Data:
    url=original_url
    provider=selected_provider
    """
    if request.form and request.form.keys() == {'url', 'provider'}:
        url = request.form['url']
        provider = request.form['provider']

        # checking if any required field is missing
        if not url or not provider:
            error_message = 'Both fields:url, provider are required.'
            return render_template('result_display.html', error_msg=error_message)

        result = shorten_url(url=url, provider=provider)

        # Final check for unexpected errors
        if result == '' or not isinstance(result, str):
            error_message = "Failed to shorten the URL"
            return render_template('result_display.html', error_msg=error_message)

        payload = {"url": url, "link": result, "provider": provider}
        return render_template('result_display.html', payload=payload)

    else:
        return render_template('result_display.html', error_msg="Invalid payload")


@api.route('/available-providers', methods=['GET'])
def get_available_provider_info():
    """
    Endpoint to display information about available URL shortening providers.
    """
    return render_template('providers.html')
