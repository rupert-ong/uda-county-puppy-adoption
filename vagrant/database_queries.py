import datetime

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Shelter, Puppy, PuppyProfile

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

    puppies = session.query(Puppy).filter(Puppy.dateOfBirth > six_months_ago).\
        order_by(desc(Puppy.dateOfBirth)).all()

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


def groupByShelter():
    """Query all puppies and group by shelter name"""
    puppies = session.query(
        Puppy.name.label('puppy_name'), Shelter.name.label('shelter_name')).\
        filter(Puppy.shelter_id == Shelter.id).order_by(Shelter.name, Puppy.name)

    print "Sort Puppies by shelter name ascending \n"

    for puppy in puppies:
        print(puppy.puppy_name, puppy.shelter_name)

    print "\n"


def getPuppyAndProfile():
    """Using the one-to-one relationship, get puppy name, gender, image,
    description, special needs from the puppy and puppy_profile tables"""
    puppies = session.query(
        Puppy.name, Puppy.gender, PuppyProfile.image, PuppyProfile.description,
        PuppyProfile.special_needs).\
        filter(Puppy.id == PuppyProfile.puppy_id).all()

    print "Get Puppies and correlating Puppy Profiles (One-to-One)"

    for puppy in puppies:
        print(
            puppy.name, puppy.gender, puppy.image, puppy.description,
            puppy.special_needs)

    print "\n"


def executeQueries():
    # sortAscendingName()
    # sortLessthanSixMonthsOld()
    # sortAscendingWeight()
    # groupByShelter()
    getPuppyAndProfile()

executeQueries()
