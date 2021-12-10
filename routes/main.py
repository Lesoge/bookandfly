from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from User import Flight, Booking

app_main = Blueprint('app_main', __name__)


@app_main.route('/', methods=['GET'])
def index():
    flights = Flight.query.filter(Flight.depTime >= datetime.now())
    bookings = Booking.query
    return render_template('index.html', flights=flights, bookings=bookings)


@app_main.route('/profile', methods=['GET'])
@login_required
def profile():
    bookings = Booking.query.filter(Booking.user == current_user, Flight.depTime >= datetime.now(), Booking.payed)
    return render_template('profile.html', user=current_user, bookings=bookings)


@app_main.route("/flight/<int:flightnr>", methods=['GET'])
def flight(flightnr):
    flight = Flight.query.get_or_404(flightnr)
    bookings = Booking.query
    return render_template("flight.html", flight=flight, bookings=bookings)

@app_main.route("/flight/<int:flightnr>", methods=['POST'])
def flight_post(flightnr):
    session['flight_id'] = flightnr
    return redirect(url_for('app_pay.pay'))