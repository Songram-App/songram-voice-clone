from flask import Flask

app = Flask(__name__)

from .api import *  # Import API routes

# Additional application setup can be done here if needed.