import os
import json
import pandas as pd  
import datetime 
import time

def log_store(action,scraping_source,link,output):     
    print("logging")
    actions = []  
    source = []  
    links = [] 
    time_stamps = [] 
    file = []
    actions.append(action) 
    source.append(scraping_source)
    links.append(link) 
    file.append(output)
    ts = time.time() 
    ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')   
    time_stamps.append(ts)
    rows = pd.DataFrame({"Action": actions, "Source":source, "Link": links, "Timestamp":time_stamps, "File_Output":file}) 
    rows.to_csv("logs/scraping_logs.csv", index=False) 
    return True
    # rows.to_csv("logs/scraping_logs.csv", index=False,mode='a', header=False)