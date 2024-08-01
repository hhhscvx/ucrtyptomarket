import os
import sqlite3


conn = sqlite3.connect("profile.db")
cur = conn.cursor()


def insert(table: str, column_values: dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cur.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()
