from pathlib import Path

from mcp.server.fastmcp import FastMCP

from document_processor import (
    extract_text_from_pdf
)

from agent import summarize_document

from database import (
    get_databases,
    get_tables,
    get_table_structure,
    get_row_count,
    get_sample_data as db_get_sample_data,
    execute_read_query as db_execute_read_query
)


# =========================================================
# MCP SERVER
# =========================================================

mcp = FastMCP(
    "Document and Database MCP Server"
)


# =========================================================
# DIRECTORIES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(
    exist_ok=True
)


# =========================================================
# DOCUMENT TOOLS
# =========================================================

@mcp.tool()
def list_documents() -> list[str]:

    """
    List all documents in uploads.
    """

    return [
        file.name
        for file in UPLOAD_DIR.iterdir()
        if file.is_file()
    ]


# =========================================================
# READ PDF
# =========================================================

@mcp.tool()
def read_pdf(
    filename: str
) -> str:

    """
    Extract text from a PDF.
    """

    file_path = (
        UPLOAD_DIR / filename
    )

    if not file_path.exists():

        raise FileNotFoundError(
            f"File not found: {filename}"
        )

    return extract_text_from_pdf(
        file_path
    )


# =========================================================
# SUMMARIZE PDF
# =========================================================

@mcp.tool()
def summarize_pdf(
    filename: str
) -> str:

    """
    Extract text from PDF
    and summarize using Gemini.
    """

    file_path = (
        UPLOAD_DIR / filename
    )

    if not file_path.exists():

        raise FileNotFoundError(
            f"File not found: {filename}"
        )

    text = extract_text_from_pdf(
        file_path
    )

    if not text.strip():

        return (
            "No text could be extracted "
            "from this PDF."
        )

    return summarize_document(
        text
    )


# =========================================================
# DATABASE TOOLS
# =========================================================

@mcp.tool()
def list_databases() -> list[str]:

    """
    List all MySQL databases.
    """

    try:

        return get_databases()

    except Exception as e:

        return [
            f"Database error: {str(e)}"
        ]


# =========================================================
# LIST TABLES
# =========================================================

@mcp.tool()
def list_tables(
    database_name: str
) -> list[str]:

    """
    List tables in a database.
    """

    try:

        return get_tables(
            database_name
        )

    except Exception as e:

        return [
            f"Database error: {str(e)}"
        ]


# =========================================================
# DESCRIBE TABLE
# =========================================================

@mcp.tool()
def describe_table(
    database_name: str,
    table_name: str
) -> list[dict]:

    """
    Get table structure.
    """

    try:

        return get_table_structure(
            database_name,
            table_name
        )

    except Exception as e:

        return [
            {
                "error": str(e)
            }
        ]


# =========================================================
# GET ROW COUNT
# =========================================================

@mcp.tool()
def get_table_row_count(
    database_name: str,
    table_name: str
) -> int:

    """
    Get number of rows.
    """

    try:

        return get_row_count(
            database_name,
            table_name
        )

    except Exception as e:

        raise Exception(
            f"Database error: {str(e)}"
        )


# =========================================================
# GET SAMPLE DATA
# =========================================================

@mcp.tool()
def get_sample_data(
    database_name: str,
    table_name: str,
    limit: int = 5
) -> dict:

    """
    Get sample data from a table.
    """

    try:

        return db_get_sample_data(
            database_name,
            table_name,
            limit
        )

    except Exception as e:

        return {
            "error": str(e)
        }


# =========================================================
# EXECUTE READ-ONLY SQL
# =========================================================

@mcp.tool()
def execute_read_query(
    database_name: str,
    query: str
) -> dict:

    """
    Execute a read-only SQL query.

    Only SELECT and WITH queries
    should be executed.
    """

    try:

        query_upper = (
            query.strip().upper()
        )

        if not (
            query_upper.startswith("SELECT")
            or query_upper.startswith("WITH")
        ):

            return {
                "error":
                    "Only SELECT and WITH "
                    "queries are allowed."
            }

        return db_execute_read_query(
            database_name,
            query
        )

    except Exception as e:

        return {
            "error": str(e)
        }


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    print(
        "[MCP SERVER] Starting..."
    )

    mcp.run()














# from pathlib import Path

# from mcp.server.fastmcp import FastMCP

# from document_processor import extract_text_from_pdf
# from agent import summarize_document

# from database import (
#     get_databases,
#     get_tables,
#     get_table_structure,
#     get_row_count,
#     get_sample_data as db_get_sample_data,
#     execute_read_query as db_execute_read_query
# )

# # =========================================================
# # MCP SERVER
# # =========================================================

