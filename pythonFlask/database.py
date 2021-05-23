import sqlite3
from sqlite3 import Error
from datetime import datetime

class Database():
    """
    Used to create, and write to a database that stores the user's info
    """
    def __init__(self):
        """
        create database file
        :param: None
        :return: None
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect("messages.db")
        except Error as e:
            print(e)

        self.cursor = self.conn.cursor()
        self.createTable()
    
    def close(self):
        """
        -close conn
        :param: None
        :return: None
        """
        self.conn.close()

    def createTable(self):
        """
        -create new table in database file if it doesn't exist yet
        :param: None
        :return: None
        """
        query = """CREATE TABLE IF NOT EXISTS Messages
                    (name TEXT, content TEXT, hour TEXT, minute TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT)"""
        self.cursor.execute(query)
        self.conn.commit()

    def getMessages(self):
        """
        -get messages for specific user
        :param: None
        :return rows: list 
        """
        query = """SELECT content, name, hour, minute FROM Messages"""
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        # get the last 15 messages
        length = len(rows)
        rows = rows[length - 15:]
        return list(rows)
        

    def addMessage(self, message, name):
        """
        add message, username, and current time into database
        :param message: str
        :param name: str
        :return: None
        """
        currentTime = datetime.now()
        currentHour = currentTime.hour
        currentMinute = currentTime.minute
        query = f"""INSERT INTO Messages (name, content, hour, minute, id) VALUES(?, ?, ?, ?, ?)"""
        self.cursor.execute(query, 
        (name, message, currentHour, currentMinute, None))
        self.conn.commit()
