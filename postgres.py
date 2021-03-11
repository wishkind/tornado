import os
import sys
import psycopg2
  
def connectPostgreSQL():
    conn = psycopg2.connect(database="postgres", user="postgres", password="dragon", host="127.0.0.1", port="5432")
    print('connect successful!')
    cursor=conn.cursor()
    cursor.execute('''create table public.member(
                  id integer not null primary key,
                  name varchar(32) not null,
                  password varchar(32) not null,
                  singal varchar(128)
                  )''')
    conn.commit()
    conn.close()
    print('table public.member is created!')

def insertOperate():
    conn = psycopg2.connect(database="postgres", user="postgres", password="dragon", host="127.0.0.1", port="5432")
    cursor=conn.cursor()
    cursor.execute("insert into public.member(id,name,password,singal)\
               values(1,'member0','password0','signal0')")
    cursor.execute("insert into public.member(id,name,password,singal)\
               values(2,'member1','password1','signal1')")
    cursor.execute("insert into public.member(id,name,password,singal)\
               values(3,'member2','password2','signal2')")
    cursor.execute("insert into public.member(id,name,password,singal)\
               values(4,'member3','password3','signal3')")
    conn.commit()
    conn.close()
    
    print('insert records into public.memmber successfully')

def selectOperate():
    conn = psycopg2.connect(database="postgres", user="postgres", password="dragon", host="127.0.0.1", port="5432")
    cursor=conn.cursor()
    cursor.execute("select id,name,password,singal from public.member where id>2")
    rows=cursor.fetchall()
    for row in rows:
        print('id=',row[0], ',name=',row[1],',pwd=',row[2],',singal=',row[3],'\n')
    conn.close()

def updateOperate():
    conn = psycopg2.connect(database="postgres", user="postgres", password="dragon", host="127.0.0.1", port="5432")
    cursor=conn.cursor()
    cursor.execute("update public.member set name='update ...' where id=2")
    conn.commit()
    print("Total number of rows updated :", cursor.rowcount)

    cursor.execute("select id,name,password,singal from public.member")
    rows=cursor.fetchall()
    for row in rows:
        print('id=',row[0], ',name=',row[1],',pwd=',row[2],',singal=',row[3],'\n')
    conn.close()

def deleteOperate():
    conn = psycopg2.connect(database="postgres", user="postgres", password="dragon", host="127.0.0.1", port="5432")    
    cursor=conn.cursor()

    cursor.execute("select id,name,password,singal from public.member")
    rows=cursor.fetchall()
    for row in rows:
        print( 'id=',row[0], ',name=',row[1],',pwd=',row[2],',singal=',row[3],'\n')

        print('begin delete')
        cursor.execute("delete from public.member where id=2")
    conn.commit()   
    print('end delete')
    print("Total number of rows deleted :", cursor.rowcount)     
    cursor.execute("select id,name,password,singal from public.member")
    rows=cursor.fetchall()
    for row in rows:
        print('id=',row[0], ',name=',row[1],',pwd=',row[2],',singal=',row[3],'\n')
    conn.close()
     
if __name__=='__main__':
    #connectPostgreSQL()
    #insertOperate()
    #selectOperate()
    #updateOperate()
    deleteOperate()
