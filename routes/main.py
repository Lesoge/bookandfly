
from flask import Blueprint, render_template, session, redirect, url_for, flash
from flask_security import login_required, current_user
from datetime import datetime
from dbModel import Flight, Booking
from decorators import breached

app_main = Blueprint('app_main', __name__)


@app_main.route('/', methods=['GET'])
def index():
    bookings = Booking.query
    flights = Flight.query.filter(Flight.depTime >= datetime.now())
    flights = [f for f in flights if f.available_seats(bookings) > 0]
    return render_template('index.html', flights=flights, bookings=bookings)


@app_main.route('/profile', methods=['GET'])
@login_required
@breached
def profile():
    bookings = Booking.query.filter(Booking.user == current_user, Flight.depTime >= datetime.now(), Booking.payed)
    return render_template('profile.html', user=current_user, bookings=bookings)


@app_main.route("/flight/<int:flightnr>", methods=['GET'])
@login_required
@breached
def flight(flightnr):
    flight = Flight.query.get_or_404(flightnr)
    bookings = Booking.query
    return render_template("flight.html", flight=flight, bookings=bookings)

@app_main.route("/flight/<int:flightnr>", methods=['POST'])
@login_required
@breached
def flight_post(flightnr):
    flight = Flight.query.get_or_404(flightnr)
    bookings = Booking.query
    if flight.available_seats(bookings) == 0:
        flash('No more Tickets are available for this flight')
        return redirect(url_for('app_main.flight', flightnr=flight.id))
    session['flight_id'] = flightnr
    return redirect(url_for('app_pay.pay'))
