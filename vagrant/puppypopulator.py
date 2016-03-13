from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Shelter, Puppy, PuppyProfile, Adopter
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random

engine = create_engine('sqlite:///puppyshelter.db', echo=True)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


#Add Shelters
shelter1 = Shelter(name="Oakland Animal Services", address="1101 29th Ave", city="Oakland", state="California", zipCode="94601", website="oaklandanimalservices.org", current_occupancy=0, maximum_capacity=31)
session.add(shelter1)

shelter2 = Shelter(name="San Francisco SPCA Mission Adoption Center", address="250 Florida St", city="San Francisco", state="California", zipCode="94103", website="sfspca.org", current_occupancy=0, maximum_capacity=15)
session.add(shelter2)

shelter3 = Shelter(name="Wonder Dog Rescue", address="2926 16th Street", city="San Francisco", state="California", zipCode="94103", website="http://wonderdogrescue.org", current_occupancy=0, maximum_capacity=20)
session.add(shelter3)

shelter4 = Shelter(name="Humane Society of Alameda", address="PO Box 1571", city="Alameda", state="California", zipCode="94501", website="hsalameda.org", current_occupancy=0, maximum_capacity=15)
session.add(shelter4)

shelter5 = Shelter(name="Palo Alto Humane Society", address="1149 Chestnut St.", city="Menlo Park", state="California", zipCode="94025", website="paloaltohumane.org", current_occupancy=0, maximum_capacity=20)
session.add(shelter5)


#Add Puppies

male_names = ["Bailey", "Max", "Charlie", "Buddy", "Rocky", "Jake", "Jack", "Toby", "Cody", "Buster", "Duke", "Cooper", "Riley", "Harley", "Bear", "Tucker", "Murphy", "Lucky", "Oliver", "Sam", "Oscar", "Teddy", "Winston", "Sammy", "Rusty", "Shadow", "Gizmo", "Bentley", "Zeus", "Jackson", "Baxter", "Bandit", "Gus", "Samson", "Milo", "Rudy", "Louie", "Hunter", "Casey", "Rocco", "Sparky", "Joey", "Bruno", "Beau", "Dakota", "Maximus", "Romeo", "Boomer", "Luke", "Henry"]

female_names = ['Bella', 'Lucy', 'Molly', 'Daisy', 'Maggie', 'Sophie', 'Sadie', 'Chloe', 'Bailey', 'Lola', 'Zoe', 'Abby', 'Ginger', 'Roxy', 'Gracie', 'Coco', 'Sasha', 'Lily', 'Angel', 'Princess', 'Emma', 'Annie', 'Rosie', 'Ruby', 'Lady', 'Missy', 'Lilly', 'Mia', 'Katie', 'Zoey', 'Madison', 'Stella', 'Penny', 'Belle', 'Casey', 'Samantha', 'Holly', 'Lexi', 'Lulu', 'Brandy', 'Jasmine', 'Shelby', 'Sandy', 'Roxie', 'Pepper', 'Heidi', 'Luna', 'Dixie', 'Honey', 'Dakota']

puppy_images = ["http://pixabay.com/get/da0c8c7e4aa09ba3a353/1433170694/dog-785193_1280.jpg?direct", "http://pixabay.com/get/6540c0052781e8d21783/1433170742/dog-280332_1280.jpg?direct", "http://pixabay.com/get/8f62ce526ed56cd16e57/1433170768/pug-690566_1280.jpg?direct", "http://pixabay.com/get/be6ebb661e44f929e04e/1433170798/pet-423398_1280.jpg?direct", "http://pixabay.com/static/uploads/photo/2010/12/13/10/20/beagle-puppy-2681_640.jpg", "http://pixabay.com/get/4b1799cb4e3f03684b69/1433170894/dog-589002_1280.jpg?direct", "http://pixabay.com/get/3157a0395f9959b7a000/1433170921/puppy-384647_1280.jpg?direct", "http://pixabay.com/get/2a11ff73f38324166ac6/1433170950/puppy-742620_1280.jpg?direct", "http://pixabay.com/get/7dcd78e779f8110ca876/1433170979/dog-710013_1280.jpg?direct", "http://pixabay.com/get/31d494632fa1c64a7225/1433171005/dog-668940_1280.jpg?direct"]

