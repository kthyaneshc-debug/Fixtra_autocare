import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG, DATABASE_NAME

class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
        )
        cur = self.conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DATABASE_NAME}`")
        cur.close()
        self.conn.database = DATABASE_NAME
        self._create_tables()
        return self.conn

    def _create_tables(self):
        with open("schema.sql", "r", encoding="utf-8") as f:
            sql = f.read()
        cur = self.conn.cursor()
        for statement in [s.strip() for s in sql.split(";") if s.strip()]:
            if statement.upper().startswith("CREATE DATABASE"):
                continue
            cur.execute(statement)
        self.conn.commit()
        cur.close()

    def query(self, sql, params=(), fetch=False):
        cur = self.conn.cursor(dictionary=True)
        cur.execute(sql, params)
        result = cur.fetchall() if fetch else cur.rowcount
        self.conn.commit()
        cur.close()
        return result

    def scalar(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        row = cur.fetchone()
        cur.close()
        return row[0] if row else 0

    def close(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
