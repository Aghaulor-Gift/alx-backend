#!/usr/bin/env python3
"""
Basic Flask application with Babel for i18n.
"""

from flask import Flask, render_template
from flask_babel import Babel

# Instantiate Flask app
app = Flask(__name__)

# Configure app with Config class


class Config:
    """
    Configuration class for Flask app.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


# Instantiate Babel
babel = Babel(app)


@app.route('/')
def index():
    """
    Renders the index page with a welcome message.
    :return: Rendered HTML template
    """
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
