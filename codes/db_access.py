import pymysql
import pandas as pd
from PyQt5.QtWidgets import QTableWidgetItem

from datetime import datetime


def connect_db(host_name, user_name, pw, db_name, port_num):
    
    connection = pymysql.connect(host = host_name,
                                 user = user_name,
                                 password = pw,
                                 database = db_name,
                                 port = port_num,
                                 cursorclass = pymysql.cursors.DictCursor)
    
    return connection


def init_table_widget(table_widget, sql_query):
    
    # connect db
    connection = connect_db(
            host_name ="localhost",
            user_name ="root",
            pw ="0329",
            db_name="dbtermproject",
            port_num =3305)

    cursors = connection.cursor()
    
    # SQL QUERY
    cursors.execute(sql_query)
    
    # data fetch
    data = pd.DataFrame(data=cursors.fetchall())
    connection.close()
    
    # clear table
    table_widget.clear()
    
    # write table
    col = len(data.keys())
    table_widget.setColumnCount(col)
    table_widget.setHorizontalHeaderLabels(data.keys())
    
    row = len(data.index)
    table_widget.setRowCount(row)
    
    for r in range(row):
        for c in range(col):
            item = QTableWidgetItem(str(data.iloc[r,c]))
            table_widget.setItem(r,c,item)
        
    table_widget.resizeColumnsToContents()


def delete_values(table_name, primary_key, pk_value):
    pass

# test
if __name__ == '__main__':
    pass