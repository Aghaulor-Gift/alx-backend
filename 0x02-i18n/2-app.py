#!/usr/bin/env python3
"""Create a get_locale function with the babel.localeselector decorator that
request.accept_languages to determine the best match with our supported
languages."""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config():
    """Configuration class for Flask app """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def get_locale():
    """ Use request.accept_languages to determine the best match with
    the supported languages"""
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index():
    """Renders the index page with a welcome message.
    :return: Rendered HTML template """
    return render_template("2-index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
