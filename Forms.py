from wtforms import Form, BooleanField, StringField, PasswordField, validators

class PaymentForm(Form):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    street = StringField('Street')
    street_number = StringField('Street Number')
    town = StringField('Town')
    zipcode = StringField('Zipcode')
    credit_card_number = StringField('Credit Card Number')
    name_on_card = StringField('Credit Card Holder')
    expiry_date = StringField('Expiry Date')
    security_code = StringField('Security Code')
