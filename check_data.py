import psycopg2
import requests
from datetime import datetime

# Supabase configuration
SUPABASE_URL = "https://vhqbtwmvteemgfsebvff.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZocWJ0d212dGVlbWdmc2VidmZmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDUwNDgwODUsImV4cCI6MjAyMDYyNDA4NX0.xC_D4_2MXG5Cb97cG-wUwESz32MDDBbeZ-dJIEhq4w8"

# PostgreSQL configuration
DB_NAME = "open_heavens_db"
DB_USER = "stephen"
DB_PASSWORD = "qwerty"
DB_HOST = "localhost"
DB_PORT = "5432"

def fetch_data(table_name):
    """Fetch data from Supabase REST API"""
    print(f"\nFetching data from {table_name}...")
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    
    url = f"{SUPABASE_URL}/rest/v1/{table_name}"
    print(f"URL: {url}")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Successfully fetched {len(data)} records from {table_name}")
        if not data:
            print(f"Warning: No data found in {table_name}")
        return data
    else:
        print(f"Error fetching data from {table_name}: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def count_rows(cursor, table_name):
    """Count rows in a table"""
    try:
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
        count = cursor.fetchone()[0]
        print(f"Records in {table_name}: {count}")
        return count
    except Exception as e:
        print(f"Error counting rows in {table_name}: {str(e)}")
        return 0

def check_table_schema(cursor, table_name):
    """Check table schema"""
    try:
        cursor.execute(f"""
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        print(f"\nSchema for {table_name}:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]}" + (f"({col[2]})" if col[2] else ""))
    except Exception as e:
        print(f"Error checking schema for {table_name}: {str(e)}")

def main():
    try:
        # Connect to PostgreSQL
        print("\nConnecting to PostgreSQL...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()
        
        # List of tables to check
        tables = [
            "hymns",
            "open_heavens",
            "open_heavens_teenagers",
            "prayer_requests",
            "comments",
            "likes"
        ]
        
        print("\n=== Checking Current Database State ===")
        for table in tables:
            count_rows(cursor, table)
            check_table_schema(cursor, table)
        
        print("\n=== Checking Supabase Data ===")
        for table in tables:
            data = fetch_data(table)
            if data:
                print(f"Sample data from {table}:")
                sample = data[0] if data else None
                if sample:
                    print(f"  First record keys: {list(sample.keys())}")
                    print(f"  First record ID: {sample.get('id')}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()