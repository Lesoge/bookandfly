import logging
import threading
from datetime import datetime
from flask import Blueprint, render_template, session, request, redirect, url_for, abort, flash
from flask_security import current_user, login_required

from dbModel import Payment_info, Booking_address, db_commit, Booking, Flight
from decorators import breached
from session import get_from_session
from Forms import PaymentForm

app_pay = Blueprint('app_pay', __name__)
logger = logging.getLogger('web_logger')
sem = threading.Semaphore()


@app_pay.route("/pay", methods=['GET', 'POST'])
@login_required
@breached
def pay():
    flight_id = get_from_session('flight_id', request.remote_addr)
    flight = Flight.query.get_or_404(flight_id)
    form = PaymentForm(request.form)

    if not form.validate():
        logger.info('invalid input in pay_form',
                    extra={'ip': request.remote_addr, 'user': current_user.email})
        return render_template('payment.html', flightnr=flight_id, form=form)

    if request.method == 'POST':
        sem.acquire()
        if flight.check_if_full():
            return redirect(url_for('main_app.'))
        pay_address = Booking_address(
            form.first_name.data,
            form.last_name.data,
            form.street.data,
            form.street_number.data,
            form.town.data,
            form.zipcode.data
        )
        pay_info = Payment_info(
            form.credit_card_number.data,
            form.name_on_card.data,
            datetime.strptime(form.expiry_date.data, '%m/%y'),
            form.security_code.data
        )
        db_commit(pay_address, pay_info)
        booking = Booking(
            current_user.id,
            flight.id,
            pay_address.id,
            pay_info.id)
        db_commit(booking)
        sem.release()
        session['booking_id'] = booking.id
        logger.info('created booking for' + str(booking.id),
                    extra={'ip': request.remote_addr, 'user': current_user.email})
        return redirect(url_for('app_pay.booking_info'))

    return render_template('payment.html', flightnr=flight_id, form=form)


@app_pay.route("/booking", methods=['GET', 'POST'])
@login_required
@breached
def booking_info():
    booking_id = get_from_session('booking_id', request.remote_addr)
    booking = Booking.query.get_or_404(booking_id)
    if request.method == 'POST':
        booking.payed = True
        db_commit(booking)

        logger.info('payed for booking' + str(booking.id),
                    extra={'ip': request.remote_addr, 'user': current_user.email})
        flash("You successfully finished your order. Have a nice flight!")
        return redirect(url_for('app_main.index'))
    return render_template('booking.html', booking=booking)
