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


def fetchall(table: str, columns: list[str], condition: str = None) -> list[tuple]:
    columns_joined = ", ".join(columns)
    query = f"SELECT {columns_joined} FROM {table}"
    if condition:
        query += f" {condition}"
    cur.execute(query)
    rows = cur.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result
