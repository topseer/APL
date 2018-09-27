# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 17:44:58 2018

@author: Yang
"""

from bs4 import BeautifulSoup 
import pandas as pd

soup = BeautifulSoup( open("Atlantic hurricane season - Wikipedia.html",'r',encoding='utf-8'), "html.parser")
    
tables = soup(['table'])



for table in tables: 
 
    headers = [header.text.replace("\n","") for header in table.find_all('th')]
    
    rows = []
    df_ = pd.DataFrame(columns=headers)
    
    for i,row in enumerate(table.find_all('tr')):
        rows.append( [ str(val.text.encode('utf8')) for val in row.find_all('td')])
        #rows.append( [val.text.encode('utf8') for val in row.find_all('td')])
        rows[i] = [x.replace("b'","") for x in rows[i]]
        rows[i] = [x.replace("\\n'","") for x in rows[i]]
        rows[i] = [x.replace("'","") for x in rows[i]]
        rows[i] = [x.replace("\\xe2\\x80\\x93","-") for x in rows[i]]
        rows[i] = [x.replace("\\xe2\\x80\\xa2","-") for x in rows[i]]                
        if i>=1:
            df_.loc[i] = rows[i]

