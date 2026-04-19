import sqlite3

DB_NAME = "students.db"

def run_query(query):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(query)

        # ✅ SELECT
        if query.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            conn.close()

            return {
                "type": "select",
                "data": rows,
                "columns": columns
            }

        # ✅ INSERT / UPDATE / DELETE
        else:
            conn.commit()   # 🔥 IMPORTANT FIX
            affected = cursor.rowcount

            conn.close()

            return {
                "type": "action",
                "rows": affected
            }

    except Exception as e:
        return {
            "type": "error",
            "message": str(e)
        }
    