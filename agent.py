import os
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from dotenv import load_dotenv
import google.generativeai as genai

from document_processor import extract_text_from_pdf
from prompts import SQL_GENERATION_PROMPT


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# CONFIGURE GEMINI
# =========================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-3.6-flash")


# =========================================================
# FASTAPI
# =========================================================

app = FastAPI()


# =========================================================
# DIRECTORIES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(exist_ok=True)


# =========================================================
# DOCUMENT SUMMARIZATION
# =========================================================

def summarize_document(text: str) -> str:

    prompt = f"""
You are a document analysis assistant.

Analyze the following document and provide a clear summary.

Document:
{text}

Provide:

1. A short summary
2. Key points
3. Important information
"""

    response = model.generate_content(prompt)

    return response.text.strip()


# =========================================================
# PDF SUMMARIZATION ENDPOINT
# =========================================================

@app.post("/summarize")
async def summarize_pdf(
    file: UploadFile = File(...)
):

    try:

        file_path = UPLOAD_DIR / file.filename

        # Save uploaded file
        with open(file_path, "wb") as buffer:

            buffer.write(
                await file.read()
            )

        # Extract text
        text = extract_text_from_pdf(
            file_path
        )

        if not text.strip():

            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the PDF."
            )

        # Generate summary
        summary = summarize_document(
            text
        )

        return {
            "filename": file.filename,
            "summary": summary
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# GENERATE SQL
# =========================================================

def generate_sql(
    question: str,
    schema: str
) -> str:

    prompt = SQL_GENERATION_PROMPT.format(
        schema=schema,
        question=question
    )

    response = model.generate_content(
        prompt
    )

    sql = response.text.strip()

    # Remove Gemini markdown fences
    sql = sql.replace(
        "```sql",
        ""
    )

    sql = sql.replace(
        "```SQL",
        ""
    )

    sql = sql.replace(
        "```",
        ""
    )

    return sql.strip()


# =========================================================
# GENERATE NATURAL LANGUAGE ANSWER
# =========================================================

def generate_answer(
    question: str,
    sql: str,
    result
) -> str:

    prompt = f"""
You are a database assistant.

User question:
{question}

SQL query:
{sql}

Database result:
{result}

Answer the user's question using ONLY the database result.

Rules:

1. Give a clear and simple answer.
2. Do not make up information.
3. Do not unnecessarily explain the SQL query.
4. Do not return SQL unless the user asks for SQL.
5. If no matching data was found, clearly say so.
6. If the result contains rows, summarize them clearly.
"""

    response = model.generate_content(
        prompt
    )

    return response.text.strip()


# =========================================================
# ANSWER DATABASE QUESTION
# =========================================================

async def answer_database_question(
    question: str,
    database: str,
    schema: str
) -> str:

    # -----------------------------------------------------
    # STEP 1: Generate SQL
    # -----------------------------------------------------

    sql = generate_sql(
        question,
        schema
    )

    print(
        "\n[AGENT] Generated SQL:"
    )

    print(sql)


    # -----------------------------------------------------
    # SAFETY CHECK
    # -----------------------------------------------------

    sql_upper = sql.strip().upper()

    if not (
        sql_upper.startswith("SELECT")
        or sql_upper.startswith("WITH")
    ):

        return (
            "I can only execute "
            "read-only SELECT queries."
        )


    # -----------------------------------------------------
    # STEP 2: Execute SQL through MCP
    # -----------------------------------------------------

    from mcp_client import execute_read_query

    result = await execute_read_query(
        database_name=database,
        query=sql
    )

    print(
        "\n[AGENT] Database result:"
    )

    print(result)


    # -----------------------------------------------------
    # STEP 3: Generate natural language answer
    # -----------------------------------------------------

    answer = generate_answer(
        question,
        sql,
        result
    )

    return answer










# import os
# from pathlib import Path
# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.responses import JSONResponse
# from dotenv import load_dotenv
# import google.generativeai as genai
# from document_processor import extract_text_from_pdf  
# from prompts  import SQL_GENERATION_PROMPT

# # Load environment variables
# load_dotenv()

# # Configure Gemini API
# api_key = os.getenv("GEMINI_API_KEY")
# genai.configure(api_key=api_key)
# model = genai.GenerativeModel("gemini-3.6-flash")

# # Initialize FastAPI app
# app = FastAPI()

# # Directory for uploads
# BASE_DIR = Path(__file__).resolve().parent
# UPLOAD_DIR = BASE_DIR / "uploads"
# UPLOAD_DIR.mkdir(exist_ok=True)

# # Function to summarize a document
# def summarize_document(text):
#     prompt = f"""
# You are a document analysis assistant.

# Analyze the following document and provide a clear summary.

# Document:
# {text}

# Provide:
# 1. A short summary
# 2. Key points
# 3. Important information
# """
#     response = model.generate_content(prompt)
#     return response.text

# # MCP endpoint for PDF summarization
# @app.post("/summarize")
# async def summarize_pdf(file: UploadFile = File(...)):
#     try:
#         # Save uploaded file
#         file_path = UPLOAD_DIR / file.filename
#         with open(file_path, "wb") as buffer:
#             buffer.write(await file.read())

#         # Extract text from PDF
#         text = extract_text_from_pdf(file_path)

#         # Generate summary using Gemini
#         summary = summarize_document(text)

#         return {"filename": file.filename, "summary": summary}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))  
    


# def generate_sql(question, schema):

#     prompt = SQL_GENERATION_PROMPT.format(
#         schema=schema,
#         question=question
#     )

#     response = model.generate_content(prompt)

#     sql = response.text.strip()

#     # Remove markdown fences if Gemini returns them
#     sql = sql.replace("```sql", "")
#     sql = sql.replace("```", "")

#     return sql.strip()