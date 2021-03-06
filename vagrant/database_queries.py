import datetime
import random
from random import randint

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from database_setup import Base, Shelter, Puppy, PuppyProfile, Adopter

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
    """Using the one-to-one relationship, get puppy name, gender, picture,
    description, special needs from the puppy and puppy_profile tables"""
    puppies = session.query(
        Puppy.name, Puppy.gender, PuppyProfile.picture,
        PuppyProfile.description, PuppyProfile.special_needs).\
        filter(Puppy.id == PuppyProfile.puppy_id).all()

    print "Get Puppies and correlating Puppy Profiles (One-to-One)"

    for puppy in puppies:
        print(
            puppy.name, puppy.gender, puppy.picture, puppy.description,
            puppy.special_needs)

    print "\n"


def setupManyToMany():
    """Setup many-to-many relationship between Adopter(s) and Pupp(ies)"""
    # Puppies: "Bailey", "Max", "Charlie", "Buddy", "Rocky", "Jake", "Jack"
    puppy_bailey = session.query(Puppy).filter_by(name='Bailey').first()
    puppy_max = session.query(Puppy).filter_by(name='Max').one()
    puppy_charlie = session.query(Puppy).filter_by(name='Charlie').one()
    puppy_buddy = session.query(Puppy).filter_by(name='Buddy').one()
    puppy_rocky = session.query(Puppy).filter_by(name='Rocky').one()
    puppy_jake = session.query(Puppy).filter_by(name='Jake').one()
    puppy_jack = session.query(Puppy).filter_by(name='Jack').one()

    adopter_james_smith = session.query(Adopter).\
        filter_by(first_name='James').one()
    adopter_maggie_smith = session.query(Adopter).\
        filter_by(first_name='Maggie').one()
    adopter_crazy_lady = session.query(Adopter).\
        filter_by(first_name='Crazy').one()

    # Add puppy to 2 adopters (same family)
    puppy_bailey.adopters.append(adopter_james_smith)
    puppy_bailey.adopters.append(adopter_maggie_smith)

    # Add several puppies to 1 adopter
    adopter_crazy_lady.puppies.append(puppy_max)
    adopter_crazy_lady.puppies.append(puppy_charlie)
    adopter_crazy_lady.puppies.append(puppy_buddy)
    adopter_crazy_lady.puppies.append(puppy_rocky)
    adopter_crazy_lady.puppies.append(puppy_jake)
    adopter_crazy_lady.puppies.append(puppy_jack)

    # Check many-to-many relationships
    print "Get Adopters of Bailey (Many-to-Many):"

    for a in puppy_bailey.adopters:
        print(a.first_name, a.last_name)

    print "\n"

    print "Get Puppies of Crazy Lady (Many-to-Many):"
    for p in adopter_crazy_lady.puppies:
        print(p.name)

    print "\n"

    # Using the any operator
    print "Get Puppies of Crazy Lady (Many-to-Many) Using any() operator:"
    crazy_query = session.query(Puppy).\
        filter(Puppy.adopters.any(first_name='Crazy')).all()

    for p in crazy_query:
        print(p, p.name)

    print "\n"


def createRandomAge():
    """ Make a random age for each puppy between 0-18 months(approx.)
        old from the day the algorithm was run."""
    today = datetime.date.today()
    days_old = randint(0, 540)
    birthday = today - datetime.timedelta(days=days_old)
    return birthday


def createRandomWeight():
    """Create a random weight between 1.0-40.0 pounds"""
    return random.uniform(1.0, 40.0)


def checkInPuppy(puppy_name, puppy_gender, puppy_dob, puppy_weight, shelter_id):
    """Check in puppy only if a shelter has vacancy """
    shelter = session.query(Shelter).get(shelter_id)

    if(shelter.current_occupancy >= shelter.maximum_capacity):
        print shelter.name + " is full. Trying another shelter..."

        shelter = session.query(Shelter).\
            filter(Shelter.current_occupancy < Shelter.maximum_capacity).\
            order_by(Shelter.current_occupancy).first()

        if(shelter is None):
            print "All shelters are full. Please open more shelters."
            return False

    new_puppy = Puppy(
        name=puppy_name, gender=puppy_gender, dateOfBirth=puppy_dob,
        shelter_id=shelter.id, weight=puppy_weight)
    session.add(new_puppy)
    session.commit()

    new_profile = PuppyProfile(
        picture="No image",
        description="No description",
        special_needs="No needs",
        puppy_id=new_puppy.id)

    shelter.current_occupancy = shelter.current_occupancy + 1

    session.add(new_profile)
    session.commit()

    print(new_puppy.name + " has been placed in " + shelter.name)


def checkInPuppies():
    """Scenarios to check current_occupancy and maximum_capcity of shelters"""

    print "Check in a dog. Should be checked in the next available shelter."
    checkInPuppy("Rexford", "male", createRandomAge(), createRandomWeight(), 2)
    print "\n"

    print "Check in a dog in an already full facility"
    checkInPuppy("Test1", "male", createRandomAge(), createRandomWeight(), 2)
    print session.query(exists().where(Puppy.name == "Test1")).scalar()  # False
    print "\n"


def adoptPuppy(puppy_id, adopters_list):
    """Adopt a puppy based on id. Remove it from shelter occupancy"""
    puppy = session.query(Puppy).get(puppy_id)

    if(len(puppy.adopters) > 0):
        print "%s is already adopted!" % puppy.name
        return puppy

    for a_id in adopters_list:
        adopter = session.query(Adopter).get(a_id)
        puppy.adopters.append(adopter)

    shelter = session.query(Shelter).get(puppy.shelter_id)
    shelter.current_occupancy = shelter.current_occupancy - 1

    session.commit()

    return puppy


def checkAdoptPuppies():
    id_1 = 8

    # Check shelter occupancies before:
    stmt_1 = session.query(Puppy.shelter_id.label('s_id')).\
        filter(Puppy.id == id_1).\
        subquery()
    shelter_1 = session.query(Shelter).\
        filter(Shelter.id == stmt_1.c.s_id).one()

    print("%s has an current occupancy of %s" % (
        shelter_1.name, shelter_1.current_occupancy))

    # Have Mr. and Mrs. Smith adopt another puppy
    puppy_1 = adoptPuppy(id_1, [1, 2])

    # Check shelter occupancies afterwards:
    print "Get Adopters of puppy_1:"

    for a in puppy_1.adopters:
        print(a.first_name, a.last_name)

    print "\n"

    print("After %s's adoption, %s has an current occupancy of %s" % (
        puppy_1.name, shelter_1.name, shelter_1.current_occupancy))


def executeQueries():
    # sortAscendingName()
    # sortLessthanSixMonthsOld()
    # sortAscendingWeight()
    # groupByShelter()
    # getPuppyAndProfile()
    # setupManyToMany()
    checkInPuppies()
    # checkAdoptPuppies()

executeQueries()
