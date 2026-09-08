import os

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# =========================================================
# CREATE MYSQL CONNECTION
# =========================================================

def get_db_connection(database_name=None):
    """
    Create a connection to MySQL.

    If database_name is supplied, that database
    will be selected.
    """

    try:

        config = {
            "host": DB_HOST,
            "port": DB_PORT,
            "user": DB_USER,
            "password": DB_PASSWORD
        }

        if database_name:

            database_name = str(
                database_name
            ).strip()

            if not database_name:

                raise ValueError(
                    "Database name cannot be empty."
                )

            config["database"] = database_name

        connection = mysql.connector.connect(
            **config
        )

        if connection.is_connected():

            print(
                "[DATABASE] Connected to MySQL"
                + (
                    f" | Database: {database_name}"
                    if database_name
                    else " | Server connection"
                )
            )

            return connection

        raise ConnectionError(
            "Could not connect to MySQL."
        )

    except Error as e:

        print(
            f"[DATABASE] Connection error: {e}"
        )

        raise


# =========================================================
# GET DATABASES
# =========================================================

def get_databases():
    """
    Return all databases available on MySQL.
    """

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute(
            "SHOW DATABASES"
        )

        rows = cursor.fetchall()

        databases = []

        for row in rows:

            if row and row[0]:

                databases.append(
                    str(row[0])
                )

        print(
            f"[DATABASE] Databases found: "
            f"{databases}"
        )

        return databases

    except Error as e:

        print(
            f"[DATABASE] Error getting databases: {e}"
        )

        raise

    finally:

        if cursor:

            cursor.close()

        if connection and connection.is_connected():

            connection.close()


# =========================================================
# GET TABLES
# =========================================================

def get_tables(database_name):
    """
    Return all tables from the specified database.
    """

    if not database_name:

        raise ValueError(
            "Database name is required."
        )

    database_name = str(
        database_name
    ).strip()

    print(
        f"[DATABASE] Getting tables from: "
        f"'{database_name}'"
    )

    connection = None
    cursor = None

    try:

        connection = get_db_connection(
            database_name
        )

        cursor = connection.cursor()

        cursor.execute(
            "SHOW TABLES"
        )

        rows = cursor.fetchall()

        tables = [
            str(row[0])
            for row in rows
            if row and row[0]
        ]

        print(
            f"[DATABASE] Tables in "
            f"'{database_name}': {tables}"
        )

        return tables

    except Error as e:

        print(
            f"[DATABASE] Error getting tables "
            f"from '{database_name}': {e}"
        )

        raise

    finally:

        if cursor:

            cursor.close()

        if connection and connection.is_connected():

            connection.close()


# =========================================================
# GET TABLE STRUCTURE
# =========================================================

def get_table_structure(
    database_name,
    table_name
):
    """
    Return the structure of a specific table.
    """

    if not database_name:

        raise ValueError(
            "Database name is required."
        )

    if not table_name:

        raise ValueError(
            "Table name is required."
        )

    database_name = str(
        database_name
    ).strip()

    table_name = str(
        table_name
    ).strip()

    print(
        f"[DATABASE] Describing "
        f"'{database_name}.{table_name}'"
    )

    connection = None
    cursor = None

    try:

        connection = get_db_connection(
            database_name
        )

        cursor = connection.cursor()

        # -------------------------------------------------
        # Verify table exists
        # -------------------------------------------------

        cursor.execute(
            "SHOW TABLES"
        )

        tables = {
            str(row[0])
            for row in cursor.fetchall()
        }

        if table_name not in tables:

            raise ValueError(
                f"Table '{table_name}' does not "
                f"exist in database '{database_name}'."
            )

        # -------------------------------------------------
        # Describe table
        # -------------------------------------------------

        cursor.execute(
            f"DESCRIBE `{table_name}`"
        )

        rows = cursor.fetchall()

        columns = []

        for row in rows:

            columns.append({

                "name": row[0],

                "type": row[1],

                "nullable": row[2],

                "key": row[3],

                "default": row[4],

                "extra": row[5]

            })

        return columns

    except Error as e:

        print(
            f"[DATABASE] Error describing "
            f"'{database_name}.{table_name}': {e}"
        )

        raise

    finally:

        if cursor:

            cursor.close()

        if connection and connection.is_connected():

            connection.close()


