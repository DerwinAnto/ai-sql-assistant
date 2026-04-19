from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

def text_to_sql(user_input, table_name, columns):

    prompt = f"""
You are an SQL expert.

Table: {table_name}
Columns: {columns}

STRICT RULES:
1. Return ONLY SQL query
2. DO NOT explain
3. DO NOT use SELECT instead of DELETE
4. If user says delete, use DELETE query
5. If user says update, use UPDATE query
6. If user says insert, use INSERT query

Examples:

User: show all students
SQL: SELECT * FROM {table_name};

User: delete id 10
SQL: DELETE FROM {table_name} WHERE id = 10;

User: update name to John where id 1
SQL: UPDATE {table_name} SET name='John' WHERE id=1;

User: insert into students
SQL: INSERT INTO {table_name} VALUES (...);

Now convert:

User: {user_input}
SQL:
"""

    response = llm.invoke(prompt)

    # 🔥 CLEAN OUTPUT (VERY IMPORTANT)
    sql = response.strip()

    # remove ```sql ```
    if "```" in sql:
        sql = sql.split("```")[1]

    sql = sql.replace("sql", "").strip()

    return sql