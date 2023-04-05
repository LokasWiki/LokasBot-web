import configparser
import os

import click
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

home_path = os.path.expanduser("~")

""""
config.ini example

[mysql]
username=your_username
password=your_password
host=your_host
port=your_port
database=your_database
[ai_api]
key = my_key
url= ai_flask_url
"""

config_path = os.path.join(home_path, 'config1.ini')

# Read the configuration file
config = configparser.ConfigParser()
config.read(config_path)

# Get the MySQL connection details from the configuration file
username = config.get('mysql', 'username')
password = config.get('mysql', 'password')
host = config.get('mysql', 'host')
port = config.get('mysql', 'port')
database = config.get('mysql', 'database')

# Create the database engine
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}', echo=False)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)


def shutdown_session(exception=None):
    """If this request connected to the database, close the
    connection.
    """
    db_session.remove()


@click.command('init-db2')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(shutdown_session)
    app.cli.add_command(init_db_command)
