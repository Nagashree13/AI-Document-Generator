import sys
import ast
from pathlib import Path

from mcp import (
    ClientSession,
    StdioServerParameters
)

from mcp.client.stdio import stdio_client


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

MCP_SERVER = BASE_DIR / "mcp_server.py"


# =========================================================
# CREATE MCP SERVER PARAMETERS
# =========================================================

def get_server_params():

    return StdioServerParameters(
        command=sys.executable,
        args=[
            str(MCP_SERVER)
        ]
    )


# =========================================================
# EXTRACT TEXT FROM MCP RESULT
# =========================================================

# def extract_result_text(result):

#     output = ""

#     for content in result.content:

#         if hasattr(content, "text"):

#             output += content.text

#     return output.strip()


def extract_result_text(result):

    output = []

    for content in result.content:

        if hasattr(content, "text"):

            output.append(content.text)

    return "\n".join(output).strip()


# =========================================================
# PARSE LIST RESPONSE
# =========================================================

def parse_list_response(text):

    """
    Convert MCP string response into a Python list.

    Example:

    "['data', 'mysql', 'sys']"

    becomes:

    ['data', 'mysql', 'sys']
    """

    if not text:
        return []


    text = text.strip()


    # -----------------------------------------------------
    # Try Python list
    # -----------------------------------------------------

    try:

        value = ast.literal_eval(text)

        if isinstance(value, list):

            return [
                str(item).strip()
                for item in value
                if str(item).strip()
            ]

    except Exception:
        pass


    # -----------------------------------------------------
    # Try JSON
    # -----------------------------------------------------

    try:

        import json

        value = json.loads(text)

        if isinstance(value, list):

            return [
                str(item).strip()
                for item in value
                if str(item).strip()
            ]

    except Exception:
        pass


    # -----------------------------------------------------
    # Try newline separated values
    # -----------------------------------------------------

    values = []

    for line in text.splitlines():

        line = line.strip()

        if line:

            values.append(line)


    if values:

        return values


    # -----------------------------------------------------
    # Fallback
    # -----------------------------------------------------

    return [text]


# =========================================================
# SUMMARIZE PDF
# =========================================================

async def summarize_pdf(
    filename: str
) -> str:

    print(
        "\n[CLIENT] Starting MCP server..."
    )

    server_params = get_server_params()

    async with stdio_client(
        server_params
    ) as (read, write):

        print(
            "[CLIENT] Connected to MCP server"
        )

        async with ClientSession(
            read,
            write
        ) as session:

            await session.initialize()

            print(
                "[CLIENT] MCP session initialized"
            )

            result = await session.call_tool(
                "summarize_pdf",
                arguments={
                    "filename": filename
                }
            )

            return extract_result_text(
                result
            )


# =========================================================
# LIST DATABASES
# =========================================================

async def list_databases():

    print(
        "\n[CLIENT] Getting databases..."
    )

    server_params = get_server_params()

    async with stdio_client(
        server_params
    ) as (read, write):

        print(
            "[CLIENT] MCP server started"
        )

        async with ClientSession(
            read,
            write
        ) as session:

            await session.initialize()

            print(
                "[CLIENT] MCP session initialized"
            )

            result = await session.call_tool(
                "list_databases",
                arguments={}
            )

            text = extract_result_text(
                result
            )

            print(
                f"[CLIENT] Raw databases: {text}"
            )

            databases = parse_list_response(
                text
            )

            print(
                f"[CLIENT] Parsed databases: "
                f"{databases}"
            )

            return databases


# =========================================================
# LIST TABLES
# =========================================================

# async def list_tables(
#     database_name: str
# ):

#     print(
#         f"\n[CLIENT] Getting tables "
#         f"from {database_name}"
#     )

#     server_params = get_server_params()

#     async with stdio_client(
#         server_params
#     ) as (read, write):

#         async with ClientSession(
#             read,
#             write
#         ) as session:

#             await session.initialize()

