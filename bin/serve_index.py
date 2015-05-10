from flask import Flask, send_file
from os import getenv
app = Flask(__name__)

@app.route('/')
def index():
    return send_file("../static/index.html")

if __name__ == '__main__':
    port = getenv("PORT")
    if port:
        port = int(port)
    else:
        port = 5000
    app.run(port=port)
