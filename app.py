import os
from pathlib import Path

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel
from dotenv import load_dotenv

import google.generativeai as genai


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# CONFIGURE GEMINI
# =========================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set in .env"
    )

genai.configure(
    api_key=api_key
)

model = genai.GenerativeModel(
    "gemini-3.6-flash"
)


# =========================================================
# MCP CLIENT
# =========================================================

from mcp_client import (
    summarize_pdf,
    list_databases,
    list_tables,
    describe_table
)


# =========================================================
# AGENT
# =========================================================

from agent import answer_database_question


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Document AI Agent",
    description=(
        "Document summarization and "
        "database question answering using MCP"
    ),
    version="2.0.0"
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
# STATIC FILES
# =========================================================

app.mount(
    "/static",
    StaticFiles(
        directory=BASE_DIR / "static"
    ),
    name="static"
)


# =========================================================
# DATABASE QUESTION MODEL
# =========================================================

class DatabaseQuestion(BaseModel):

    question: str

    database: str


# =========================================================
# CLEAR UPLOADED FILES
# =========================================================

def clear_uploaded_files():

    """
    Delete all files from uploads directory.
    """

    for file in UPLOAD_DIR.iterdir():

        if file.is_file():

            try:

                file.unlink()

                print(
                    f"[FASTAPI] Deleted old file: "
                    f"{file.name}"
                )

            except Exception as e:

                print(
                    f"[FASTAPI] Could not delete "
                    f"{file.name}: {e}"
                )


# =========================================================
# BUILD DATABASE SCHEMA
# =========================================================

async def build_database_schema(
    database_name: str
) -> str:

    """
    Get all tables and their structures
    through the MCP server and build a
    schema string for Gemini.
    """

    print(
        f"\n[FASTAPI] Building schema for: "
        f"{database_name}"
    )

    # -----------------------------------------------------
    # Validate database name
    # -----------------------------------------------------

    if not isinstance(
        database_name,
        str
    ):

        raise ValueError(
            "Database name must be a string."
        )

    database_name = database_name.strip()

    if not database_name:

        raise ValueError(
            "Database name cannot be empty."
        )

    # -----------------------------------------------------
    # Get tables through MCP
    # -----------------------------------------------------

    tables = await list_tables(
        database_name
    )

    print(
        f"[FASTAPI] Tables received: "
        f"{tables}"
    )

    # -----------------------------------------------------
    # Make sure MCP returned a list
    # -----------------------------------------------------

    if not isinstance(
        tables,
        list
    ):

        raise ValueError(
            "MCP did not return a valid "
            "table list."
        )

    # -----------------------------------------------------
    # Remove empty values and errors
    # -----------------------------------------------------

    cleaned_tables = []

    for table in tables:

        table = str(table).strip()

        if not table:
            continue

        if table.lower().startswith(
            "database error:"
        ):
            continue

        cleaned_tables.append(
            table
        )

    tables = cleaned_tables

    # -----------------------------------------------------
    # Check whether tables exist
    # -----------------------------------------------------

    if not tables:

        return (
            f"Database '{database_name}' "
            "does not contain any accessible tables."
        )

    # -----------------------------------------------------
    # Build schema
    # -----------------------------------------------------

    schema_parts = []

    schema_parts.append(
        f"Database: {database_name}"
    )

    schema_parts.append("")

    # -----------------------------------------------------
    # Get structure of every table
    # -----------------------------------------------------

    for table_name in tables:

        print(
            f"[FASTAPI] Getting structure for "
            f"table: {table_name}"
        )

        try:

            structure_text = await describe_table(
                database_name,
                table_name
            )

            # Ignore MCP database errors
            if (
                isinstance(
                    structure_text,
                    str
                )
                and structure_text.lower().startswith(
                    "database error:"
                )
            ):

                print(
                    f"[FASTAPI] Error describing "
                    f"{table_name}: "
                    f"{structure_text}"
                )

                continue

            schema_parts.append(
                f"Table: {table_name}"
            )

            schema_parts.append(
                f"Columns: {structure_text}"
            )

            schema_parts.append("")

        except Exception as e:

            print(
                f"[FASTAPI] Could not describe "
                f"{table_name}: {e}"
            )

            continue

    # -----------------------------------------------------
    # Final schema
    # -----------------------------------------------------

    schema = "\n".join(
        schema_parts
    )

    print(
        "\n[FASTAPI] Generated database schema:"
    )

    print(
        schema
    )

    return schema


# =========================================================
# HOME PAGE
# =========================================================

@app.get("/")
async def serve_index():

    """
    Open the home page.

    Previously uploaded files are
    deleted when the page is refreshed.
    """

    clear_uploaded_files()

    return FileResponse(
        BASE_DIR
        / "templates"
        / "index.html"
    )


