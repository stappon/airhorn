from flask import Flask, send_file
from os import getenv
app = Flask(__name__)

@app.route('/')
def index():
    return send_file("../static/index.html")

if __name__ == '__main__':
    port = getenv("PORT")
    print getenv("PWD")
    if port:
        port = int(port)
    else:
        port = 5000
    print "booted up serve_index"
    app.run(port=port)
