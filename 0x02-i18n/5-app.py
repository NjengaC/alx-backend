#!/usr/bin/env python3
"""This module helps with internalization and localization the application"""

from flask_babel import Babel, _, gettext
from flask import Flask, render_template, request, g
from typing import Mapping, Union


class Config:
    """Configurations for the Flask application."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

# Mock user database
users: Mapping[int, Mapping[str, Union[str, None]]] = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Mapping[str, Union[str, None]], None]:
    """Retrieve user information based on login_as parameter."""
    login_info = request.args.get('login_as')
    if login_info:
        return users.get(int(login_info), None)
    return None


@app.before_request
def before_request() -> None:
    """Set g.user to the user retrieved from get_user()."""
    g.user = get_user()


@app.route("/", methods=["GET"])
def welcome_page() -> str:
    """Render the HTML welcome page."""
    return render_template('5-index.html')


@app.template_global()
def _(msgid: str, **kwargs) -> str:
    """Mock implementation of gettext."""
    translations = {
        "home_title": "Welcome to the Homepage",
        "home_header": "Welcome to our Website",
        "logged_in_as": "You are logged in as %(username)s.",
        "not_logged_in": "You are not logged in."
    }
    return translations[msgid] % kwargs


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