# =========================================================
# UPLOAD DOCUMENT
# =========================================================

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    try:

        # -------------------------------------------------
        # Validate filename
        # -------------------------------------------------

        if not file.filename:

            raise HTTPException(
                status_code=400,
                detail="No file selected."
            )

        # -------------------------------------------------
        # Check file type
        # -------------------------------------------------

        if not file.filename.lower().endswith(
            ".pdf"
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only PDF files are supported."
                )
            )

        # -------------------------------------------------
        # Secure filename
        # -------------------------------------------------

        filename = Path(
            file.filename
        ).name

        file_path = (
            UPLOAD_DIR / filename
        )

        # -------------------------------------------------
        # Save file
        # -------------------------------------------------

        with open(
            file_path,
            "wb"
        ) as buffer:

            buffer.write(
                await file.read()
            )

        print(
            f"\n[FASTAPI] File uploaded: "
            f"{filename}"
        )

        # -------------------------------------------------
        # Call MCP
        # -------------------------------------------------

        print(
            "[FASTAPI] Calling MCP client..."
        )

        summary = await summarize_pdf(
            filename
        )

        print(
            "[FASTAPI] Summary received"
        )

        # -------------------------------------------------
        # Return result
        # -------------------------------------------------

        return {
            "success": True,
            "filename": filename,
            "summary": summary
        }

    except HTTPException:

        raise

    except Exception as e:

        print(
            f"[FASTAPI] Upload error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"An error occurred: {str(e)}"
            )
        )


# =========================================================
# LIST DATABASES
# =========================================================

@app.get("/databases")
async def get_databases():

    try:

        print(
            "\n[FASTAPI] Requesting databases "
            "from MCP..."
        )

        databases = await list_databases()

        print(
            f"[FASTAPI] Databases received: "
            f"{databases}"
        )

        # -------------------------------------------------
        # Make sure databases is a list
        # -------------------------------------------------

        if not isinstance(
            databases,
            list
        ):

            raise ValueError(
                "MCP did not return a valid "
                "database list."
            )

        # -------------------------------------------------
        # Clean database names
        # -------------------------------------------------

        cleaned_databases = []

        for database in databases:

            database = str(
                database
            ).strip()

            if not database:
                continue

            if database.lower().startswith(
                "database error:"
            ):
                continue

            cleaned_databases.append(
                database
            )

        return {
            "success": True,
            "databases": cleaned_databases
        }

    except Exception as e:

        print(
            f"[FASTAPI] Database error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# DATABASE QUESTION
# =========================================================

@app.post("/database-question")
async def database_question(
    request: DatabaseQuestion
):

    """
    Answer a natural-language question
    about a MySQL database.

    Example:

    {
        "question": "How many students are there?",
        "database": "hibernate_student"
    }
    """

    try:

        # -------------------------------------------------
        # Validate question
        # -------------------------------------------------

        question = request.question.strip()

        database = request.database.strip()

        if not question:

            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty."
            )

        if not database:

            raise HTTPException(
                status_code=400,
                detail="Database cannot be empty."
            )

        # -------------------------------------------------
        # Make sure database is a single string
        # -------------------------------------------------

        if isinstance(
            database,
            list
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Please select one database. "
                    "Multiple databases cannot be "
                    "sent at once."
                )
            )

        print(
            "\n======================================"
        )

        print(
            "[FASTAPI] DATABASE QUESTION"
        )

        print(
            "======================================"
        )

        print(
            f"[FASTAPI] Database: {database}"
        )

        print(
            f"[FASTAPI] Question: {question}"
        )

        # -------------------------------------------------
        # STEP 1
        # Build database schema
        # -------------------------------------------------

        schema = await build_database_schema(
            database
        )

        if not schema.strip():

            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not retrieve "
                    "database schema."
                )
            )

        print(
            "\n[FASTAPI] Schema successfully built."
        )

        # -------------------------------------------------
        # STEP 2
        # Send question to agent
        # -------------------------------------------------

        answer = await answer_database_question(
            question=question,
            database=database,
            schema=schema
        )

        # -------------------------------------------------
        # STEP 3
        # Return answer
        # -------------------------------------------------

        print(
            "\n[FASTAPI] Final answer:"
        )

        print(
            answer
        )

        return {
            "success": True,
            "question": question,
            "database": database,
            "answer": answer
        }

    except HTTPException:

        raise

    except Exception as e:

        print(
            f"[FASTAPI] Database question "
            f"error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"An error occurred: {str(e)}"
            )
        )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health_check():

    return {
        "status": "ok",
        "message": "Document AI Agent is running."
    }