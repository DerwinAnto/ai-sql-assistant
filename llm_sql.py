from langchain_community.llms import Ollama
import re

llm = Ollama(model="llama3")

def extract_sql(text):
    match = re.search(r"```sql(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    match = re.search(r"(SELECT .*?;)", text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()

    return text.strip()

def text_to_sql(user_input):
    prompt = f"""
    You are an SQL generator.

    Rules:
    - Output ONLY SQL
    - No explanation
    - No text
    - No markdown

    Table: students(id, name, age, grade)

    Input: {user_input}
    """

    response = llm.invoke(prompt)
    clean_sql = extract_sql(response)

    return clean_sql