
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
            (id int, 
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
