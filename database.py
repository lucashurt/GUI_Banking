import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

def initialize_connection():
    mydb = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        passwd=os.getenv("DB_PASS")
    )
    cursor = mydb.cursor()
    create_database(cursor)
    create_tables(cursor)
    return mydb, cursor

def create_database(cursor):
    cursor.execute("SHOW DATABASES")
    temp = cursor.fetchall()
    databases = (item[0] for item in temp)
    if "bank_database" not in databases:
        cursor.execute("CREATE DATABASE bank_database")

    cursor.execute("USE bank_database")

def create_tables(cursor):
    cursor.execute("SHOW TABLES")
    temp = cursor.fetchall()
    tables = (item[0] for item in temp)
    if "user_info" not in tables:
        cursor.execute("""CREATE TABLE user_info(account_number INT PRIMARY KEY AUTO_INCREMENT,
                                                 name VARCHAR(70), 
                                                 username VARCHAR(50),
                                                 password VARCHAR(50),
                                                 PIN INT,
                                                 balance DECIMAL(65,2) default 0)""")

def create_transaction_table(cursor,mydb,username):
    cursor.execute("SHOW TABLES")
    temp = cursor.fetchall()
    tables = (item[0] for item in temp)
    if f"{username}_transactions" not in tables:
        cursor.execute(f"""CREATE TABLE {username}_transactions(account_number INTEGER,
                                                                action VARCHAR(15),
                                                                amount DECIMAL(65,2),
                                                                action_date DATE DEFAULT (CURRENT_DATE)) """)
        mydb.commit()

def insert_into_transaction_table(cursor,mydb,username,account_number,action,amount):
    sql = f"INSERT INTO {username}_transactions(account_number,action,amount) VALUES(%s,%s,%s)"
    val = (account_number,action,amount)
    cursor.execute(sql,val)
    mydb.commit()

def register(cursor,mydb,data):
    name = data["name"]
    username = data["username"]
    password = data["password"]
    PIN = data["PIN"]
    sql = "INSERT INTO user_info(name,username,password,PIN) VALUES(%s,%s,%s,%s)"
    val = (name,username,password,PIN)
    cursor.execute(sql,val)
    mydb.commit()
    create_transaction_table(cursor,mydb,username)

def login(cursor,data):
    username = data["username"]
    password = data["password"]
    sql = "SELECT * FROM user_info WHERE username=%s AND password=%s"
    val = (username,password)
    cursor.execute(sql,val)

    if cursor.fetchone() is not None:
        return True
    return False

def username_not_available(cursor,data):
    username = data["username"]
    sql = "SELECT * FROM user_info WHERE username=%s"
    val = (username,)
    cursor.execute(sql,val)
    if cursor.fetchone() is not None:
        return True
    return False

def account_number_available(cursor,account_number):
    checked_account_number = account_number
    sql = "SELECT * FROM user_info WHERE account_number=%s"
    val = (checked_account_number,)
    cursor.execute(sql,val)
    if cursor.fetchone() is not None:
        return True
    return False

def return_information_using_username(cursor,action,username):
    sql = f"SELECT {action} FROM user_info WHERE username=%s"
    val = (username,)
    cursor.execute(sql,val)
    result = cursor.fetchone()[0]
    return result

def return_information_using_account_number(cursor,action,account_number):
    sql = f"SELECT {action} FROM user_info WHERE account_number=%s"
    val = (account_number,)
    cursor.execute(sql,val)
    result = cursor.fetchone()[0]
    return result