#             result = await session.call_tool(
#                 "list_tables",
#                 arguments={
#                     "database_name":
#                         database_name
#                 }
#             )

#             text = extract_result_text(
#                 result
#             )

#             print(
#                 f"[CLIENT] Raw tables: {text}"
#             )

#             return parse_list_response(
#                 text
#             ) 

async def list_tables(
    database_name: str
):
    if isinstance(database_name, list):
        raise ValueError(
            "database_name must be a single database name, not a list."
        )

    database_name = str(database_name).strip()

    if not database_name:
        raise ValueError(
            "Database name cannot be empty."
        )

    print(
        f"\n[CLIENT] Getting tables from {database_name}"
    )

    server_params = get_server_params()

    async with stdio_client(
        server_params
    ) as (read, write):

        async with ClientSession(
            read,
            write
        ) as session:

            await session.initialize()

            result = await session.call_tool(
                "list_tables",
                arguments={
                    "database_name": database_name
                }
            )

            text = extract_result_text(result)

            print(
                f"[CLIENT] Raw tables: {text}"
            )

            return parse_list_response(text)


# =========================================================
# DESCRIBE TABLE
# =========================================================

async def describe_table(
    database_name: str,
    table_name: str
) -> str:

    print(
        f"\n[CLIENT] Describing "
        f"{database_name}.{table_name}"
    )

    server_params = get_server_params()

    async with stdio_client(
        server_params
    ) as (read, write):

        async with ClientSession(
            read,
            write
        ) as session:

            await session.initialize()

            result = await session.call_tool(
                "describe_table",
                arguments={
                    "database_name":
                        database_name,

                    "table_name":
                        table_name
                }
            )

            return extract_result_text(
                result
            )


# =========================================================
# GET ROW COUNT
# =========================================================

async def get_row_count(
    database_name: str,
    table_name: str
) -> str:

    print(
        f"\n[CLIENT] Getting row count "
        f"for {database_name}.{table_name}"
    )

    server_params = get_server_params()

    async with stdio_client(
        server_params
    ) as (read, write):

        async with ClientSession(
            read,
            write
        ) as session:

            await session.initialize()

            result = await session.call_tool(
                "get_table_row_count",
                arguments={
                    "database_name":
                        database_name,

                    "table_name":
                        table_name
                }
            )

            return extract_result_text(
                result
            )


# =========================================================
# GET SAMPLE DATA
# =========================================================

async def get_sample_data(
    database_name: str,
    table_name: str,
    limit: int = 5
) -> str:

    print(
        f"\n[CLIENT] Getting sample data "
        f"from {database_name}.{table_name}"
    )

    server_params = get_server_params()

    async with stdio_client(
        server_params
    ) as (read, write):

        async with ClientSession(
            read,
            write
        ) as session:

            await session.initialize()

            result = await session.call_tool(
                "get_sample_data",
                arguments={
                    "database_name":
                        database_name,

                    "table_name":
                        table_name,

                    "limit":
                        limit
                }
            )

            return extract_result_text(
                result
            )


# =========================================================
# EXECUTE READ-ONLY SQL QUERY
# =========================================================

async def execute_read_query(
    database_name: str,
    query: str
) -> str:

    print(
        "\n[CLIENT] Executing SQL query..."
    )

    print(
        f"[CLIENT] Database: "
        f"{database_name}"
    )

    print(
        f"[CLIENT] Query: {query}"
    )

    server_params = get_server_params()

    async with stdio_client(
        server_params
    ) as (read, write):

        print(
            "[CLIENT] MCP server started"
        )

        async with ClientSession(
            read,
            write
        ) as session:

            await session.initialize()

            print(
                "[CLIENT] MCP session initialized"
            )

            result = await session.call_tool(
                "execute_read_query",
                arguments={
                    "database_name":
                        database_name,

                    "query":
                        query
                }
            )

            print(
                "[CLIENT] SQL result received"
            )

            return extract_result_text(
                result
            )