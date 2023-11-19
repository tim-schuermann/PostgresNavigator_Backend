import bcrypt
import app.database as db
from dotenv import load_dotenv
import os
from typing import List, Dict
from passlib.context import CryptContext
from app.schemas import UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Load environment variables from .env file
load_dotenv()

# Environment variables
ALLOWED_TABLES = os.getenv("ALLOWED_TABLES", "").split(",")

# Function to check if the table name is valid
def is_valid_table_name(table_name):
    return table_name in ALLOWED_TABLES

def drop_table(table_name: str):
    # Validate table name against whitelist
    if not is_valid_table_name(table_name):
        raise ValueError("Invalid table name provided.")
    drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
    with db.get_db_cursor(commit=True) as cursor:
        cursor.execute(f"SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}';")
        table_exists = cursor.fetchone() is not None

        if table_exists:
            cursor.execute(drop_table_query)
            return f"Table {table_name} has been dropped."
        else:
            return f"No such table: {table_name}"

def create_users_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        role VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        full_name VARCHAR(255) NOT NULL,
        disabled BOOLEAN NOT NULL,
        hashed_password TEXT NOT NULL
    );
    """
    with db.get_db_cursor(commit=True) as cursor:
        cursor.execute(create_table_query)

def create_user(username: str, password: str, role: str, email: str, full_name: str, disabled: bool = False):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password_str = hashed_password.decode('utf-8')
    with db.get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO users (username, role, email, full_name, disabled, hashed_password) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;",
            (username, role, email, full_name, disabled, hashed_password_str)
        )
        user_id = cursor.fetchone()['id']
        return user_id

def get_user_by_id(user_id: int):
    with db.get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        return user

def get_user_by_username(username: str) -> UserInDB | None:
    with db.get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = %s;", (username,))
        user_record = cursor.fetchone()
        return user_record

def fetch_one(table_name: str, column: str, value: str):
    # Validate table name against whitelist
    if not is_valid_table_name(table_name):
        raise ValueError("Invalid table name provided.")

    # Protect against SQL injection in column name
    if not column.isidentifier():
        raise ValueError("Invalid column name provided.")

    # Now that we've validated the table name and column, we can interpolate them into the query
    fetch_query = f"SELECT * FROM \"{table_name}\" WHERE {column} = %s;"

    with db.get_db_cursor() as cursor:
        cursor.execute(fetch_query, (value,))
        return cursor.fetchone()

def fetch_all(table_name: str, columns):
    # Validate table name against whitelist
    if not is_valid_table_name(table_name):
        raise ValueError("Invalid table name provided.")

    if isinstance(columns, str):
        columns = [columns]  # Ensure columns is a list

    # Protect against SQL injection in column names
    columns = [f'"{column}"' for column in columns if column.isidentifier()]

    # Joining columns into a string for the SQL statement
    columns_sql = ", ".join(columns)

    # Now that we've validated the table name and columns, we can interpolate them into the query
    fetch_query = f"SELECT {columns_sql} FROM \"{table_name}\";"

    with db.get_db_cursor() as cursor:
        cursor.execute(fetch_query)
        return cursor.fetchall()

def fetch_ids_for_names(table_name: str, names: List[str]) -> List[int]:
    placeholders = ', '.join(['%s'] * len(names))
    query = f"SELECT id FROM \"{table_name}\" WHERE name IN ({placeholders});"
    with db.get_db_cursor() as cursor:
        cursor.execute(query, names)
        return [row[0] for row in cursor.fetchall()]

def fetch_items_by_foreign_keys(tables_with_names: Dict[str, List[str]]):
    # First, collect all the IDs for the given names from their respective tables
    ids_collected = {}
    for table_name, names in tables_with_names.items():
        ids_collected[table_name] = fetch_ids_for_names(table_name, names)

    # Now build a query to select items that have these IDs as foreign keys
    where_clauses = []
    for table_name, ids in ids_collected.items():
        foreign_key_column = f"{table_name}_id"
        ids_list = ', '.join(map(str, ids))
        where_clauses.append(f"{foreign_key_column} IN ({ids_list})")

    where_statement = ' OR '.join(where_clauses)
    items_query = f"SELECT * FROM items WHERE {where_statement};"

    # Fetch and return the items
    with db.get_db_cursor() as cursor:
        cursor.execute(items_query)
        return cursor.fetchall()

if __name__ == '__main__':
    # drop_table("users")
    create_users_table()
    test = fetch_all("projects", "name")