import datetime

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Shelter, Puppy

engine = create_engine('sqlite:///puppyshelter.db', echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def sortAscendingName():
    """Query all puppies and return the results in ascending alphabetical order"""
    puppies = session.query(Puppy).order_by(Puppy.name).all()

    print "Sort Puppies by name alphabetically: \n"

    for puppy in puppies:
        print(puppy.id, puppy.name)

    print "\n"


def sortLessthanSixMonthsOld():
    """Query all puppies that are less than six months old, sorted youngest to oldest"""
    today = datetime.date.today()
    six_months_ago = today - datetime.timedelta(180)

    puppies = session.query(Puppy).filter(Puppy.dateOfBirth > six_months_ago).order_by(desc(Puppy.dateOfBirth)).all()

    print "Sort Puppies less than 6 months old, youngest to oldest: \n"

    for puppy in puppies:
        print(puppy.id, puppy.name, puppy.dateOfBirth)

    print "\n"


def sortAscendingWeight():
    """Query all puppies and return by ascending weight"""
    puppies = session.query(Puppy).order_by(Puppy.weight).all()

    print "Sort Puppies by weight ascending \n"

    for puppy in puppies:
        print(puppy.id, puppy.name, puppy.weight)

    print "\n"


def executeQueries():
    #sortAscendingName()
    # sortLessthanSixMonthsOld()
    sortAscendingWeight()

executeQueries()
