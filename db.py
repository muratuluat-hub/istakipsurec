import sqlite3

DB_PATH = "database.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS firms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        firm_id INTEGER,
        employee_id INTEGER,
        task_name TEXT,
        due_date TEXT,
        status TEXT DEFAULT 'Beklemede',
        notes TEXT
    )''')
    conn.commit()
    conn.close()

def add_firm(name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO firms (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def list_firms():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM firms ORDER BY name")
    data = c.fetchall()
    conn.close()
    return data

def add_employee(name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO employees (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def list_employees():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM employees ORDER BY name")
    data = c.fetchall()
    conn.close()
    return data

def add_task(firm_id, employee_id, task_name, due_date):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (firm_id, employee_id, task_name, due_date) VALUES (?, ?, ?, ?)", 
              (firm_id, employee_id, task_name, due_date))
    conn.commit()
    conn.close()

def list_tasks():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT t.id, f.name, e.name, t.task_name, t.due_date, t.status, t.notes
                 FROM tasks t
                 LEFT JOIN firms f ON t.firm_id=f.id
                 LEFT JOIN employees e ON t.employee_id=e.id
                 ORDER BY t.id DESC""")
    data = c.fetchall()
    conn.close()
    return data

def update_task(task_id, status, notes):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE tasks SET status=?, notes=? WHERE id=?", (status, notes, task_id))
    conn.commit()
    conn.close()
def update_firm(old_name, new_name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE firms SET name=? WHERE name=?", (new_name, old_name))
    conn.commit()
    conn.close()

def delete_firm(name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM firms WHERE name=?", (name,))
    conn.commit()
    conn.close()

def delete_employee(name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM employees WHERE name=?", (name,))
    conn.commit()
    conn.close()
def update_firm(old_name, new_name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE firms SET name=? WHERE name=?", (new_name, old_name))
    conn.commit()
    conn.close()

def delete_firm(name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM firms WHERE name=?", (name,))
    conn.commit()
    conn.close()

def delete_employee(name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM employees WHERE name=?", (name,))
    conn.commit()
    conn.close()
import sqlite3
from datetime import datetime, timedelta

def delete_old_completed_tasks(db_name="tasks.db"):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        # 30 günden eski tamamlanmış görevleri sil
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        c.execute("""
            DELETE FROM tasks
            WHERE status='Tamamlandı'
            AND (
                (due_date IS NOT NULL AND date(due_date) <= date(?))
                OR (completed_date IS NOT NULL AND date(completed_date) <= date(?))
            )
        """, (thirty_days_ago, thirty_days_ago))

        deleted = c.rowcount
        conn.commit()
        conn.close()
        print(f"🧹 {deleted} eski tamamlanmış görev silindi.")
    except Exception as e:
        print(f"🚨 Silme hatası: {e}")
