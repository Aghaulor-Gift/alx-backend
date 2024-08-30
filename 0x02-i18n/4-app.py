#!/usr/bin/env python3
"""Use the _ or gettext function to parametrize your templates. Use the
message IDs home_title and home_header """
from flask import Flask, render_template, request
from flask_babel import Babel, _


app = Flask(__name__)
babel = Babel(app)
app.url_map.strict_slashes = False


class Config():
    """Represents a Flask Babel configuration."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEK_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Determine the best match for the supported languages.
    If a 'locale' argument is provided in the request URL,
    use it if it's a supported language.
    :return: Best match language string"""
    # Check if 'locale' is present in the request arguments
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    # Fallback to the default behavior
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route("/")
def index():
    """Renders the index page with a welcome message.
    :return: Rendered HTML template  """
    return render_template("4-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0",  port=5000, debug=True)
