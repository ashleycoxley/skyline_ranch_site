import flask
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators
import contact_form
import os
import json

app = flask.Flask(__name__)
IMG_EXTENSIONS = ['png', 'jpeg', 'jpg']
MAIN_PAGE_CONTENT = 'main_page_content.json'


class MessageForm(FlaskForm):
    name = StringField('name', validators=[validators.DataRequired()])
    email = StringField('email', validators=[validators.DataRequired(), validators.Email()])
    subject = StringField('subject', validators=[validators.DataRequired()])
    message = TextAreaField('message', validators=[validators.DataRequired()])


@app.route('/')
def main_page():
    with open(MAIN_PAGE_CONTENT, 'r') as infile:
        content = json.load(infile).get('carousel-content')
    return flask.render_template('main.html',
                                 content=content)


@app.route('/lessons')
def lesson_page():
    lesson_pictures = [item for item in os.listdir('static/img/lessons') if item.split('.')[1].lower() in IMG_EXTENSIONS]
    return flask.render_template('lessons.html',
                                 files=lesson_pictures)


@app.route('/aboutus')
def aboutus_page():
    return flask.render_template('instructors.html')


@app.route('/boarding')
def boarding_page():
    boarding_pictures = [item for item in os.listdir('static/img/boarding') if item.split('.')[1].lower() in IMG_EXTENSIONS]
    # maximum 4 pictures for modal
    boarding_pictures = boarding_pictures[:4]
    return flask.render_template('boarding.html',
                                 files=boarding_pictures)


@app.route('/shows')
def shows_page():
    show_pictures = [item for item in os.listdir('static/img/shows') if item.split('.')[1].lower() in IMG_EXTENSIONS]
    return flask.render_template('shows.html',
                                 files=show_pictures)


@app.route('/summercamp')
def camp_page():
    camp_pictures = [item for item in os.listdir('static/img/camp') if item.split('.')[1].lower() in IMG_EXTENSIONS]
    return flask.render_template('summercamp.html',
                                 files=camp_pictures)


@app.route('/piedmont')
def photos_page():
    return flask.render_template('piedmont.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    form = MessageForm()
    if flask.request.method == 'GET':
        return flask.render_template('contact.html', form=form)

    elif flask.request.method == 'POST':
        if form.validate_on_submit():
            subject = form.subject.data
            sender_name = form.name.data
            sender_email = form.email.data
            message = form.message.data
            contact_form.send_emails(subject, sender_name, sender_email, message)
            return flask.render_template('success.html')
        return flask.render_template('contact.html', form=form)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=8080, debug=True)
