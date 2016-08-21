# Gamefolk.org

A [Flask][flask] web application built with Python 3.

## Installation Procedure
### Setup

1.  Clone the repository and cd into it.

    ```sh
    $ git clone https://github.com/gamefolk/gamefolk.org && cd gamefolk.org
    ```

2. Create a Python file somewhere outside of the repository. This file will
   contain secret information relevant to the application that should not be
   pushed the respository. The file should contain the following key-value
   pairs:

    ```python
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////path/to/local/db'
    SECRET_KEY = '...'
    RECAPTCHA_PUBLIC_KEY = '...'
    RECAPTCHA_PRIVATE_KEY = '...'
    PAYPAL_MERCHANT_ID = '...'
    PAYPAL_MERCHANT_EMAIL = '...'
    CARTRIDGE_COST = '...'
    MAIL_SERVER = '...'
    MAIL_PORT = '...'
    MAIL_USERNAME = '...'
    MAIL_PASSWORD = '...'
    DEFAULT_MAIL_SENDER = '...'
    ```

### Docker Installation (Option A)

1. Move your Python config file into your current directory.

2. If you don't have the docker daemon already running, start it now.

3.  Build the image and run the application.

    ```sh
    $ docker-compose build
    $ docker-compose up
    ```

3. Navigate to `localhost:5000` in your browser.

### Manual Installation (Option B)

This application requires Python 3.3+ and node.js. The application is served
using Flask and node.js handles the frontend dependencies. If you're using
Linux, these programs can be installed using your distro's package manager. If
you're using OS X or Windows, I suggest using an unofficial package manager such
as [homebrew][homebrew] or [chocolatey][chocolatey], respectively.

1. Install command-line tools.

    ```sh
    $ sudo pip install virtualenv
    $ sudo npm install -g grunt-cli
    ```

2.  Create and activate a virtualenv.

    ```sh
    $ virtualenv -p /path/to/your/python3 .
    $ source bin/activate
    ```

3. Install local dependencies.

    ```sh
    $ pip install -r requirements.txt
    $ npm install
    $ grunt
    ```

4. Export an environment variable so that Flask can find the secret
   configuration.

    ```sh
    $ export GAMEFOLK_SETTINGS=/path/to/the/file/you/just/made.py
    ```

5. Run the application.

    ```sh
    $ python application.py
    ```

6. Navigate to `localhost:5000` in your browser.

### PayPal Integration

If you want to test the site's PayPal integration, there are some additional
steps:

1. Install localtunnel. This program allows you to pipe requests from the
   internet to your local machine without setting up your machine as a web
   server.

    ```sh
    $ sudo npm install -g localtunnel
    ```

2. With the application already running, open another terminal and run
   localtunnel, telling it that we want to redirect traffic to the default Flask
   port 5000.

    ```sh
    $ lt --port 5000
    ```

3. Open the URL that localtunnel outputs in your browser. Note: due to the way
   that recaptcha verifies registration, you will have to register accounts on
   localhost rather than through the localtunnel.

### Email

To test email integration, you will need to set up a fake STMP server.
Thankfully, Python comes with one built in. Just open up another terminal and
execute

```sh
sudo python -m smptd -n -c DebuggingServer localhost:25
 ```

## Development

If you are editing the website's CSS, you can run `grunt watch` to automatically
rebuild the CSS when the files change.


[flask]: http://flask.pocoo.org
[homebrew]: http://brew.sh
[chocolatey]: http://chocolatey.org
