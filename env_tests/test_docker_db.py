import psycopg2

print("Checking connection to Docker SQL database...")

try:
    # This connects to the 'postgres' database we started in Docker
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        # Use your local DB password here; do not commit actual credentials.
        password="REDACTED" 
    )
    print("--- SUCCESS ---")
    print("Python is talking to the Docker SQL Database!")
    conn.close()
except Exception as e:
    print(f"--- CONNECTION FAILED ---")
    print(f"Error: {e}")
    print("\nTip: Make sure Docker Desktop is open and the whale is green!")
    