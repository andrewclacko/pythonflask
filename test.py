import psycopg2
import sys
 
#connectionstring = "postgresql://postgres:postgres@pythonflask.eastus.cloudapp.azure.com:5432/costs"
con = "postgresql://postgres:postgres@pythonflask.eastus.cloudapp.azure.com:5432/testdb"
 
try:
    con = psycopg2.connect("host='postgres:postgres@pythonflask.eastus.cloudapp.azure.com' dbname='testdb' user='pythonspot' password='popythonspotstgres'")  
    cur = con.cursor()
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username text, password text)")
    cur.execute("INSERT INTO Products VALUES(1,'jose','asdf')")
    con.commit()

# except psycopg2.DatabaseError, e:
#     if con:
#         con.rollback()
 
    # print 'Error %s' % e    
    # sys.exit(1)
 
finally:   
    if con:
        con.close()