# -*- coding: utf-8 -*-


#this is a script to store scraped content into database
#if we scrape a lot of websites or simply scrape a website everyday
#we will end up with a huge amount of data
#it is essential to create a data warehouse to keep everything organized
import sqlite3
import requests
import pandas as pd
from io import BytesIO
import re
import pyodbc


#say if we wanna get the trader commitment report of lme from the link below
# https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders#tabIndex=1
#when we select aluminum and we will be redirected to a new link
# https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Aluminium
#if we try to view page source, we will find nothing in html parse tree
#what do we do?
#here is a very common scenario in web scraping
#we simply right click and select inspect element
#we will have to monitor the traffic one by one to identify where the report comes from
#as usual, i have done it for you
def get_download_link():
    
    download_link='https://www.lme.com/api/Lists/DownloadLinks/%7B02E29CA4-5597-42E7-9A22-59BB73AE8F6B%7D'
        
    
    #there are quite a few pages of reports
    #for simplicity, we only care about the latest report
    #note that the page counting starts from 0
    session=requests.Session()
    response = session.get(download_link, 
                           params={"currentPage": 0})
    
    
    #the response is a json file
    #i assume you should be familiar with json now
    #if not, plz check the link below
    # https://github.com/je-suis-tm/web-scraping/blob/master/CME2.py
    url_list=response.json()['content_items']
    
    
    return url_list



#once we find out where the download link is
#we can get the actual report
def get_report(url_list):
    
    prefix='https://www.lme.com'    
    url=url_list[0]['Url']
    
    
    session=requests.Session()
    response = session.get(prefix+url)
    
    
    #we also get the date of the data from url
    date=pd.to_datetime(re.search(r"\d{4}/\d{2}/\d{2}",url).group())
    
    return response.content,date


#
def etl(content,date):
    
    #the first seven rows are annoying headers
    #we simply skip them
    df = pd.ExcelFile(BytesIO(content)).parse('AH', skiprows=7)
    
    #assume we only want positions of investment funds 
    #lets do some etl
    df['Unnamed: 0'].fillna(method='ffill',
                            inplace=True)
    
    col=list(df.columns)
    for i in range(1,len(col)):
        if 'Unnamed' in col[i]:
            col[i]=col[i-1]
    
    df.columns=col
    del df['Notation of the position quantity']
    df.dropna(inplace=True)
    
    output=df['Investment Funds'][df['Unnamed: 0']=='Number of Positions']    
    output.columns=['long','short']
    
    output=output.melt(value_vars=['long','short'], 
                       var_name='position', 
                       value_name='value')
    
    output['type']=df['LOTS'].drop_duplicates().tolist()*2
    output['date']=date
    
    return output


#for sql server
#we have to use pyodbc driver
def connect(
        server=None, database=None, driver=None,
        username=None, password=None,
        autocommit=False
    ):
        """ get the db connection """
        connection_string = "Driver={driver}; Server={server}; Database={database}"
        if username:
            connection_string += "; UID={username}"
        if password:
            connection_string += "; PWD={password}"
        if not driver:
            driver = [
                d for d in sorted(pyodbc.drivers())
                if re.match(r"(ODBC Driver \d+ for )?SQL Server", d)
            ][0]
    
        return pyodbc.connect(
            connection_string.format(
                server=server,
                database=database,
                driver=driver,
                username=username,
                password=password,
            ),
            autocommit=autocommit,
        )
            
            
#this function is to insert data into sqlite3 database
#i will not go into details for sql grammar
#for pythoners, sql is a piece of cake
#go check out the following link for sql
# https://www.w3schools.com/sql/
def database(df,SQL=False):
    
    #plz make sure u have created the database and the table to proceed
    #to create a table in database, first two lines are the same as below
    #just add a few more lines
    
    #c.execute("""CREATE TABLE lme (position TEXT, value FLOAT, type TEXT, date DATE);""")
    #conn.commit()
    #conn.close()
    
    #connect to sqlite3
    if not SQL:
        
        #to see what it looks like in the database
        #use microsoft access or toad or just pandas
        #db=pd.read_sql("""SELECT * FROM lme""",conn)
        conn = sqlite3.connect('database.db')
    else:
        SERVER='10.10.10.10'
        DATABASE='meme_stock'
        conn=connect(SERVER,DATABASE,'SQL Server')
    c = conn.cursor()      
        
    #insert data
    for i in range(len(df)):
        try:
            c.execute("""INSERT INTO lme VALUES (?,?,?,?)""",df.iloc[i,:])
            conn.commit()
            print('Updating...')
        except Exception as e:
            print(e)
    
    #always need to close it
    conn.close()

    print('Done.')

    return 


#
def main():
    
    url_list=get_download_link()
    
    content,date=get_report(url_list)
    
    output=etl(content,date)
    
    database(output)
    

if __name__ == "__main__":
    main()
