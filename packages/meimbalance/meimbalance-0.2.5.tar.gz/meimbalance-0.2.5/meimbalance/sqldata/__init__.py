from dotenv import load_dotenv
import pyodbc # Python interface for ODBC API         https://github.com/mkleehammer/pyodbc
import os
from datetime import datetime
import logging
import platform

def get_read_connection():
    try:
        load_dotenv(verbose=False, override=True)
    except:
        logging.info('Error in load_dotenv')

    server=os.environ['IMBALANCE_LOG_SERVER']
    database=os.environ['IMBALANCE_LOG_DATABASE']
    username=os.environ['IMBALANCE_LOG_READ_USERNAME']
    password=os.environ['IMBALANCE_LOG_READ_PASSWORD']
    driver='ODBC Driver 17 for SQL Server'
    if platform.system() == 'Windows':
        driver='SQL Server'
    tries=0
    while tries < 5:
        try:
            connection = pyodbc.connect('DRIVER={' + driver + '};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
            break
        except:
            tries = tries + 1
            logging.info('get_connection retry')
    
    return connection

