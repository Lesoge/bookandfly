import pyotp
from flask_security import hash_password

from dbModel import user_datastore, User


def test_home_page(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200


def test_login(test_client, init_database):
    password = hash_password('Saphira1010')
    new_user = user_datastore.create_user(username='test', email='test@test.de', password=password,
                                          roles=['end-user'])
    new_user2 = user_datastore.create_user(username='test2', email='test2@test.de', password=password,
                                           roles=['end-user'], mfasecretkey='F4NI4XX2OME5P6MMQVRMFN7MYPG3YZNA')
    user_datastore.commit()
    response1 = test_client.post('/login', data=dict(password='Saphira1010', email='test@test.de'),
                                 follow_redirects=True)
    response2 = test_client.post('/login', data=dict(password='Saphira1010', email='test2@test.de'),
                                 follow_redirects=True)

    assert response1.request.path == '/signup/mfa'
    assert response2.request.path == '/login/mfa'


def test_signup(test_client, init_database):
    email = 'test2@test.de'
    response = test_client.post('/signup', data=dict(username='test', password='asdwfalskhfiuqh', email=email),
                                follow_redirects=True)
    assert response.request.path == '/signup/mfa'
    assert User.query.filter_by(email=email) is not None


def test_signup_mfa(test_client, init_database):
    new_user = user_datastore.create_user(username='test', email='test@test.de', password='Saphira1010',
                                          roles=['end-user'])
    new_user2 = user_datastore.create_user(username='test2', email='test2@test.de', password='Saphira1010',
                                           roles=['end-user'], mfasecretkey='F4NI4XX2OME5P6MMQVRMFN7MYPG3YZNA')

    test_client.post('/login', data=dict(username='test', password='Saphira1010', email='test@test.de'),
                     follow_redirects=True)
    response2 = test_client.post('/login', data=dict(username='test2', password='Saphira1010', email='test2@test.de'),
                                 follow_redirects=True)

    assert new_user.mfasecretkey is not None
    assert response2.request.path == '/login/mfa'


def test_pay(test_client, init_database):
    new_user = create_test_user()
    login_test_user(test_client, new_user)

    with test_client.session_transaction() as sess:
        sess['flight_id'] = 5
    print(sess)

    response = test_client.post('/pay', data=dict(first_name='Kevin', last_name='Chantal', street='Dummen Straße',
                                                  street_number='69', town='Bilefeld', zipcode='69420',
                                                  credit_card_number='1234123412341234', name_on_card='Kevin Chantal',
                                                  expiry_date='06/23', security_code='123'), follow_redirects=True)
    assert response.request.path == '/booking'


def test_login_to_profile(test_client, init_database):
    # create Test-User
    new_user2 = user_datastore.create_user(username='test2', email='test2@test.de', password='Saphira1010',
                                           roles=['end-user'], mfasecretkey='F4NI4XX2OME5P6MMQVRMFN7MYPG3YZNA')
    otp2 = pyotp.TOTP(new_user2.mfasecretkey).now()
    # User logs in
    response2 = test_client.post('/login',
                                 data=dict(username='test2', password='Saphira1010', email='test2@test.de', otp=otp2),
                                 follow_redirects=True)
    # User enters his MFA-Token
    response2 = test_client.post(response2.request.path,
                                 data=dict(username='test2', password='Saphira1010', email='test2@test.de', otp=otp2),
                                 follow_redirects=True)
    assert response2.request.path == '/profile'


def test_signup_to_profile(test_client, init_database):
    email = 'test@test.de'
    username = 'test'
    password = 'Saphira1010'
    response = test_client.post('/signup', data=dict(username=username, password=password, email=email),
                                follow_redirects=True)
    response = test_client.post(response.request.path, data=dict(username=username, password=password, email=email),
                                follow_redirects=True)
    user = User.query.filter_by(email=email).first()
    otp = pyotp.TOTP(user.mfasecretkey).now()
    response = test_client.post('/login', data=dict(username=username, password=password, email=email, otp=otp),
                                follow_redirects=True)
    response = test_client.post(response.request.path,
                                data=dict(username=username, password=password, email=email, otp=otp),
                                follow_redirects=True)
    assert response.request.path == '/profile'


def create_test_user():
    # create Test-User
    new_user = user_datastore.create_user(username='test', email='test@test.de', password='Saphira1010',
                                          roles=['end-user'], mfasecretkey='F4NI4XX2OME5P6MMQVRMFN7MYPG3YZNA')
    return new_user


def login_test_user(test_client, user, password='Saphira1010'):
    otp = pyotp.TOTP(user.mfasecretkey).now()
    # User logs in
    response2 = test_client.post('/login',
                                 data=dict(username=user.username, password=password, email=user.email),
                                 follow_redirects=True)
    # User enters his MFA-Token
    response2 = test_client.post('/login/mfa',
                                 data=dict(otp=otp), follow_redirects=True)