puppy_descriptions = [
	"Easy going dog with a good temperament.", "Feisty but friendly.",
	"Great with children.", "Whiny and annoying.", "Large dog with a big heart.",
	"Playful daschund who takes on more than it can chew.", "Small chihuahua", 
	"Exciting Boxer who has lots of love to give", "Crazy Terrier who will destroy your furniture.",
	"Dalmation who loves to walk!"]

puppy_special_needs = [
	"Lots of room to walk", "Plenty of exercise", "Restricted diet",
	"Large bed and plenty of food", "Veterinary shots daily", "None"]


# This method will make a random age for each puppy between 0-18 months(approx.)
# old from the day the algorithm was run.
def CreateRandomAge():
	today = datetime.date.today()
	days_old = randint(0, 540)
	birthday = today - datetime.timedelta(days=days_old)
	return birthday


# This method will create a random weight between 1.0-40.0 pounds (or whatever
# unit of measure you prefer)
def CreateRandomWeight():
	return random.uniform(1.0, 40.0)


# Create Puppies (First Way)
def CreatePuppies():
	for i, x in enumerate(male_names):
		new_puppy = Puppy(
			name=x, gender="male", dateOfBirth=CreateRandomAge(),
			picture=random.choice(puppy_images), shelter_id=randint(1, 5),
			weight=CreateRandomWeight())
		session.add(new_puppy)
		session.commit()

	for i, x in enumerate(female_names):
		new_puppy = Puppy(
			name=x, gender="female", dateOfBirth=CreateRandomAge(), 
			picture=random.choice(puppy_images), shelter_id=randint(1, 5),
			weight=CreateRandomWeight())
		session.add(new_puppy)
		session.commit()


# Convenience method for Puppy, PuppyProfile population
def EnumeratePuppies(names_list, start_num=1, gender_type="male"):
	for i, x in enumerate(names_list, start=start_num):
		# Get shelter_id and check if current_occupancy is less than
		# maximum_capacity
		random_shelter_id = randint(1, 5)
		shelter = session.query(Shelter).get(random_shelter_id)

		if(shelter.current_occupancy >= shelter.maximum_capacity):
			print(shelter.name + " is full. Trying another shelter...")

			shelter = session.query(Shelter).\
				filter(Shelter.current_occupancy < Shelter.maximum_capacity).\
				order_by(Shelter.current_occupancy).first()

			if(shelter is None):
				print "All shelters are full. Please open more shelters."
				break

		if(shelter is None):
			return False

		new_puppy = Puppy(
			name=x, gender=gender_type, dateOfBirth=CreateRandomAge(),
			shelter_id=randint(1, 5), weight=CreateRandomWeight())
		new_profile = PuppyProfile(
			picture=random.choice(puppy_images),
			description=random.choice(puppy_descriptions),
			special_needs=random.choice(puppy_special_needs),
			puppy_id=i)
		shelter.current_occupancy = shelter.current_occupancy + 1

		session.add_all([new_puppy, new_profile])
		session.commit()


# Create Puppy and PuppyProfile instances (one-to-one relationship)
def CreatePuppiesAndProfiles():
	EnumeratePuppies(male_names)
	EnumeratePuppies(female_names, 50, "female")


# Create Adopters (many-to-many relationship with Puppy)
def CreateAdopters():
	james_smith = Adopter("James", "Smith")
	maggie_smith = Adopter("Maggie", "Smith")
	crazy_dog_lady = Adopter("Crazy", "Lady")
	session.add_all([james_smith, maggie_smith, crazy_dog_lady])
	session.commit()

CreatePuppiesAndProfiles()
CreateAdopters()
