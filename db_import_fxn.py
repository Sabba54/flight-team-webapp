import sqlite3
import pandas as pd

conn2 = sqlite3.connect("Tasks.db")
c2 = conn2.cursor()

def create_new_db(team):
    c2.execute('CREATE TABLE newtaskstable(task TEXT,task_status TEXT, task_due_date DATE, team TEXT)')
    newtaskstable = pd.read_csv('database_tasks.csv')
    newtaskstable.to_sql('newtaskstable',conn2, if_exists='append', index = False)