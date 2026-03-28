from fastapi import FastAPI
from pydantic import BaseModel
from llm_sql import text_to_sql
from execute import run_query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.post("/query")
def get_query(data: Query):
    sql = text_to_sql(data.question)
    result = run_query(sql)
    return {"sql": sql, "result": result}