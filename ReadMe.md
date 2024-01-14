URL Shortener - Florina Biletsiou
======================
## Description

URL Shortener, is a service to help to reduce the length of the URL so that it can be shared and used easily.
<br>The two providers used for this project are Bitly and TinyURL.

## Getting Started

### Built With

This project was build with the following frameworks, libraries and tools:
1. [Flask](http://flask.pocoo.org/)
2. [pytest](http://pytest.org/latest/)
3. [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
4. [HTTP statuses](https://httpstatuses.com/)
5. [bitlyshortener](https://bitly.com/pages/solutions/for-developers)

### Installing

Before running the application, make sure you follow the installing steps below

1. Make sure you have a Python version (3.6+) installed on your system. 
    ```
    py --version
    ```
2. Create the project's virtual environment and activate it. 
    ```
    pip install virtualenv
    virtualenv venv
    ```
   in order to activate the new virtual environment:
    * For Mac OS / Linux
    ```
    source venv/bin/activate 
    ```
    * For Windows
    ```
    venv\Scripts\activate
    ```
3. Install the libraries required from the `requirements.txt`:
    ```
    pip install requirements.txt
    ```

### Configuration

In order to be able to use Bitly there needs to be a Bitly Connected to the application. 
For that to happen please follow the [instructions provided](https://support.bitly.com/hc/en-us/articles/230647907-How-do-I-generate-an-OAuth-access-token-for-the-Bitly-API-) by Bitly to create the Acces Token that is required.
Next, create a `.env` file at the main project's location and type:
```
BITLY_ACCESS_TOKEN= YOUR ACCESS TOKEN
```


### Executing program

* If you are using an IDE, follow the steps below (The demonstration is for PyCharm):
  1. Click `File`>`Open` and open the project on your IDE. 
  2. Navigate to `Run`>`Edit Configurations`>`(+)` and add a `Flask server` type of configuration. 
  3. Fill the configuration fields as listed below:
     * Target: C:\(LOCAL LOCATION)\url-shortener-app\src\run.py
     * FLASK_ENV: development
     * FLASK_DEBUG: True
     * Python interpreter: (THE VIRTUAL ENV WE CREATED EARLIER)
  4. Click Run
* Using the Command Line
  1. Open a terminal and navigate to the project's location
  2. Simply type:
       ```
       python run.py
       ```

Access the application at : http://127.0.0.1:5000

## Testing

To execute the project's tests, open a terminal and run:
```
py.test -v    
```

## Sending Requests

The primary way of sending requests is from outside sources.<br> 
One way to send requests is **through an API testing application**, like Postman or Insomnia.
<br>To do that,
1. send a POST request at http://127.0.0.1:5000/shortlinks
2. include the following to the JSON part of the request:
   ```
    {
      "url": "ANY-VALID-URL",
      "provider": "PROVIDER"
    }
    ```
    When it comes to providers the available options are:
   * bitly
   * tinyurl
   * no preference

An easier way to **send a request is from the frontend route** that I additionally created. <br>
Just head to the index page and fill the form with the url you want to shorten and your provider preference, if there is any.


## Authors
[Florina Biletsiou](https://www.linkedin.com/in/florina-biletsiou/) [@fbiletsiou](https://github.com/fbiletsiou)

