from flask import *
import asyncio
import main


app = Flask(__name__)


@app.route('/lvl/<int:id>/')
def lvl(id):
    return render_template("lvl.html", guild=main.get_guild(id))


if __name__ == '__main__':
    app.run(threaded=True, port=5000, debug=False)

