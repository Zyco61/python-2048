import os
import sqlite3
from sqlite3.dbapi2 import connect

class DataBaseHandler():
    def __init__(self, database_name: str):
        self.con = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}")
        self.con.row_factory = sqlite3.Row
    
    def get_user(self, username: str):
        cursor = self.con.cursor()
        query = "SELECT * FROM users WHERE username = ?;"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return list(result)
    
    def create_user(self, username: str):
        cursor = self.con.cursor()
        query = "INSERT INTO users (username) VALUES (?) RETURNING id;"
        cursor.execute(query, (username,))
        result = list(map(str, cursor.fetchone()))
        cursor.close()
        self.con.commit()
        return result

    def user_exist(self, username: str) -> str:
        cursor = self.con.cursor()
        query = "SELECT username FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        return len(cursor.fetchall()) > 0
    
    def get_leaderboard(self):
        cursor = self.con.cursor()
        cursor.execute("SELECT username, score FROM score JOIN users USING(id) ORDER BY score DESC LIMIT(5)")
        return list(map(list, cursor.fetchall()))

    def insert_score(self, score, id):
        cursor = self.con.cursor()
        query = ("INSERT INTO score(id, score) VALUES (?, ?)")
        cursor.execute(query, (id, score))
        self.con.commit()
        cursor.close()