import flask
import sqlalchemy


app = flask.Flask(__name__)


@app.route('/')
def main_page():
    return flask.render_template('main.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=8080, debug=True)
