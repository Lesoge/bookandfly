from flask import Blueprint, render_template, session, request, redirect, url_for, abort, flash
from flask_login import current_user, login_required

from User import Payment_info, Booking_address, db_commit, Booking, Flight

app_pay = Blueprint('app_pages', __name__)


@app_pay.route("/pay", methods=['GET'])
# @login_required todo remove comment login required only for develoopment
def pay():
    flight_id = get_from_session('flight_id')
    flight = Flight.query.get_or_404(flight_id)
    if flight.check_if_full():
        flash('No more Tickets are available for this flight')
        return redirect(url_for('app_main.flight', flightnr=flight.id))
    return render_template('payment.html')


@app_pay.route("/booking", methods=['POST'])
# @login_required
def pay_post():
    flight_id = get_from_session('flight_id')
    flight = Flight.query.get_or_404(flight_id)
    if flight.check_if_full():
        return redirect(url_for('app_main.flight', flightnr=flight.id))

    pay_info = Payment_info(
        request.form.get('credit_card_number'),
        request.form.get('name_on_card'),
        request.form.get('expire_date'),
        request.form.get('security_code')
    )
    pay_address = Booking_address(
        request.form.get('first_name'),
        request.form.get('last_name'),
        request.form.get('street'),
        request.form.get('street_number'),
        request.form.get('town'),
        request.form.get('zipcode'),
    )
    booking = Booking(
        current_user.id,
        flight.id,
        pay_address.id,
        pay_info.id)
    db_commit(pay_address, pay_info, booking)
    session['booking_id'] = booking.id
    return redirect(url_for('app_pay.booking_info'))


@app_pay.route("/booking", methods=['GET'])
# @login_required
def booking_info():
    booking_id = get_from_session('booking_id')
    booking = Booking.query.get_or_404(booking_id)


@app_pay.route("/booking", methods=['Post'])
# @login_required
def booking_info_post():
    booking_id = get_from_session('booking_id')
    booking = Booking.query.get_or_404(booking_id)
    booking.payed = True
    db_commit(booking)


def get_from_session(key):
    if key in session:
        return session['flight_id']
    else:
        abort(404, description='you tried to access that page through an invalid path')
