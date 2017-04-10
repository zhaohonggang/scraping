import psycopg2
from psycopg2.extensions import AsIs
'''
conn = psycopg2.connect(dsn)
curs = conn.cursor()
curs.execute("SELECT 1 AS foo")

print curs.fetchone()
from psycopg2.extensions import AsIs
curs.execute('INSERT INTO %s (%s, %s) VALUES (%s, %s)', (AsIs('article'), AsIs('article_name'), AsIs('article_desc'), 'test', 'test'))
curs.execute('INSERT INTO article (article_name, article_desc) VALUES (%s, %s)', ('test', 'test'))
conn.commit()

from psql import PExec

schema = 'INSERT INTO article (article_name, article_desc) VALUES (%s, %s)'
valuelists = [('a1','b1'),]
valuelists = [('a1','b1'),('a2','b2')]
PExec(dsn,schema,valuelists)
PExec(dsn_raw,"delete from raw",['1'])


'''
def PExec(dsn,schema,valuelists):
    try:
        with psycopg2.connect(dsn) as conn:
            curs = conn.cursor()
            for vl in valuelists:
                try:
                    curs.execute(schema,vl)
                except Exception as e: 
                    print(str(e))
            conn.commit()
    except Exception as e: 
        print(str(e))

'''
from psql import *
r =  PGet(dsn,'select * from article')
r =  PGet(dsn_raw,'select id from house_id_temp')
'''
def PGet(dsn,schema,value = ''):
    try:
        with psycopg2.connect(dsn) as conn:
            curs = conn.cursor()
            curs.execute(schema,value)
            rows = curs.fetchall()
            return rows
    except Exception as e: 
        print(str(e))

