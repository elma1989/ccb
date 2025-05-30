from flask import Flask
from route import recepe

app = Flask (__name__)
app.register_blueprint(recepe)