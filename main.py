from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import pandas as pd
import sqlite3

from llm_sql import text_to_sql
from execute import run_query

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

# 🌍 GLOBAL VARIABLE (important)
table_name = "uploaded_data"
columns = []

# ✅ UPLOAD CSV
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global columns

    file_path = file.filename

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Read CSV
    df = pd.read_csv(file_path)

    # Store column names
    columns = list(df.columns)

    # Save into SQLite
    conn = sqlite3.connect(DB_NAME)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    return {"message": "File uploaded successfully", "columns": columns}


# ✅ QUERY API
@app.post("/query")
async def query(data: dict):
    user_input = data["question"]

    # 🔥 Pass table + columns to LLM
    sql_query = text_to_sql(user_input, table_name, columns)

    result = run_query(sql_query)

    return {
        "sql": sql_query,
        "result": result
    }