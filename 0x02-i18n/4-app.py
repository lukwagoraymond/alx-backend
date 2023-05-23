#!/usr/bin/env python3
"""This module contains a Basic Flask App"""

from flask import Flask, render_template, request
from flask_babel import Babel


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
    res_object = request.args.get('locale')
    if res_object in app.config['LANGUAGES']:
        return res_object
    return request.accept_languages.best_match(app.config['LANGUAGES'])


# babel.init_app(app, locale_selector=get_locale)


@app.route('/', strict_slashes=False)
def index() -> str:
    """End point route to handle / route"""
    return render_template('4-index.html')


if __name__ == "__main__":
    app.run(port='5000', host='0.0.0.0', debug=True)
