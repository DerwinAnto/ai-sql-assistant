def is_safe(query):
    dangerous_words = ["DROP", "DELETE", "TRUNCATE", "--"]

    for word in dangerous_words:
        if word in query.upper():
            return False
    return True