from datetime import datetime

from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, DateField, ValidationError


def valid_date(form, field):
    date = field.data
    if '/' not in date:
        raise ValidationError()
    date = date.split('/')
    if int(date[1]) + 2000 < datetime.now().year:
        raise ValidationError('Expiry Date is invalid')
    elif int(date[0]) <= datetime.now().month:
        if int(date[1]) + 2000 <= datetime.now().year:
            raise ValidationError('Expiry Date is invalid')


class PaymentForm(Form):
    first_name = StringField('First Name',
                             [validators.InputRequired(), validators.Length(1, 15, message='Input too long or short')])
    last_name = StringField('Last Name',
                            [validators.InputRequired(), validators.Length(1, 15, message='Input too long or short')])
    street = StringField('Street',
                         [validators.InputRequired(), validators.Length(1, 20, message='Input too long or short')])
    street_number = StringField('Street Number', [validators.InputRequired(), validators.Regexp('\d')])
    town = StringField('Town',
                       [validators.InputRequired(), validators.Length(1, 20, message='Input too long or short')])
    zipcode = StringField('Zipcode', [validators.InputRequired(),
                                      validators.Regexp('\d{5}$', flags=0,
                                                        message='Input has to be a valid Postal Code (exactly 5 Numbers)')])
    credit_card_number = StringField('Credit Card Number', [validators.InputRequired(),
                                                            validators.Regexp('\d{16}$', flags=0,
                                                                              message='Input has to be a valid Credit Card number (exactly 16 Numbers)')])
    name_on_card = StringField('Credit Card Holder', [validators.InputRequired(),
                                                      validators.Length(1, 31, message='Input too long or short')])
    # todo adjust to needed input
    expiry_date = StringField('Expiry Date', [validators.InputRequired(),
                                              validators.Regexp('(0[1-9]|1[0-2])[\/](\d{2})$', flags=0,
                                                                message='Has to be the form mm/yy'), valid_date])

    security_code = StringField('Security Code', [validators.InputRequired(), validators.Regexp('\d{3}$', flags=0,
                                                                                                message='Input has to be a valid CVV number (exactly 3 Numbers)')])


class SignUpForm(Form):
    email = StringField('Email Address', [validators.InputRequired(), validators.Email()])
    # Username can consist out of small and big letters, numbers and whitespaces
    username = StringField('Username', [validators.InputRequired(), validators.Regexp('[a-z]*[A-Z]*[0-9]*\s*', flags=0,
                                                                                      message='Username can not contain special characters')])
    password = PasswordField('Password', [validators.InputRequired()])


class LogInForm(Form):
    email = StringField('Email Address', [validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', [validators.InputRequired()])
    remember = BooleanField('Remember me')


class ResetPasswordForm(Form):
    password = PasswordField('Password', [validators.InputRequired()])


class MfaForm(Form):
    otp = StringField('Enter your MFA Token', [validators.InputRequired(), validators.Regexp('\d{6}$')])
