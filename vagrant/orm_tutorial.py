# Version Check
import sqlalchemy
sqlalchemy.__version__


# Connecting (to a memory only database)
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)


# Declare a Mapping
# Describe database tables, and define classes to map to those tables
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        # Optional method, returns nicely formated item
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)


# Create a Schema
# Returns info about table. Table object is a member of the MetaData collection.
User.__table__

# Creates the table in database
Base.metadata.create_all(engine)


# Create an Instance of the Mapped Class
ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
ed_user.name  # prints 'ed'
ed_user.password  # prints 'edspassword'
str(ed_user.id)  # prints 'None', not added to table. Currently is transient.


# Creating a Session
# ORM's "handle" to the database is the Session, which talks to the DB.
# Define a Session class which will serve as a factory for new Session objects
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


# Adding and Updating Objects (To persist an object, add() it to a Session)
session.add(ed_user)  # instance is now currently pending

# Query
our_user = session.query(User).filter_by(name='ed').first()
our_user  # Returns <User(name='ed', fullname='Ed Jones', password...)>

ed_user is our_user  # Prints True

# Add multiple objects using add_all()
session.add_all([
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')])

# Update row
ed_user.password = 'f8s7css'

# Session knows 'Ed Jones' has been modified
session.dirty  # Returns IdentitySet([<User(name='ed', fullname...)>])

# Session also knows 3 users are pending
session.new  # Returns IdentitySet([<User>, <User>, <User>])

session.commit()  # Commits all changes to database

ed_user.id  # Returns 1 now as it is now in the database. Now persistent.


# Rolling Back (transactions made in session)
ed_user.name = 'Edwardo'
fake_user = User(name='fakeuser', fullname='Invalid', password='12345')
session.add(fake_user)

# Query will see they're flushed into current transaction (returns both users)
session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()

session.rollback()
ed_user.name  # Prints 'ed'
fake_user in session  # Prints False

# Since rollback, only 'ed' is returned
session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all()


# Querying
# Iterating through User objects:
for instance in session.query(User).order_by(User.id):
    print(instance.name, instance.fullname)
    # prints ed Ed Jones \n wendy Wendy Williams...

# Query also accepts ORM instrumented descriptors as arguments
for name, fullname in session.query(User.name, User.fullname):
    print(name, fullname)
    # prints ed Ed Jones \n wendy Wendy Williams...

# Tuples returned by query can be treated like tuples in Python
# Names are same as attributes and class...
for row in session.query(User, User.name).all():
    print(row.User, row.name)
    # prints <User(name='...')> ed, <User(name='...')> wendy, ...

# Can custom label() columns
for row in session.query(User.name.label('name_label')).all():
    print(row.name_label)

# Can alias tables as well
from sqlalchemy.orm import aliased
user_alias = aliased(User, name='user_alias')

for row in session.query(user_alias, user_alias.name).all():
    print(row.user_alias)
    # prints <User(name='...')>, ...

# OFFSET AND LIMIT are established by using Python's array slices
for u in session.query(User).order_by(User.id)[1:3]:
    print(u)
    # prints "<User(name='wendy')..>, <User(name='mary')...>"

# Filtering using keyword arguments - filter_by():
for name in session.query(User.name).filter_by(fullname='Ed Jones'):
    print(name)  # Prints ed

# Filtering using flexible SQL expression language constructs. Can use
# Python operators with class-level attributes on mapped classes
for name in session.query(User.name).filter(User.name == 'Ed Jones'):
    print(name)  # Prints ed

# Chaining Filters: Query object is fully generative. Next example
# looks for users named "ed" with a full name of "Ed Jones"
for user in session.query(User).\
        filter(User.name == 'ed').\
        filter(User.fullname == 'Ed Jones'):
    print(user)
    # prints <User(name='ed', fullname='Ed Jones')>


# Querying 1.1: Common Filters
# Here's a rundown of some of the most common operators used in filter():

# EQUALS:
# query.filter(User.name == 'ed')

# NOT EQUALS:
# query.filter(User.name != 'ed')

# LIKE:
# query.filter(User.name.like('%ed%'))

# IN:
# query.filter(User.name.in_(['ed', 'wendy', 'jack']))

# works with query objects too:
# query.filter(User.name.in_(
#         session.query(User.name).filter(User.name.like('%ed%'))
# ))

# NOT IN:
# query.filter(~User.name.in_(['ed', 'wendy', 'jack']))

# IS NULL:
# query.filter(User.name == None)

# alternatively, if pep8/linters are a concern
# query.filter(User.name.is_(None))

# IS NOT NULL:
# query.filter(User.name != None)

# alternatively, if pep8/linters are a concern
# query.filter(User.name.isnot(None))

# AND:
# use and_()
# from sqlalchemy import and_
# query.filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))

# or send multiple expressions to .filter()
# query.filter(User.name == 'ed', User.fullname == 'Ed Jones')

# or chain multiple filter()/filter_by() calls
# query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')

# Note: Make sure you use and_() and not the Python and operator!

# OR:
# from sqlalchemy import or_
# query.filter(or_(User.name == 'ed', User.name == 'wendy'))

# Note
# Make sure you use or_() and not the Python or operator!

# MATCH:
# query.filter(User.name.match('wendy'))

# Note: match() uses a database-specific MATCH or CONTAINS function; its
# behavior will vary by backend and is not available on some backends (SQLite).


## Querying 1.2: Returning Lists and Scalars
query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)

# all() returns a list
query.all()

# first()
query.first()

# one(). Fully fetches all rows. If multiple or no results round, it returns
# errors. Great for checking if more than one or no results found.
# user = query.filter(User.id == 99).one()

# one_or_none() like one(), but it no results found, doesn't return error.
# It returns None. Does raise error for multiple results

# scalar() invokes one() method, and returns the FIRST column of the row
query = session.query(User.id).filter(User.name == 'ed').\
    order_by(User.id)
query.scalar()  # Returns the id of 1


# Querying 1.3: Using Textual SQL
# Can use text() to specify string based SQL
from sqlalchemy import text
for user in session.query(User).filter(text("id<224")).\
        order_by(text("id")).all():
    print(user.name)

# Can bind parameters using colon and params() method
session.query(User).filter(text("id<:value and name=:name")).\
    params(value=224, name='fred').order_by(User.id).one()

# Can use full string-based statements using from_statement() method
session.query(User).from_statement(
    text("SELECT * FROM users WHERE name=:name")).\
    params(name='ed').all()

# Can match columns on name when dealing with complex queries where
# columns have the same names, etc. Note the first two lines which map it out
# stmt = text("SELECT name, id, fullname, password "
#             "FROM users WHERE name=:name")
# stmt = stmt.columns(User.name, User.id, User.fullname, User.password)
# session.query(User).from_statement(stmt).params(name='ed').all()


# Querying 1.4: Counting
# count() returns number of rows from SQL statment
session.query(User).filter(User.name.like('%ed')).count()  # 2

# To count something specifically, use func.count() method
# Below counts user name grouped by:
from sqlalchemy import func
session.query(func.count(User.name), User.name).group_by(User.name).all()
# Returns [(1, u'ed'), (1, u'fred'), (1, u'mary'), (1, u'wendy')]

# For SELECT COUNT(*) FROM table:
session.query(func.count('*')).select_from(User).scalar()  # 4

# Can remove select_from() method if express count in terms of primary key
session.query(func.count(User.id)).scalar()  # 4


# Building a Relationship
# Create a second table 'addresses', where each user from the 'users' table
# can have multiple addresses, creating a ONE TO MANY RELATIONSHIP for users
# to addresses due to the foreign key use
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Create a user attribute linking to User class
    # back_populate refers to the complementary attribute names
    # (in User here), determining Address.user will be a MANY TO ONE
    # back_populate creates a bidirectional relationship...
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s'>" % self.email_address

# Establish relationship attribute for User class, back_populating to
# Address relationship attribute mentioned above. ONE TO MANY
User.addresses = relationship(
    "Address", order_by=Address.id, back_populates='user')

# Create addresses table in the database
Base.metadata.create_all(engine)


# Working with Related Objects
jack = User(name='jack', fullname='Jack Bean', password='gjffdd')
jack.addresses  # Returns []

jack.addresses = [
    Address(email_address='jack@google.com'),
    Address(email_address='j25@yahoo.com')]

# Bidirectional relationship in use. Elements are visible to each other:
jack.addresses[1]  # <Address(email_address='j25@yahoo.com')>
jack.addresses[1].user
# <User(name='jack', fullname='Jack Bean', password='gjffdd')>

# By adding jack, we also add 2 new address members also. This is called
# CASCADING
session.add(jack)
session.commit()

jack = session.query(User).filter_by(name='jack').one()
jack  # Doesn't return addresses, only <User...>

jack.addresses  # Returns addresses collection (lazy loading)


# Query with Joins
# Using Filter
for u, a in session.query(User, Address).\
        filter(User.id == Address.user_id).\
        filter(Address.email_address == 'jack@google.com').all():
    print(u)  # <User(name='jack', fullname='Jack Bean', password='gjffdd')>
    print(a)  # <Address(email_address='jack@google.com')>

# Using join() method
# Query.join() knows how to join User and Address because there is only
# one foreign key between them
session.query(User).join(Address).\
    filter(Address.email_address == 'jack@google.com').\
    all()  # [<User(name='jack', fullname='Jack Bean', password='gjffdd')>]

# If NO or SEVERAL foreign keys, Query.join() works better when done as so:

# Explicit condition:
session.query(User).join(Address, User.id == Address.user_id).all()

# Specify relationship left to right
session.query(User).join(User.addresses).all()

# Specify relationship left to right with explicit target
session.query(User).join(Address, User.addresses).all()

# Specify relationship left to right using string of parameter
session.query(User).join('addresses').all()

# Using LEFT OUTER JOIN
session.query(User).outerjoin(User.addresses).all()

session.query(User.name, Address.email_address).\
    outerjoin(Address, User.id == Address.user_id).all()

# Counting emails per user (outerjoin)
from sqlalchemy import func
session.query(User, func.count(Address.email_address)).\
    outerjoin(Address, User.id == Address.user_id).group_by(User.name).all()


# Querying with Joins 1.2: Using Aliases
# Useful when using same table reference two or more times (addresses)
from sqlalchemy.orm import aliased
adalias1 = aliased(Address)
adalias2 = aliased(Address)
for username, email1, email2 in \
        session.query(User.name, adalias1.email_address, adalias2.email_address).\
        join(adalias1, User.addresses).\
        join(adalias2, User.addresses).\
        filter(adalias1.email_address == 'jack@google.com').\
        filter(adalias2.email_address == 'j25@yahoo.com'):
    print(username, email1, email2)


# Querying with Joins 1.3: Using Subqueries
# Example: Load User objects along with count of how many Address records each
# user has.
#
# The best way to generate SQL like this is to get the count of addresses
# grouped by user ids, and JOIN to the parent. In this case we use a
# LEFT OUTER JOIN so that we get rows back for those users who don't
# have any addresses, e.g.:
#  SELECT users.*, adr_count.address_count FROM users LEFT OUTER JOIN
#    (SELECT user_id, count(*) AS address_count
#        FROM addresses GROUP BY user_id) AS adr_count
#    ON users.id=adr_count.user_id

# First, create our subquery
from sqlalchemy import func
stmt = session.query(
    Address.user_id, func.count('*').label('address_count')).\
    group_by(Address.user_id).subquery()
# essentially creates (5, 2), 5 being the id of jack, who has 2 emails

# Once we have our statement, it behaves like a Table construct.
# Columns on the statement are accessed through an attribute called c:
for u, count in session.query(User, stmt.c.address_count).\
        outerjoin(stmt, User.id == stmt.c.user_id).order_by(User.id):
    print(u, count)
    # <User(name='ed')> None, .. , <User(name='jack')> 2


# Querying with Joins 1.4: Selecting entities from subqueries
# If we want our subquery to map to an entity, use aliased to associate an
# "alias" of a mapped class to a subquery:
stmt = session.query(Address).\
    filter(Address.email_address != 'j25@yahoo.com').subquery()
adalias = aliased(Address, stmt)

for user, address in session.query(User, adalias).join(adalias, User.addresses):
    print(user)
    print(address)
# <User name='jack'> and <Address email='jack@google.com'>


# Querying with Joins 1.5: Using EXISTS
# Returns True if given expression contains rows
# May be used in Joins and is useful for locating rows which don't have
# corresponding rows in a related table

# Explicit EXISTS construct:
from sqlalchemy.sql import exists
stmt = exists().where(Address.user_id == User.id)
for name in session.query(User.name).filter(stmt):
    print(name)  # jack

# Automatic use of exists using any()
for name in session.query(User.name).filter(User.addresses.any()):
    print(name)  # jack

# any() can take parameters to limit rows matched;
for name in session.query(User.name).\
        filter(User.addresses.any(Address.email_address.like('%google%'))):
    print(name)  # jack

# has() is same operator as any() for MANY-TO-ONE relationships. ~ means NOT
session.query(Address).\
    filter(~Address.user.has(User.name == 'jack')).all()


# Querying with Joins 1.6: Common Relationship Operators

# __eq__() (many-to-one equals comparision):
# query.filter(Address.user == someuser)

# __ne__() (many-to-one not equals comparision):
# query.filter(Address.user != someuser)

# IS NULL (many-to-one equals comparision):
# query.filter(Address.user == None)

# contains() (used for one-to-many collections):
# query.filter(User.addresses.contains(someaddress))

# any() (used for collections):
# query.filter(User.addresses.any(Address.email_address == 'bar'))

# has() (used for scalar references):
# query.filter(Address.user.has(name='ed'))

# Query.with_parent() (used for any relationship):
# session.query(Address).with_parent(someuser, 'addresses')


# Eager Loading (Reduces number of queries dramatically, like lazy load)
# 3 Types: 2 automatic, one involves custom criterion
# All three are usually invoked via functions known as query options which give
# additional instructions to the Query on how we would like various attributes
# to be loaded, via the Query.options() method.

# Eager Loading 1.1: Subquery Load
# Want User.addresses to load eagerly. Use orm.subqueryload(), which emits
# a second SELECT statement that fully loads the collections associated with
# the results just loaded

# subqueryload() is better for loading related collections (one-to-many)
from sqlalchemy.orm import subqueryload
jack = session.query(User).\
    options(subqueryload(User.addresses)).\
    filter_by(name='jack').one()
jack  # <User(name='jack'..)>
jack.addresses  # <Address(email_address='jack@google.com')>, <Address(...)>


# Eager Loading 1.2: Joined Load
# More well known, but older. orm.joinedload() emits a JOIN, LEFT OUTER JOIN by
# default, so the lead object and related object/collection are loaded in one
# step.

# joinedload() better suited for many-to-one relationships, as only ONE row is
# loaded for both the lead and related object
from sqlalchemy.orm import joinedload
jack = session.query(User).\
    options(joinedload(User.addresses)).\
    filter_by(name='jack').one()

# Even though OUTER JOIN resulted in 2 rows, we only got one instance of User
# back.
jack  # <User(name='jack'..)>
jack.addresses  # <Address(email_address='jack@google.com')>, <Address(...)>


# Eager Loading 1.3: Explicit Join + Eagerload
# Here we construct a JOIN explicitly to locate primary rows, and we want to
# apply the extra table to a related object or collection on the primary object.
# orm.contains_eager() useful for preloaded many-to-one object on a query
from sqlalchemy.orm import contains_eager
jacks_addresses = session.query(Address).\
    join(Address.user).\
    filter(User.name == 'jack').\
    options(contains_eager(Address.user)).all()
jacks_addresses  # <Address(email_address='jack@google.com')>, <Address(...)>
jacks_addresses[0].user  # <User(name='jack')>


# Deleting
# Deleting jack DOES NOT delete cascades (reference to addresses)
# user_id in Address will be set to NULL, but will still exist for jack!
jack = session.query(User).filter(User.name == 'jack').one()
session.delete(jack)
session.query(User).filter_by(name='jack').count()  # 0
session.query(Address).filter(
    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])).\
    count()  # 2


