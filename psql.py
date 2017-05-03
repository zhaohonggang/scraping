import psycopg2
from psycopg2.extensions import AsIs
from utils import *
'''
refresh('psql')
from psql import *

conn = psycopg2.connect(dsn)
conn = psycopg2.connect(dsn_raw_prod)
curs = conn.cursor()
curs.execute("SELECT 1 AS foo")
curs.execute("select * from house_raw where mls_number like '%test%'")
print(curs.fetchone())
from psycopg2.extensions import AsIs
curs.execute('INSERT INTO %s (%s, %s) VALUES (%s, %s)', (AsIs('article'), AsIs('article_name'), AsIs('article_desc'), 'test', 'test'))
curs.execute('INSERT INTO article (article_name, article_desc) VALUES (%s, %s)', ('test', 'test'))
conn.commit()



schema = 'INSERT INTO article (article_name, article_desc) VALUES (%s, %s)'
valuelists = [('a1','b1'),]
valuelists = [('a1','b1'),('a2','b2')]
PExec(dsn,schema,valuelists)
PExec(dsn_raw,"delete from raw",['1'])

schema = 'INSERT INTO article (article_name, article_desc) VALUES (%(article_name)s, %(article_desc)s)'

schema = 'INSERT INTO article (article_name, article_desc) VALUES (%(article_desc)s, %(article_name)s)'
valuelists = [{'article_name':'a1','article_desc':'b1'},{'article_name':'a2','article_desc':'b2'}]

valuelists = [{'article_name':'a1','0':'0000','article_desc':'b1'},{'article_name':'a2','article_desc':'b2'}]
PExec(dsn,schema,valuelists)
'''
'''
r = getParaFields('article_name, article_desc')
'''
def getParaFields(fields):
     return ','.join('%({0})s'.format(e.strip()) for e in fields.split(','))

'''
table='article'
fields = 'article_name, article_desc'
schema = buildInsertQuery('article','article_name, article_desc')
PExec(dsn,schema,valuelists):
'''

'''
InsertFromJsonFile('tmp/20170407/west.json', dsn, sold_table, sold_fields)
InsertFromJsonFile(open('tmp/20170406/0_0.json', 'r'), dsn_raw, sold_table, sold_fields)
InsertFromJsonFile('tmp/20170406/0_0aaaa.json', dsn_raw, sold_table, sold_fields)
'''
def InsertFromJsonFile(file, dsn, table, fields):
    valuelists = LogExp(readJson, file)
    schema = buildInsertQuery(table, fields)
    log('inserting {0}'.format(file))
    PExec(dsn,schema,valuelists)

'''
InsertFromJsonFolder('tmp/20170407/', dsn_raw, sold_table, sold_fields)
'''
def InsertFromJsonFolder(folder, dsn, table, fields):
    runFolder(InsertFromJsonFile, folder, '.json', dsn, table, fields)

def buildInsertQuery(table, fields):
    schema = 'INSERT INTO {table} ({fields}) values ({parafields})'
    d = {'table':table, 'fields':fields, 'parafields':getParaFields(fields)}
    return schema.format(**d)

def PExec(dsn,schema,valuelists):
    try:
        with psycopg2.connect(dsn) as conn:
            curs = conn.cursor()
            for vl in valuelists:
                try:
                    curs.execute(schema,vl)
                except Exception as e: 
                    log(str(e))
            conn.commit()
    except Exception as e: 
        log(str(e))

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

