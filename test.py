from llm_sql import text_to_sql
from execute import run_query
from voice_input import get_voice_input

print("1. Type input")
print("2. Voice input")

choice = input("Choose option (1 or 2): ")

if choice == "1":
    user_input = input("Ask something: ")

elif choice == "2":
    user_input = get_voice_input()

else:
    print("Invalid choice")
    exit()

sql_query = text_to_sql(user_input)
print("\nGenerated SQL:\n", sql_query)

result = run_query(sql_query)
print("\nResult:\n", result)