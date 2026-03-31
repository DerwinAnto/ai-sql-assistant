from backend.llm_sql import text_to_sql
from backend.execute import run_query

while True:
    user_input = input("Ask something: ")

    sql_query = text_to_sql(user_input)
    print("Generated SQL:", sql_query)

    result = run_query(sql_query)
    print("Result:", result)