# =========================================================
# GET ROW COUNT
# =========================================================

def get_row_count(
    database_name,
    table_name
):
    """
    Return the number of rows in a table.
    """

    if not database_name:

        raise ValueError(
            "Database name is required."
        )

    if not table_name:

        raise ValueError(
            "Table name is required."
        )

    database_name = str(
        database_name
    ).strip()

    table_name = str(
        table_name
    ).strip()

    connection = None
    cursor = None

    try:

        connection = get_db_connection(
            database_name
        )

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT COUNT(*) "
            f"FROM `{table_name}`"
        )

        result = cursor.fetchone()

        count = result[0]

        print(
            f"[DATABASE] "
            f"{database_name}.{table_name} "
            f"contains {count} rows"
        )

        return count

    except Error as e:

        print(
            f"[DATABASE] Error getting row count: {e}"
        )

        raise

    finally:

        if cursor:

            cursor.close()

        if connection and connection.is_connected():

            connection.close()


# =========================================================
# GET SAMPLE DATA
# =========================================================

def get_sample_data(
    database_name,
    table_name,
    limit=5
):
    """
    Return sample rows from a table.
    """

    if not database_name:

        raise ValueError(
            "Database name is required."
        )

    if not table_name:

        raise ValueError(
            "Table name is required."
        )

    database_name = str(
        database_name
    ).strip()

    table_name = str(
        table_name
    ).strip()

    # Keep limit safe

    try:

        limit = int(limit)

    except (ValueError, TypeError):

        limit = 5

    limit = max(
        1,
        min(limit, 20)
    )

    connection = None
    cursor = None

    try:

        connection = get_db_connection(
            database_name
        )

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM `{table_name}` "
            f"LIMIT {limit}"
        )

        rows = cursor.fetchall()

        columns = []

        if cursor.description:

            columns = [
                description[0]
                for description in cursor.description
            ]

        return {
            "columns": columns,
            "rows": rows
        }

    except Error as e:

        print(
            f"[DATABASE] Error getting sample data: {e}"
        )

        raise

    finally:

        if cursor:

            cursor.close()

        if connection and connection.is_connected():

            connection.close()


# =========================================================
# EXECUTE READ-ONLY SQL
# =========================================================

def execute_read_query(
    database_name,
    query
):
    """
    Execute a read-only SQL query.

    Only SELECT and WITH queries are allowed.
    """

    if not database_name:

        raise ValueError(
            "Database name is required."
        )

    if not query:

        raise ValueError(
            "SQL query cannot be empty."
        )

    database_name = str(
        database_name
    ).strip()

    query = str(
        query
    ).strip()

    query_lower = query.lower()

    # -----------------------------------------------------
    # Only SELECT / WITH
    # -----------------------------------------------------

    if not (
        query_lower.startswith("select")
        or query_lower.startswith("with")
    ):

        raise ValueError(
            "Only SELECT and WITH queries "
            "are allowed."
        )

    # -----------------------------------------------------
    # Block dangerous operations
    # -----------------------------------------------------

    forbidden_keywords = [
        "insert ",
        "update ",
        "delete ",
        "drop ",
        "alter ",
        "truncate ",
        "create ",
        "replace ",
        "grant ",
        "revoke "
    ]

    for keyword in forbidden_keywords:

        if keyword in query_lower:

            raise ValueError(
                "Query contains a forbidden "
                "SQL operation."
            )

    connection = None
    cursor = None

    try:

        print(
            f"[DATABASE] Executing query "
            f"on '{database_name}':"
        )

        print(query)

        connection = get_db_connection(
            database_name
        )

        cursor = connection.cursor()

        cursor.execute(
            query
        )

        rows = cursor.fetchall()

        columns = []

        if cursor.description:

            columns = [
                description[0]
                for description in cursor.description
            ]

        return {
            "columns": columns,
            "rows": rows
        }

    except Error as e:

        print(
            f"[DATABASE] SQL query error: {e}"
        )

        raise

    finally:

        if cursor:

            cursor.close()

        if connection and connection.is_connected():

            connection.close()