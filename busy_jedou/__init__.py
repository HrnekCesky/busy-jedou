"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import busy_jedou.views
import busy_jedou.api

