from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Flasks for everyone"

if __name__ == "__main__":
    app.run()

"""
/usr/bin/python /Users/john.ubante/PycharmProjects/poven/projects/flask/helloFlask.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [08/Apr/2016 18:04:37] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [08/Apr/2016 18:04:37] "GET /favicon.ico HTTP/1.1" 404 -
"""