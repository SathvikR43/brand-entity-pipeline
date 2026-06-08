import psycopg2
from config.settings import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def test_connection():
    try:
        conn = get_connection()
        print("✅ Database connection successful!")
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    test_connection()