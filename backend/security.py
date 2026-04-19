def is_safe_query(sql: str):
    sql_lower = sql.lower()

    # ❌ Completely block dangerous operations
    blocked_keywords = [
        "drop",
        "truncate",
        "alter",
        "delete table",
        "drop table"
    ]

    for word in blocked_keywords:
        if word in sql_lower:
            return False

    return True