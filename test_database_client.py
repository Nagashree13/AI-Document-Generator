import asyncio

from mcp_client import (
    list_databases,
    list_tables,
    describe_table,
    get_row_count,
    get_sample_data,
    execute_read_query
)


async def main():

    # ==========================================
    # 1. LIST DATABASES
    # ==========================================

    print("\n==============================")
    print("DATABASES")
    print("==============================")

    databases = await list_databases()

    print(databases)


    # ==========================================
    # 2. LIST TABLES
    # ==========================================

    database_name = "hibernate_student"

    print("\n==============================")
    print("TABLES")
    print("==============================")

    tables = await list_tables(database_name)

    print(tables)


    # ==========================================
    # 3. DESCRIBE TABLE
    # ==========================================

    if tables:

        # Change this if you want a specific table
        table_name = tables[0]

        print("\n==============================")
        print("TABLE STRUCTURE")
        print("==============================")

        structure = await describe_table(
            database_name,
            table_name
        )

        print(structure)


        # ==========================================
        # 4. ROW COUNT
        # ==========================================

        print("\n==============================")
        print("ROW COUNT")
        print("==============================")

        count = await get_row_count(
            database_name,
            table_name
        )

        print(count)


        # ==========================================
        # 5. SAMPLE DATA
        # ==========================================

        print("\n==============================")
        print("SAMPLE DATA")
        print("==============================")

        sample = await get_sample_data(
            database_name,
            table_name,
            5
        )

        print(sample)


    # ==========================================
    # 6. SQL QUERY
    # ==========================================

    print("\n==============================")
    print("SQL QUERY")
    print("==============================")

    result = await execute_read_query(
        database_name,
        "SELECT * FROM students LIMIT 5"
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())