#!/usr/bin/env python3
""" A  basic Flask app module that create a single / route and an index.html
template that simply outputs “Welcome to Holberton” as page title (<title>)
and “Hello world” as header (<h1>).
"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def index():
    """
    Renders the index page with a welcome message.
    :return: Rendered HTML template
    """
    return render_template("0-index.html")


if __name__ == '__main__':
    app.run(debug=True)
