import requests
import json

def check_teenagers_data():
    PROJECT_ID = "vhqbtwmvteemgfsebvff"
    SUPABASE_URL = "https://vhqbtwmvteemgfsebvff.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZocWJ0d212dGVlbWdmc2VidmZmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDUwNDgwODUsImV4cCI6MjAyMDYyNDA4NX0.xC_D4_2MXG5Cb97cG-wUwESz32MDDBbeZ-dJIEhq4w8"
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Prefer": "return=representation"
    }
    
    url = f"{SUPABASE_URL}/rest/v1/Open Heavens Teenagers?select=*"
    response = requests.get(url, headers=headers)
    
    if response.ok:
        data = response.json()
        if data:
            print("\nSample row from Supabase:")
            print(json.dumps(data[0], indent=2))
            
            print("\nColumn names from first row:")
            for key in data[0].keys():
                print(f"- {key}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    check_teenagers_data()