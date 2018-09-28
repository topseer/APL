# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 17:44:58 2018

@author: Yang
"""

from bs4 import BeautifulSoup 
import pandas as pd

# prepare the table 

import sqlite3
from sqlite3 import Error

conn = sqlite3.connect("hurricanes.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Hurricanes;")
cur = conn.cursor()
cur.execute("""
            create table Hurricanes 
            (Year text, 
            tropical_storms text,
            hurricanes text, 
            major_hurricanes text, 
            deaths text,
            damage text,
            notes text)
            """
            )
conn.commit()
cur.close()
conn.close()



soup = BeautifulSoup( open("Atlantic hurricane season - Wikipedia.html",'r',encoding='utf-8'), "html.parser")
    
tables = soup(['table'])

for t,table in enumerate(tables): 
 
    headers = [header.text.replace("\n","") for header in table.find_all('th')]
    
    print (headers)
    rows = []
    df_ = pd.DataFrame(columns=headers)
    
    conn = sqlite3.connect("hurricanes.db")
    for i,row in enumerate(table.find_all('tr')):
        rows.append( [ str(val.text.encode('utf8')) for val in row.find_all('td')])
        #rows.append( [val.text.encode('utf8') for val in row.find_all('td')])
        rows[i] = [x.replace("b'","") for x in rows[i]]
        rows[i] = [x.replace('b"',"") for x in rows[i]]
        rows[i] = [x.replace('\\n"',"") for x in rows[i]]
        rows[i] = [x.replace("\\n'","") for x in rows[i]]
        rows[i] = [x.replace("'","") for x in rows[i]]
        rows[i] = [x.replace("\\xe2\\x80\\x93","-") for x in rows[i]]
        rows[i] = [x.replace("\\xe2\\x80\\xa2","-") for x in rows[i]]      
        rows[i] = [x.replace("\\xe2\\x89\\xa5",">=") for x in rows[i]]      
        rows[i] = [x.replace("\\xc2\\xa0"," ") for x in rows[i]]      

          
        if i>=1:
            df_.loc[i] = rows[i]
        
            year= stroms = hurricanes = mhurricanes =  deaths = damage = notes = ""    
            if "Year" in df_: year = str(df_.loc[:,'Year'][i])     
            if "Number oftropical storms" in df_: stroms = str(df_.loc[:,'Number oftropical storms'][i])     
            if "Number ofhurricanes" in df_: hurricanes = str(df_.loc[:,'Number ofhurricanes'][i])     
            if "Number ofmajor hurricanes" in df_: mhurricanes = str(df_.loc[:,'Number ofmajor hurricanes'][i]) 
            if "Deaths" in df_: deaths = str(df_.loc[:,'Deaths'][i]) 
            if "DamageUSD" in df_: damage = str(df_.loc[:,'DamageUSD'][i]) 
            if "Notes" in df_: notes = str(df_.loc[:,'Notes'][i]) 
            new_row = [year,stroms , hurricanes ,mhurricanes ,  deaths , damage , notes]
            
            sql = "insert into Hurricanes values ({0})".format(str(new_row)).replace('[','').replace("]","")
            cur = conn.cursor()
            cur.execute(sql)
            print( sql )
            conn.commit()
            
    conn.close()
    



conn = sqlite3.connect("hurricanes.db")

df = pd.read_sql_query("select * from Hurricanes;", conn)

conn.close()

#from sqlalchemy import create_engine

#engine = create_engine('sqlite:///hurricanes.db', echo=False)