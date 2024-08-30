#!/usr/bin/env python3
"""Use the _ or gettext function to parametrize your templates. Use the
message IDs home_title and home_header """
from flask import Flask, render_template, request
from flask_babel import Babel, _


app = Flask(__name__)
babel = Babel(app)
app.url_map.strict_slashes = False


class Config():
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEK_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Use request.accept_languages to determine the best match with
    the supported languages"""
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index():
    """Renders the index page with a welcome message.
    :return: Rendered HTML template  """
    return render_template("3-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0",  port=5000, debug=True)
