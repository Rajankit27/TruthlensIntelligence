import sys
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app import app

def run_test():
    app.config['TESTING'] = True
    client = app.test_client()
    
    import uuid
    username = f"testhistory_{uuid.uuid4().hex[:6]}"
    password = "password123"
    
    print(f"1. Registering new user: {username}")
    reg_resp = client.post("/auth/register", json={"username": username, "password": password})
    print("   Response:", reg_resp.status_code, reg_resp.get_json())
    
    print("\n2. Logging in to get JWT token")
    login_resp = client.post("/auth/login", json={"username": username, "password": password})
    token = login_resp.get_json().get("token")
    print("   Token received:", bool(token))
    
    if not token:
        print("   Exiting early due to missing token.")
        return
        
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n3. Making /predict request")
    fake_news_text = "Breaking News: Scientists discover a new planet made entirely of diamonds in our solar system!"
    predict_resp = client.post("/predict", json={"text": fake_news_text}, headers=headers)
    print("   Response:", predict_resp.status_code, predict_resp.get_json())
    
    import time
    time.sleep(1.0) # Wait for daemon thread to insert BSON
    
    print("\n4. Checking /history")
    history_resp = client.get("/history", headers=headers)
    print("   Response Code:", history_resp.status_code)
    history_data = history_resp.get_json()
    
    if isinstance(history_data, list):
        print(f"   Found {len(history_data)} history records.")
        for i, record in enumerate(history_data, 1):
            print(f"   Record {i}:", record)
    else:
        print("   Unexpected history format:", history_data)

if __name__ == "__main__":
    run_test()
