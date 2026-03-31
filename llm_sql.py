from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

def text_to_sql(user_input, table_name, columns):

    column_str = ", ".join(columns)

    prompt = f"""
You are an expert SQL generator.

Database table name: {table_name}
Columns: {column_str}

Rules:
- Use ONLY this table
- Do not guess table names
- Do not explain anything
- Return ONLY SQL query

User question:
{user_input} 
"""

    response = llm.invoke(prompt)

    return response.strip()