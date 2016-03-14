# Uda County Puppy Adoption Database Schema

**Uda County Puppy Adoption Database Schema** is a database schema used to store puppies and shelter information. This project is written in [Python](https://www.python.org), [SQLAlchemy](http://sqlalchemy.org) and [SQLite](https://www.sqlite.org).

This is a project for the lovely folks at [Udacity](https://www.udacity.com), submitted for review by [Rupert Ong](http://twitter.com/rupertong), who is completing the Fullstack Web Developer Nanodegree.


## Table of contents

* [Quick start](#quick-start)
* [What's included](#whats-included)
* [Contributors](#contributors)
* [Copyright and license](#copyright-and-license)


## Quick start

Here's what you need to do to view this project:

1. Install [Vagrant](https://www.vagrantup.com) and [VirtualBox](https://www.virtualbox.org).
2. Within Terminal (Mac), navigate to the vagrant folder and launch the Vagrant VM by running the command `vagrant up`.
3. SSH into the running Vagrant machine `vagrant ssh`. 
4. Execute `cd /vagrant` to change directory.
5. Run `python database_setup.py` to create database.
6. Run `python puppypopulator.py` to populate database.
7. Finally, run `python database_queries.py` to run the related queries. Be sure to comment and uncomment methods as needed.


## What's included

Within the downloaded files, this is the relevant structure:

```
uda-county-puppy-adoption/
└── vagrant/
    ├── Vagrantfile
    ├── database_queries.py
    ├── database_setup.py
    ├── puppypopulator.py
    └── pg_config.sh
```


## Contributors

**Rupert Ong**

* <https://twitter.com/rupertong>
* <https://github.com/rupert-ong>


## Copyright and license

Code and documentation copyright 2011-2016 Udacity Inc. All rights reserved.