# mcp = FastMCP("Document and Database MCP Server")


# # =========================================================
# # DIRECTORIES
# # =========================================================

# BASE_DIR = Path(__file__).resolve().parent

# UPLOAD_DIR = BASE_DIR / "uploads"

# UPLOAD_DIR.mkdir(exist_ok=True)


# # =========================================================
# # DOCUMENT TOOLS
# # =========================================================

# @mcp.tool()
# def list_documents() -> list[str]:
#     """
#     List all documents in the uploads directory.
#     """

#     return [
#         file.name
#         for file in UPLOAD_DIR.iterdir()
#         if file.is_file()
#     ]


# @mcp.tool()
# def read_pdf(filename: str) -> str:
#     """
#     Extract text from a PDF.
#     """

#     file_path = UPLOAD_DIR / filename

#     if not file_path.exists():
#         raise FileNotFoundError(
#             f"File not found: {filename}"
#         )

#     return extract_text_from_pdf(file_path)


# @mcp.tool()
# def summarize_pdf(filename: str) -> str:
#     """
#     Extract text from PDF and summarize it using Gemini.
#     """

#     file_path = UPLOAD_DIR / filename

#     if not file_path.exists():
#         raise FileNotFoundError(
#             f"File not found: {filename}"
#         )

#     text = extract_text_from_pdf(file_path)

#     if not text.strip():

#         return (
#             "No text could be extracted "
#             "from this PDF."
#         )

#     return summarize_document(text)


# # =========================================================
# # DATABASE TOOLS
# # =========================================================

# @mcp.tool()
# def list_databases() -> list[str]:
#     """
#     List all databases available on the MySQL server.
#     """

#     try:

#         databases = get_databases()

#         return databases

#     except Exception as e:

#         return [
#             f"Database error: {str(e)}"
#         ]


# # =========================================================
# # LIST TABLES
# # =========================================================

# @mcp.tool()
# def list_tables(
#     database_name: str
# ) -> list[str]:
#     """
#     List all tables in a specific database.

#     Example:
#         database_name = "hibernate_student"
#     """

#     try:

#         tables = get_tables(
#             database_name
#         )

#         return tables

#     except Exception as e:

#         return [
#             f"Database error: {str(e)}"
#         ]


# # =========================================================
# # DESCRIBE TABLE
# # =========================================================

# @mcp.tool()
# def describe_table(
#     database_name: str,
#     table_name: str
# ) -> list[dict]:
#     """
#     Get the structure/schema of a table.

#     Returns column name, type, nullable,
#     key, default value and extra information.
#     """

#     try:

#         structure = get_table_structure(
#             database_name,
#             table_name
#         )

#         return structure

#     except Exception as e:

#         return [
#             {
#                 "error": str(e)
#             }
#         ]


# # =========================================================
# # GET TABLE ROW COUNT
# # =========================================================

# @mcp.tool()
# def get_table_row_count(
#     database_name: str,
#     table_name: str
# ) -> int:
#     """
#     Get the number of rows in a table.
#     """

#     try:

#         count = get_row_count(
#             database_name,
#             table_name
#         )

#         return count

#     except Exception as e:

#         raise Exception(
#             f"Database error: {str(e)}"
#         )


# # =========================================================
# # GET SAMPLE DATA
# # =========================================================

# @mcp.tool()
# def get_sample_data(
#     database_name: str,
#     table_name: str,
#     limit: int = 5
# ) -> dict:
#     """
#     Get sample rows from a database table.

#     The default number of rows is 5.
#     Maximum allowed rows is 20.
#     """

#     try:

#         data = db_get_sample_data(
#             database_name,
#             table_name,
#             limit
#         )

#         return data

#     except Exception as e:

#         return {
#             "error": str(e)
#         }


# # =========================================================
# # EXECUTE READ-ONLY SQL QUERY
# # =========================================================

# @mcp.tool()
# def execute_read_query(
#     database_name: str,
#     query: str
# ) -> dict:
#     """
#     Execute a read-only SQL query.

#     Only SELECT and WITH queries are allowed.

#     Example:

#         database_name = "hibernate_student"

#         query = "SELECT * FROM students LIMIT 5"
#     """

#     try:

#         result = db_execute_read_query(
#             database_name,
#             query
#         )

#         return result

#     except Exception as e:

#         return {
#             "error": str(e)
#         }


# # =========================================================
# # START MCP SERVER
# # =========================================================

# if __name__ == "__main__":

#     print(
#         "[MCP SERVER] Starting "
#         "Document and Database MCP Server..."
#     )

#     mcp.run()



