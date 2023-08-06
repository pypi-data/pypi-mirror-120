
from app import db, migrate
from .models import ExampleModel

'''
    bws migrate main__create_table
'''

@migrate.command
def main__create_table():
    return ExampleModel.__table__.create(db.get_engine())

