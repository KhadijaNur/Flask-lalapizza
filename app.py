from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import DateField, TimeField, IntegerField, StringField, SubmitField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lalapizza.db'
app.config['SECRET_KEY'] = '123456'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    num_people = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Booking {self.name} for {self.num_people} people on {self.date} at {self.time}>'

class BookingForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    num_people = IntegerField('Number of People', validators=[DataRequired()])
    name = StringField('Your Name', validators=[DataRequired()])
    submit = SubmitField('Submit Reservation')  

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)  

    def __repr__(self):
        return f'<Course {self.title}>'


class Chef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chef_name = db.Column(db.String(100), nullable=False)
    chef_city = db.Column(db.String(100), nullable=False)
    chef_image = db.Column(db.String(400), nullable=True)
    chef_speciality = db.Column(db.String(100), nullable=True)
    chef_description = db.Column(db.Text, nullable=True)

class DeliciousStarters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)  

    def __repr__(self):
        return f'<Course {self.title}>'

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    message = db.Column(db.Text)

@app.route('/')
def index():
    with app.app_context():
        bookings = Booking.query.all()
        form = BookingForm()  
    courses = Course.query.all()
    return render_template('index.html', form=form, bookings=bookings, courses=courses)


@app.route('/book', methods=['GET', 'POST'])
def book():
    form = BookingForm()

    if form.validate_on_submit():
        date = form.date.data
        time = form.time.data
        num_people = form.num_people.data
        name = form.name.data

        new_booking = Booking(date=date, time=time, num_people=num_people, name=name)
        db.session.add(new_booking)
        db.session.commit()

        return redirect(request.referrer)

    return render_template('index.html', form=form, form_submitted=False)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = BookingForm() 
    contactform = ContactForm()

    if contactform.validate_on_submit():
        new_contact = Contact(
            name=contactform.name.data,
            email=contactform.email.data,
            message=contactform.message.data
        )
        db.session.add(new_contact)
        db.session.commit()

        return redirect(url_for('contact', form_submitted=True))

    return render_template('contact.html', contactform=contactform, form=form, form_submitted=request.args.get('form_submitted'))

@app.route('/about')
def about():

    starters = DeliciousStarters.query.all()
    return render_template('about.html', starters=starters)


@app.route('/chefs')
def chefs():
    with app.app_context():
        bookings = Booking.query.all()
        form = BookingForm()     
    chefs_data = Chef.query.all()
    return render_template('chefs.html', chefs=chefs_data , form=form, bookings=bookings)

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/bookings')
def view_bookings():
    bookings = Booking.query.all()
    return render_template('bookings.html', bookings=bookings)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=false, host='0.0.0,')
