from flask import Flask, render_template
from fodder import Fodder

app = Flask(__name__)

@app.route("/")
def hello():
    results = []
    results.append("slam")
    f = Fodder()
    results.append(f.get_sport())
    return render_template('item.html', result=results)
    # return render_template('list_item.html', result=results)

if __name__ == "__main__":
    app.run(port=80)
