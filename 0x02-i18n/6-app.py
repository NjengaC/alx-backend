#!/usr/bin/env python3
"""A Basic Flask app with internationalization support."""
from flask_babel import Babel, _, gettext
from typing import Union, Dict
from flask import Flask, render_template, request, g


class Config:
    """Represents a Flask Babel configuration."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)

users: Dict[int, Dict[str, Union[str, None]]] = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict[str, Union[str, None]], None]:
    """Retrieve user information based on login_as parameter."""
    login_id = request.args.get('login_as')
    if login_id:
        return users.get(int(login_id), None)
    return None


@app.before_request
def before_request() -> None:
    """Set g.user to the user retrieved from get_user()."""
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """Determine the user's preferred language."""
    locale = request.args.get('locale')
    if locale in app.config["LANGUAGES"]:
        return locale

    if g.user and g.user['locale'] in app.config["LANGUAGES"]:
        return g.user['locale']

    header_locale = request.headers.get('Accept-Language')
    if header_locale:
        return header_locale.split(',')[0]

    return app.config['BABEL_DEFAULT_LOCALE']


@app.route('/')
def get_index() -> str:
    """Render the index page."""
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
