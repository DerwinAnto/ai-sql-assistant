from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import pandas as pd
import sqlite3
import os

from backend.llm_sql import text_to_sql
from backend.execute import run_query
from backend.security import is_safe_query

app = FastAPI()

# ✅ Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = "students.db"

# 🌍 GLOBAL STATE
table_name = "uploaded_data"
columns = []

# ✅ CHECK TABLE EXISTS
def table_exists():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,)
    )

    exists = cursor.fetchone() is not None
    conn.close()
    return exists


# ✅ UPLOAD CSV
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global columns

    try:
        file_path = file.filename

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Read CSV
        df = pd.read_csv(file_path)

        if df.empty:
            return {"message": "❌ Uploaded file is empty"}

        # Store columns
        columns = list(df.columns)

        # Save to DB
        conn = sqlite3.connect(DB_NAME)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.close()

        return {
            "message": "✅ File uploaded successfully",
            "columns": columns
        }

    except Exception as e:
        return {"message": f"❌ Upload error: {str(e)}"}


# ✅ QUERY API
@app.post("/query")
async def query(data: dict):
    user_input = data["question"]

    sql_query = text_to_sql(user_input, table_name, columns)

    sql_lower = sql_query.lower()

    # 🔥 HARD BLOCK (IMPORTANT)
    if "drop" in sql_lower or "truncate" in sql_lower or "alter" in sql_lower:
        return {
            "sql": sql_query,
            "result": {
                "type": "error",
                "message": "❌ Dangerous query BLOCKED"
            }
        }

    # Optional: block full delete
    if "delete" in sql_lower and "where" not in sql_lower:
        return {
            "sql": sql_query,
            "result": {
                "type": "error",
                "message": "❌ BLOCKED.Use WHERE condition."
            }
        }

    result = run_query(sql_query)

    return {
        "sql": sql_query,
        "result": result
    }