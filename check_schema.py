import psycopg2
from psycopg2.extras import RealDictCursor

def check_schema():
    conn = psycopg2.connect(
        "postgresql://stephen:qwerty@localhost:5432/open_heavens_db",
        cursor_factory=RealDictCursor
    )
    
    try:
        with conn.cursor() as cur:
            # Get column information
            cur.execute("""
                SELECT column_name, data_type, character_maximum_length
                FROM information_schema.columns
                WHERE table_name = 'open_heavens_teenagers'
                ORDER BY ordinal_position;
            """)
            columns = cur.fetchall()
            
            print("\nTable: open_heavens_teenagers")
            print("Columns:")
            for col in columns:
                print(f"- {col['column_name']}: {col['data_type']}", end='')
                if col['character_maximum_length']:
                    print(f"({col['character_maximum_length']})")
                else:
                    print()
                    
    finally:
        conn.close()

if __name__ == "__main__":
    check_schema()