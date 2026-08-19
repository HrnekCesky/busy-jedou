"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

@app.route("plswork")
def plswork():
    return "works"

import views
import api

