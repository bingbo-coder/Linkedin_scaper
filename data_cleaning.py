# -*- coding: utf-8 -*-
"""
@author: Edoardo Chen
"""

import pandas as pd

df = pd.read_csv("database/linkedin_jobs.csv")
dft = df


# Columns "N employees" column covert the string into numeric value :
# For 11000 value it means more than 10000
# And 0 value it means that there is no data and later will be proccess                                                       "
df_emp = df["N. employees"].replace({"51-200 dipendenti ": "200",
                            "Oltre 10.001 dipendenti " : "11000", # Oltre i 10.000
                            "1001 - 5000 dipendenti " : "5000",
                            "11-50 dipendenti " : "50",
                            "201-500 dipendenti " : "500",
                            "51-200 dipendenti" : "200",
                            "1-10 dipendenti" : "10",
                            "501 - 1000 dipendenti " : "1000",
                            "1-10 dipendenti " : "10",
                            "5001 - 10.000 dipendenti ": "10000",
                            "11-50 dipendenti" : "50",
                            "201-500 dipendenti" : "500",
                            "501 - 1000 dipendenti" : "1000",
                            "1001 - 5000 dipendenti" : "5000",
                            "Visualizza i trend di assunzione recenti per Manpower. Prova Premium gratis" : "0",
                            "Visualizza i trend di assunzione recenti per Translated. Prova Premium gratis" : "0",
                            "Visualizza i trend di assunzione recenti per Takeda Pharmaceuticals. Prova Premium gratis" : "0"})

df_emp = pd.to_numeric(df_emp)
dft["N. employees"] = df_emp


# Columns "Post time"
def function(time):
    day = int(time.split(" ")[0])
    total_day = 0
    
    if "giorni" in time:
        total_day = day 
    elif "settimane" in time:
        total_day = day * 7
    elif "mese" in time:
        total_day = day * 30
    return total_day
dft["Post time"] = dft["Post time"].apply(function)


# Column Location 

dft["Location"] = dft["Location"].apply(lambda x: x.split(",")[0])

# Add Column (Python, Excel, exc..) from description 

dft["python"] = dft["Description"].apply(lambda x: 1 if "python" in x.lower() else 0)

dft["excel"] = dft["Description"].apply(lambda x: 1 if "excel" in x.lower() else 0)

dft["sql"] = dft["Description"].apply(lambda x: 1 if "sql" in x.lower() else 0)

dft["power bi"] = dft["Description"].apply(lambda x: 1 if "power bi" in x.lower() else 0)



dft.to_csv("database/linkedin_jobs_cleaned.csv")





