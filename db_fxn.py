import sqlite3


conn = sqlite3.connect("Tasks.db")
c = conn.cursor()


def create_table(team):
    c.execute(f'CREATE TABLE IF NOT EXISTS {team}taskstable(task TEXT,task_status TEXT, task_due_date DATE)')

def add_task(team,task,task_status,task_due_date):
    c.execute(f'INSERT INTO {team}taskstable(task,task_status,task_due_date) VALUES (?,?,?)',(task,task_status,task_due_date))
    conn.commit()

def view_all_task(team):
    c.execute(f'SELECT * FROM {team}taskstable')
    data = c.fetchall()
    return data

def view_unique_task(team):
    c.execute(f'SELECT DISTINCT task FROM {team}taskstable')
    data = c.fetchall()
    return data

def get_task(team,task):
    c.execute('SELECT * FROM {}taskstable WHERE task="{}"'.format(team,task))
    data = c.fetchall()
    return data

def edit_task_data(team,new_task,new_task_status,new_task_date,task,task_status,task_due_date):
    c.execute(f'UPDATE {team}taskstable SET task=?,task_status=?,task_due_date=? WHERE task=? and task_status=? and task_due_date=?', (new_task,new_task_status,new_task_date,task,task_status,task_due_date))
    conn.commit()
    data = c.fetchall()
    return data

def delete_task(team,task):
    c.execute('DELETE FROM {}taskstable WHERE task="{}"'.format(team,task))
    conn.commit()
    data = c.fetchall()
    return data



