import sqlite3

DB_NAME = "students.db"

def run_query(query):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(query)

        if query.lower().startswith("select"):
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            conn.close()

            return {
                "type": "select",
                "columns": columns,
                "data": data
            }

        else:
            conn.commit()
            rows = cursor.rowcount
            conn.close()

            return {
                "type": "action",
                "rows": rows
            }

    except Exception as e:
        conn.close()
        return {
            "type": "error",
            "message": str(e) 
        }