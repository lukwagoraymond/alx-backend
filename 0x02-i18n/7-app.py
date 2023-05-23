#!/usr/bin/env python3
"""This module contains a Basic Flask App"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Union, Dict
from pytz import timezone
import pytz.exceptions

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
    """A class containing configuration of supported
    languages by the Flask App"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Based on the value for the locale variable in
    the url return the based suitable language"""
    # locale from URL parameters
    res_object = request.args.get('locale')
    if res_object in app.config['LANGUAGES']:
        return res_object
    # locale from user settings
    if g.user:
        res_object = g.user.get('locale')
        if res_object and res_object in app.config['LANGUAGES']:
            return res_object
    # locale from request headers
    res_object = request.headers.get('locale', None)
    if res_object in app.config['LANGUAGES']:
        return res_object
    # Default locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """Based on the placement in of the timezone value
    return the based suitable timezone"""
    tym_zone = request.args.get('timezone', None)
    if tym_zone:
        try:
            return timezone(tym_zone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    if g.user:
        try:
            tym_zone = g.user.get('timezone')
            return timezone(tym_zone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    return app.config['BABEL_DEFAULT_TIMEZONE']


def get_user() -> Union[Dict, None]:
    """Returns user dict if ID user Dictionary
    or None if ID not in user dictionary"""
    ID = request.args.get('login_as')
    if ID is not None and int(ID) in users.keys():
        return users.get(int(ID))
    return None


@app.before_request
def before_request() -> None:
    """Function that will run before each request"""
    user_got = get_user()
    g.user = user_got


# babel.init_app(app, locale_selector=get_locale, timezone_selector=get_timezone)


@app.route('/', strict_slashes=False)
def index() -> str:
    """End point route to handle / route"""
    return render_template('7-index.html')


if __name__ == "__main__":
    app.run(port='5000', host='0.0.0.0', debug=True)