# Deleting 1.2: Configure Delete/Delete-Orphan Cascade
# Configure cascade options on User.addresses relationship
# Must start over using a new Base to do this and redefine mappings
session.close()  # Rollback

Base = declarative_base()


# Refine classes:
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    addresses = relationship(
        "Address", back_populates='user', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship(
        "User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s'>" % self.email_address

# Get jack using get() by id
jack = session.query(User).get(5)

# remove one Address (lazy load fires off)
del jack.addresses[1]

# only one remains
session.query(Address).filter(
    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])).\
    count()  # 1

# Delete Jack, delete orphans by default
session.delete(jack)

session.query(User).filter_by(name='jack').count()  # 0

session.query(Address).filter(
    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])).\
    count()  # 0


# Building a Many to Many Relationship
# Example: Users can write a BlogPost which can have Keyword items associated
# with it.
#
# For a PLAIN many-to-many, we need to create an UN-MAPPED Table to serve as an
# association table (with the IDs of the two items in a relationship). If there
# are any other columns such as primary key, or foreign keys to other tables,
# SQLAlchemy requires a different pattern to be used: "Association Object".
#
# For now, note the declaration is different (constructor):
from sqlalchemy import Table, Text

# association table
post_keywords = Table(
    'post_keywords', Base.metadata,
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
    Column('keyword_id', ForeignKey('keywords.id'), primary_key=True))


