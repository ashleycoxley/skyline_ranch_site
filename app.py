import flask
import sqlalchemy


app = flask.Flask(__name__)


@app.route('/')
def main_page():
    return flask.render_template('main.html')


@app.route('/lessons')
def lesson_page():
    return flask.render_template('lessons.html')


@app.route('/boarding')
def boarding_page():
    return flask.render_template('boarding.html')


@app.route('/training')
def training_page():
    return flask.render_template('training.html')


@app.route('/instructors')
def instructors_page():
    return flask.render_template('instructors.html')


@app.route('/summercamp')
def camp_page():
    return flask.render_template('summercamp.html')


@app.route('/photos')
def photos_page():
    return flask.render_template('photos.html')


@app.route('/contact', methods=['GET'])
def contact_page():
    return flask.render_template('contact.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=8080, debug=True)
