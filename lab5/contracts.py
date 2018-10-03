
import pandas as pd
import sqlite3

#Import the Excel File
xls = pd.ExcelFile('Top_100_Contractors_Report_Fiscal_Year_2015.xls')

#Find all sheets in the Excel File
sheets = xls.sheet_names

#Keep only Federal and Department data
sheets_toKeep = ['Federal']

for sheet in sheets:
    print (sheet)
    if "00" in str(sheet): sheets_toKeep.append(sheet)
    
#Read Federal and Department data to pd frame    
excels = pd.read_excel("Top_100_Contractors_Report_Fiscal_Year_2015.xls",sheet_name = sheets_toKeep)

df = excels["Federal"]
df["Department"] = "Federal"

for sheet in sheets_toKeep:
    if sheet == "Federal": continue
    data = excels[sheet]
    data["Department"] = sheet
    df = df.append(excels[sheet],ignore_index = True)


#Create the contractors table        
contractors = pd.DataFrame(df["Global Vendor Name"].unique(),columns = ["Global Vendor Name"])
contractors ["Pkey"]  = contractors.index

conn = sqlite3.connect("contracts.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS contractors;")
cur = conn.cursor()
cur.execute("""
            create table contractors 
            (id int PRIMARY KEY, 
            global_vendor_name text )
            """
            )
conn.commit()

for i in contractors["Pkey"]:      
    new_row = [contractors.Pkey[i],contractors["Global Vendor Name"][i]]
    sql = "insert into contractors values ({0})".format(str(new_row)).replace('[','').replace("]","")
    cur = conn.cursor()
    cur.execute(sql)
    #print( sql )
conn.commit()    
cur.close()
conn.close()

#Create the actions table    

df_new = df.join(contractors.set_index('Global Vendor Name'), on='Global Vendor Name')
df_new = df_new.rename(index=str, columns={"Pkey": "contractor_id"})

actions = df_new[["Department","Number of Actions","Dollars Obligated","contractor_id"]]

conn = sqlite3.connect("contracts.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS actions;")
cur = conn.cursor()
cur.execute("""
            create table actions 
            (id int PRIMARY KEY, 
            Department text,
            actions int,
            dollars REAL,
            contractor_id int )
            """
            )
conn.commit()

for i in range(len(actions)):          
    new_row = [actions.index[i], actions.Department[i],   str(actions["Number of Actions"][i]), str(actions["Dollars Obligated"][i]),str(actions.contractor_id[i])]
    sql = "insert into actions values ({0})".format(str(new_row)).replace('[','').replace("]","")
    cur = conn.cursor()
    cur.execute(sql)
    #print( sql )
conn.commit()    
cur.close()
conn.close()




contractor_id_department_count = actions[["Department","contractor_id"]].groupby(["contractor_id"]).agg(['count'])

contractor_id_department_count.columns =["departments"]

contractor_id_department_count["contractor_id"] = contractor_id_department_count.index
 
contractor_id_department_counts = contractor_id_department_count.groupby(["departments"]).agg(['count'])

contractor_id_department_counts.columns =["Vendors"]
total_vendors = contractor_id_department_counts.sum()[0]
contractor_id_department_counts["Vendors"] =  contractor_id_department_counts["Vendors"] /total_vendors


import numpy as np
import random as py_random
import numpy.random as np_random
import time
import seaborn as sns
import matplotlib.pyplot as plt


THEME = "darkslategray"

contractor_id_department_counts.loc[15] = 0 
contractor_id_department_counts.loc[19] = 0 

contractor_id_department_counts = contractor_id_department_counts.sort_index()

percent = contractor_id_department_counts["Vendors"]
departments =  contractor_id_department_counts.index
width = 1/2

figure = plt.figure(figsize=(10, 6)) # first element is width, second is height.

axes = figure.add_subplot(1, 1, 1)

axes.set_title( "Vendors Received Contracts")
axes.bar(range(0, len(percent)), percent, width, color=THEME, align="center")
axes.set_xticks(range(0, len(percent)))
axes.set_xticklabels(departments)
axes.yaxis.grid( b=True, which="major")
axes.set_ylim((0, 1))
axes.set_ylabel( "Percent of Total Vendors")
axes.set_xlabel( "Departments")

rects = axes.patches

# Make some labels.
labels = round(percent*100,1)

for rect, label in zip(rects, labels):
    height = rect.get_height()
    axes.text(rect.get_x() + rect.get_width() / 2, height + 0.1, label,
            ha='center', va='bottom')
    
plt.show()


