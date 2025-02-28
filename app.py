from flask_bootstrap import Bootstrap
from flask import Flask, render_template

import source.utils


app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route("/")
def home():
    context = {
        "drivers": source.utils.get_data()
    }
    return render_template('base.html', **context)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
