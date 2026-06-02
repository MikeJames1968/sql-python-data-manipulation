import os
from dotenv import load_dotenv
import psycopg

# 1. Load the variables from your local .env file
load_dotenv()

# 2. Grab the connection string
db_url = os.environ.get("DATABASE_URL")

try:
    # 3. Establish the connection to Docker
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            # Run a dummy query to test the connection
            cur.execute("SELECT version();")
            db_version = cur.fetchone()
            print("🚀 Successfully connected to Docker PostgreSQL!")
            print(f"Database version: {db_version[0]}")

except Exception as e:
    print(f"❌ Connection failed: {e}")