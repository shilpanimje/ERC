#!/usr/bin/python3
import  pymysql
import config
from contextlib import contextmanager

# Open database connection
db = pymysql.connect(
    config.mysql['host'],
    config.mysql['user'],
    config.mysql['passward'],
    config.mysql['db']
)

@contextmanager
def dbSession():
    """Provide a transactional scope around a series of operations.
    This handles rollback and closing of db session, so there is no need
    to do that throughout the code.
    Usage:
        with dbSession() as cursor:
            cursor.execute(query)
    """

    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    try:
        yield cursor
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


def prepare_query(query, params)
    
