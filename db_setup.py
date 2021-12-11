import getpass
import os
import secrets

import datetime
from flask_security import hash_password

from app import create_app, user_datastore
from User import db, Airport, Plane, db_commit, Flight


def create_standard_admin():
    app = create_app()
    app.app_context().push()
    db.create_all()
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')
    print('Create Standard Admin')
    admin_username, admin_email, admin_password = get_admin_acc2()
    admin_password = hash_password(admin_password)
    user_datastore.create_user(username=admin_username, email=admin_email, password=admin_password, roles=['admin'])
    user_datastore.commit()
    create_data()


def create_data():
    app = create_app()
    app.app_context().push()
    airport1 = Airport(town='Stuttgart', country='Germany', iata='STR', name='Manfred Rommel Flughafen')
    airport2 = Airport(town='Bangkok', country='Thailand', iata='DMK', name='Suvarnabhumi International Airport ')
    airport3 = Airport(town='Pjöngjang', country='Nord-Korea', iata='FNJ', name='Sunan')
    airport4 = Airport(town='Peking', country='China', iata='PKX', name='Flughafen Peking-Daxing')
    airport5 = Airport(town='Palma', country='Spanien', iata='PMI', name='Palma de Mallorca')

    plane1 = Plane(planename='Boeing AH-64', seats='1')
    plane2 = Plane(planename='Eurofighter Typhoon', seats='1')
    plane3 = Plane(planename='R-7', seats='4')
    plane4 = Plane(planename='F-117 B Nighthawk', seats='1')
    plane5 = Plane(planename='NCC-1701-D', seats='430')

    flight1 = Flight(depAirport=airport1, arrAirport=airport1, depTime=datetime.datetime.utcfromtimestamp(1670597890),
                     arrTime=datetime.datetime.utcfromtimestamp(1670697890), plane=plane1, ticket_price=200)
    flight2 = Flight(depAirport=airport1, arrAirport=airport2, depTime=datetime.datetime.utcfromtimestamp(1672345513),
                     arrTime=datetime.datetime.utcfromtimestamp(1672545513), plane=plane2, ticket_price=3000)
    flight3 = Flight(depAirport=airport1, arrAirport=airport3, depTime=datetime.datetime.utcfromtimestamp(1670890213),
                     arrTime=datetime.datetime.utcfromtimestamp(1670990213), plane=plane3, ticket_price=9000)
    flight4 = Flight(depAirport=airport1, arrAirport=airport4, depTime=datetime.datetime.utcfromtimestamp(1670591234),
                     arrTime=datetime.datetime.utcfromtimestamp(1670791234), plane=plane4, ticket_price=300)
    flight5 = Flight(depAirport=airport1, arrAirport=airport5, depTime=datetime.datetime.utcfromtimestamp(1670593713),
                     arrTime=datetime.datetime.utcfromtimestamp(1670693713), plane=plane5, ticket_price=0)
    db_commit(airport1, airport2, airport3, airport4, airport5, plane1, plane2, plane3, plane4, plane5, flight1,
              flight2, flight3, flight4, flight5)


def get_admin_acc():
    print('Create Standard Admin')
    admin_username = input('Admin username:')
    admin_email = input('Admin email:')
    admin_password = getpass.getpass(prompt='Admin Password:', stream=None)
    return admin_username, admin_email, admin_password


def get_admin_acc2():
    return 'admin', 'admin@admin.de', '1234'


if __name__ == '__main__':
    create_standard_admin()
