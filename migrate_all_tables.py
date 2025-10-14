import psycopg2
import requests
import json
import time
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
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    print(f"Attempting to fetch {table_name} from Supabase...")
    url = f"{SUPABASE_URL}/rest/v1/{table_name}?select=*"
    print(f"URL: {url}")
    
    retries = 3
    while retries > 0:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Response headers: {response.headers}")
            if response.status_code != 200:
                print(f"Error fetching data from {table_name}: {response.status_code}")
                try:
                    print(response.json())
                except:
                    print(f"Raw response: {response.text}")
            return response.json() if response.status_code == 200 else None
        except requests.RequestException as e:
            print(f"Error making request (retries left: {retries-1}): {str(e)}")
            retries -= 1
            if retries > 0:
                print("Waiting 5 seconds before retrying...")
                time.sleep(5)
            else:
                print("All retries exhausted")
                raise e
    return None

def create_tables(cursor):
    """Create all necessary tables"""
    # Create hymns table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hymns (
            id INTEGER PRIMARY KEY,
            hymn_title TEXT NOT NULL,
            hymn_verse TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE
        )
    """)

    # Create open_heavens table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS open_heavens (
            id INTEGER PRIMARY KEY,
            topic TEXT,
            memory_verse TEXT,
            bible_reading TEXT,
            message TEXT,
            action_point TEXT,
            created_at TIMESTAMP WITH TIME ZONE,
            hymn_id INTEGER REFERENCES hymns(id),
            date DATE,
            bible_reading_text TEXT,
            action_type TEXT,
            bible1_year TEXT,
            bible1_year_text TEXT
        )
    """)

    # Create open_heavens_teenagers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS open_heavens_teenagers (
            id INTEGER PRIMARY KEY,
            topic TEXT,
            memory_verse TEXT,
            bible_reading TEXT,
            message TEXT,
            action_text TEXT,
            created_at TIMESTAMP WITH TIME ZONE,
            hymnal_id INTEGER REFERENCES hymns(id),
            title TEXT,
            date DATE,
            memories TEXT,
            read TEXT,
            hymn_title TEXT,
            hymn TEXT,
            bible_in_one_year_verse TEXT,
            bible_in_one_year TEXT,
            action_types TEXT
        )
    """)

    # Create prayer_requests table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prayer_requests (
            id INTEGER PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE,
            disabled BOOLEAN DEFAULT FALSE,
            name TEXT,
            user_ref TEXT,
            request_content TEXT
        )
    """)

    # Create comments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY,
            comment TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE,
            open_heavens_id INTEGER REFERENCES open_heavens(id)
        )
    """)

    # Create likes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE,
            open_heavens_id INTEGER REFERENCES open_heavens(id)
        )
    """)

    # Create pray table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pray (
            id BIGINT PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            prayer_content TEXT,
            prayer_request_id BIGINT,
            name TEXT
        )
    """)

# Field mappings between Supabase and PostgreSQL
FIELD_MAPPINGS = {
    'open_heavens': {
        'bibleReadingText': 'bible_reading_text',
        'bible1YearText': 'bible1_year_text',
        'actionType': 'action_type'
    },
    'open_heavens_teenagers': {
        'Bible in One Year Verse': 'bible_in_one_year_verse',
        'Bible in One Year': 'bible_in_one_year',
        'Action Types': 'action_types',
        'Memories': 'memories',
        'Read': 'read',
        'HymnTitle': 'hymn_title',
        'Hymn': 'hymn'
    }
}

def insert_data(cursor, supabase_table_name, data):
    """Insert data into specified table"""
    successful = 0
    pg_table_name = TABLE_MAPPINGS[supabase_table_name]
    
    # Get field mappings for this table
    field_mappings = FIELD_MAPPINGS.get(pg_table_name, {})
    
    for item in data:
        try:
            # Transform field names based on mappings
            transformed_item = {}
            for key, value in item.items():
                # Check if this field needs to be mapped
                if key in field_mappings:
                    transformed_item[field_mappings[key]] = value
                else:
                    transformed_item[key] = value
            
            item = transformed_item
            
            if pg_table_name == "hymns":
                cursor.execute(
                    """
                    INSERT INTO hymns (id, hymn_title, hymn_verse, created_at)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE 
                    SET hymn_title = EXCLUDED.hymn_title,
                        hymn_verse = EXCLUDED.hymn_verse,
                        created_at = EXCLUDED.created_at
                    """,
                    (
                        item["id"],
                        item.get("hymnTitle", item.get("hymn_title", "")),
                        item.get("hymnVerse", item.get("hymn_verse", "")),
                        item["created_at"]
                    )
                )
            elif pg_table_name == "open_heavens":
                cursor.execute(
                    """
                    INSERT INTO open_heavens (id, topic, memory_verse, bible_reading, 
                                           message, action_point, created_at, hymn_id,
                                           date, bible_reading_text, action_type,
                                           bible1_year, bible1_year_text)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE 
                    SET topic = EXCLUDED.topic,
                        memory_verse = EXCLUDED.memory_verse,
                        bible_reading = EXCLUDED.bible_reading,
                        message = EXCLUDED.message,
                        action_point = EXCLUDED.action_point,
                        created_at = EXCLUDED.created_at,
                        hymn_id = EXCLUDED.hymn_id,
                        date = EXCLUDED.date,
                        bible_reading_text = EXCLUDED.bible_reading_text,
                        action_type = EXCLUDED.action_type,
                        bible1_year = EXCLUDED.bible1_year,
                        bible1_year_text = EXCLUDED.bible1_year_text
                    """,
                    (
                        item["id"],
                        item.get("topic", ""),
                        item.get("memoryVerse", item.get("memory_verse", "")),
                        item.get("bibleReading", item.get("bible_reading", "")),
                        item.get("message", ""),
                        item.get("actionPoint", item.get("action_point", "")),
                        item["created_at"],
                        item.get("hymn", item.get("hymn_id")),
                        item.get("date"),
                        item.get("bible_reading_text", ""),
                        item.get("action_type", ""),
                        item.get("bible1Year", item.get("bible1_year", "")),
                        item.get("bible1YearText", item.get("bible1_year_text", ""))
                    )
                )
            elif pg_table_name == "pray":
                cursor.execute(
                    """
                    INSERT INTO pray (id, created_at, prayer_content, prayer_request_id, name)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE 
                    SET created_at = EXCLUDED.created_at,
                        prayer_content = EXCLUDED.prayer_content,
                        prayer_request_id = EXCLUDED.prayer_request_id,
                        name = EXCLUDED.name
                    """,
                    (
                        item["id"],
                        item["created_at"],
                        item.get("prayer_content", ""),
                        item.get("prayer_request_id"),
                        item.get("name", "")
                    )
                )
            elif pg_table_name == "open_heavens_teenagers":
                cursor.execute(
                    """
                    INSERT INTO open_heavens_teenagers (id, topic, memory_verse, bible_reading, 
                                                     message, action_text, created_at, hymnal_id,
                                                     title, date, memories, read, hymn_title,
                                                     hymn, bible_in_one_year_verse,
                                                     bible_in_one_year, action_types)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE 
                    SET topic = EXCLUDED.topic,
                        memory_verse = EXCLUDED.memory_verse,
                        bible_reading = EXCLUDED.bible_reading,
                        message = EXCLUDED.message,
                        action_text = EXCLUDED.action_text,
                        created_at = EXCLUDED.created_at,
                        hymnal_id = EXCLUDED.hymnal_id,
                        title = EXCLUDED.title,
                        date = EXCLUDED.date,
                        memories = EXCLUDED.memories,
                        read = EXCLUDED.read,
                        hymn_title = EXCLUDED.hymn_title,
                        hymn = EXCLUDED.hymn,
                        bible_in_one_year_verse = EXCLUDED.bible_in_one_year_verse,
                        bible_in_one_year = EXCLUDED.bible_in_one_year,
                        action_types = EXCLUDED.action_types
                    """,
                    (
                        item["id"],
                        item.get("Title", item.get("topic", "")),
                        item.get("Memories", "").strip(),
                        item.get("BibleReading", item.get("bible_reading", "")),
                        item.get("Message", "").strip(),
                        item.get("Action Text", item.get("action_text", "")),
                        item["created_at"],
                        item.get("Hymnal", item.get("hymnal_id")),
                        item.get("title", ""),
                        item.get("date"),
                        item.get("memories", ""),
                        item.get("read", ""),
                        item.get("hymn_title", ""),
                        item.get("hymn", ""),
                        item.get("bible_in_one_year_verse", ""),
                        item.get("bible_in_one_year", ""),
                        item.get("action_types", "")
                    )
                )
            elif pg_table_name == "prayer_requests":
                cursor.execute(
                    """
                    INSERT INTO prayer_requests (id, request_content, created_at, disabled, name, user_ref)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE 
                    SET request_content = EXCLUDED.request_content,
                        created_at = EXCLUDED.created_at,
                        disabled = EXCLUDED.disabled,
                        name = EXCLUDED.name,
                        user_ref = EXCLUDED.user_ref
                    """,
                    (
                        item["id"], 
                        item.get("request_content", ""),
                        item["created_at"],
                        item.get("disabled", False),
                        item.get("name", ""),
                        item.get("user_ref", "")
                    )
                )
            elif pg_table_name == "comments":
                cursor.execute(
                    """
                    INSERT INTO comments (id, comment, created_at, open_heavens_id)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE 
                    SET comment = EXCLUDED.comment,
                        created_at = EXCLUDED.created_at,
                        open_heavens_id = EXCLUDED.open_heavens_id
                    """,
                    (
                        item["id"],
                        item.get("comment", ""),
                        item["created_at"],
                        item.get("open_heavens_id", item.get("openHeavensId"))
                    )
                )
            elif pg_table_name == "likes":
                cursor.execute(
                    """
                    INSERT INTO likes (id, created_at, open_heavens_id)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (id) DO UPDATE 
                    SET created_at = EXCLUDED.created_at,
                        open_heavens_id = EXCLUDED.open_heavens_id
                    """,
                    (
                        item["id"],
                        item["created_at"],
                        item.get("open_heavens_id", item.get("openHeavensId"))
                    )
                )
                
            successful += 1
            print(f"Inserted {supabase_table_name} record {item['id']}")
            
        except Exception as e:
            print(f"Error inserting {supabase_table_name} record {item['id']}: {str(e)}")
            continue
            
    return successful

# Define mappings between Supabase and PostgreSQL
TABLE_MAPPINGS = {
    "Hymns": "hymns",
    "OPEN HEAVENS": "open_heavens",
    "Open Heavens Teenagers": "open_heavens_teenagers",
    "prayer_requests": "prayer_requests",
    "comments": "comments",
    "likes": "likes",
    "pray": "pray"
}

FIELD_MAPPINGS = {
    "hymns": {
        "hymnTitle": "hymn_title",
        "hymnVerse": "hymn_verse"
    },
    "open_heavens": {
        "memoryVerse": "memory_verse",
        "bibleReading": "bible_reading",
        "actionPoint": "action_point",
        "hymn": "hymn_id",
        "bible1Year": "bible1_year",
        "bible1YearText": "bible1_year_text",
        "bibleReadingText": "bible_reading_text",
        "actionType": "action_type"
    },
    "open_heavens_teenagers": {
        "Title": "topic",
        "Memories": "memories",
        "BibleReading": "bible_reading",
        "Message": "message",
        "Action Text": "action_text",
        "Hymnal": "hymnal_id",
        "Read": "read",
        "HymnTitle": "hymn_title",
        "Hymn": "hymn",
        "Bible in One Year Verse": "bible_in_one_year_verse",
        "Bible in One Year": "bible_in_one_year",
        "Action Types": "action_types"
    }
}

def map_field_value(table_name, field_name, value):
    """Map field values between Supabase and PostgreSQL"""
    if table_name in FIELD_MAPPINGS and field_name in FIELD_MAPPINGS[table_name]:
        return value
    return value

def main():
    conn = None
    try:
        # Connect to PostgreSQL
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()
        
        # Drop all tables in correct order
        print("Dropping existing tables...")
        cursor.execute("""
            DROP TABLE IF EXISTS likes CASCADE;
            DROP TABLE IF EXISTS comments CASCADE;
            DROP TABLE IF EXISTS pray CASCADE;
            DROP TABLE IF EXISTS prayer_requests CASCADE;
            DROP TABLE IF EXISTS open_heavens_teenagers CASCADE;
            DROP TABLE IF EXISTS open_heavens CASCADE;
            DROP TABLE IF EXISTS hymns CASCADE;
        """)
        conn.commit()
        
        # Create tables
        print("Creating tables...")
        create_tables(cursor)
        conn.commit()
        
        # List of tables to migrate in order
        tables = list(TABLE_MAPPINGS.keys())
        
        # Migrate each table
        for supabase_table in tables:
            try:
                print(f"\nMigrating {supabase_table}...")
                data = fetch_data(supabase_table)
                if data:
                    successful = insert_data(cursor, supabase_table, data)
                    print(f"Successfully migrated {successful} out of {len(data)} records for {supabase_table}")
                else:
                    print(f"No data received for {supabase_table}")
                conn.commit()
            except Exception as table_error:
                print(f"Error migrating {supabase_table}: {str(table_error)}")
                continue

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()