# Now define our BlogPost and Keyword classes, using relationship() constructs
# each referring to the post_keywords association table
class BlogPost(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    headline = Column(String(255), nullable=False)
    body = Column(Text)

    # many to many BlogPost<->Keyword
    keywords = relationship(
        'Keyword',
        secondary=post_keywords,
        back_populates='posts'
        )

    def __init__(self, headline, body, author):
        self.author = author
        self.headline = headline
        self.body = body

    def __repr__(self):
        return "BlogPost(%r, %r, %r" % (self.headline, self.body, self.author)


class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False)

    posts = relationship(
        'BlogPost',
        secondary=post_keywords,
        back_populates='keywords'
        )

    def __init__(self, keyword):
        self.keyword = keyword

# Would like our BlogPost class to have an author field. We'll do this as
# another bidirectional relationship, but the one issue is that a single user
# may have LOTS of blog posts. When we access User.posts, we'd like to filter
# results to as not to load the entire collection. For that, set the
# relationship() property of lazy='dynamic'
BlogPost.author = relationship(User, back_populates='posts')
User.posts = relationship(BlogPost, back_populates='author', lazy='dynamic')

# Create tables
Base.metadata.create_all(engine)

# Give Wendy blog posts
wendy = session.query(User).\
    filter_by(name='wendy').\
    one()

post = BlogPost("Wendy's Blog Post", "This is a test.", wendy)
session.add(post)

# We're storing keywords uniquely in the DB. We con't know any yet, so
# we'll just create some:
post.keywords.append(Keyword('wendy'))
post.keywords.append(Keyword('firstpost'))

# Look up blog posts with keyword 'firstpost'
session.query(BlogPost).\
    filter(BlogPost.keywords.any(keyword='firstpost')).\
    all()
    # Returns [BlogPost("Wendy's Blog Post", 'This is a test',
    # <User(name='wendy', fullname='Wendy Williams', password='foobar')>)]

# Or use Wendy's own posts relationship, which is a "dynamic" relationship:
wendy.posts.\
    filter(BlogPost.keywords.any(keyword='firstpost')).all()
