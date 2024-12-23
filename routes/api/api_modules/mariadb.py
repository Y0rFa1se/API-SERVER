import pymysql
import os
import re

async def get_db_connection(db_name: str):
    connection = pymysql.connect(
        host = os.getenv("HOST"),
        user = "root",
        password = os.getenv("MARIADB_PASSWORD"),
        database = "mysql",
        cursorclass = pymysql.cursors.DictCursor
    )

    connection.select_db(db_name)

    return connection

async def is_query_safe(query: str):
    modifying_keywords = [
        r'\bINSERT\b', r'\bUPDATE\b', r'\bDELETE\b', r'\bDROP\b', r'\bALTER\b',
        r'\bTRUNCATE\b', r'\bREPLACE\b', r'\bCREATE\b', r'\bRENAME\b', r'\bMERGE\b'
    ]
    
    pattern = re.compile('|'.join(modifying_keywords), re.IGNORECASE)
    
    if pattern.search(query):
        return True
    return False

async def query_db(password: str, db_name: str, query: str):
    if password != os.getenv("GUEST_PASSWORD"):
        return "Incorrect password"
    
    if await is_query_safe(query):
        return "Unsafe query"
    
    conn = await get_db_connection(db_name)
    c = conn.cursor()

    c.execute(query)
    result = c.fetchall()

    conn.close()

    return result