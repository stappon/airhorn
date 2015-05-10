from flask import Flask, send_file, send_from_directory
from os import getenv
import os
app = Flask(__name__, static_folder=os.path.dirname(os.path.realpath(__file__)) + "/../static")
# app.debug = True

@app.route('/')
def index():
    return send_file(app.static_folder + "/index.html")

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    port = getenv("PORT")
    if port: # heroku
        host = "0.0.0.0"
        port = int(port)
    else: # dev
        host = "127.0.0.1"
        port = 5000

    app.run(host=host, port=port)
