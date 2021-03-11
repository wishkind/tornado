# -*- coding: utf-8 -*-
import pymysql.connections
import pymysql.converters
import pymysql.cursors
pymysql.install_as_MySQLdb()
import MySQLdb

from datetime import datetime
from sqlalchemy import Table, create_engine, MetaData, select, func



engine = create_engine('postgresql+psycopg2://postgresql:dragon@localhost/postgresql')


#engine = create_engine('postgresql+pg8000://postgresql:dragon@localhost/postgresql')
