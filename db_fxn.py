import sqlite3


conn = sqlite3.connect("Tasks.db")
c = conn.cursor()


def create_table(team):
    c.execute(f'CREATE TABLE IF NOT EXISTS {team}taskstable(task TEXT,task_status TEXT, start_date TEXT, task_due_date DATE, task_av TEXT, teams TEXT)')

def add_task(team,task,task_status,start_date,task_due_date,task_av,teams):
    c.execute(f'INSERT INTO {team}taskstable(task,task_status,start_date,task_due_date,task_av,teams) VALUES (?,?,?,?,?,?)',(task,task_status,start_date,task_due_date,task_av,teams))
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

def edit_task_data(team,new_task,new_task_status,new_start_date,new_task_date,new_task_av,task,task_status,start_date,task_due_date,task_av):
    c.execute(f'UPDATE {team}taskstable SET task=?,task_status=?,start_date=?,task_due_date=?, task_av=? WHERE task=? and task_status=? and start_date=? and task_due_date=? and task_av=?', (new_task,new_task_status,new_start_date,new_task_date,new_task_av,task,task_status,start_date,task_due_date,task_av))
    conn.commit()
    data = c.fetchall()
    return data

def delete_task(team,task):
    c.execute('DELETE FROM {}taskstable WHERE task="{}"'.format(team,task))
    conn.commit()
    data = c.fetchall()
    return data



