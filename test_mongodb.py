#!/usr/bin/env python
"""
MongoDB Connection & Firewall Logs Diagnostic Script
Run this to verify MongoDB is working and logs are being saved
"""

import sys
from datetime import datetime
from pymongo import MongoClient

print("=" * 60)
print("🔍 BCI Cybersecurity - MongoDB Diagnostic Tool")
print("=" * 60)

# 1. Test Connection
print("\n📌 Step 1: Testing MongoDB Connection...")
try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    # Force connection test
    client.server_info()
    print("✅ MongoDB Connection: SUCCESS")
except Exception as conn_error:
    print(f"❌ MongoDB Connection FAILED: {str(conn_error)}")
    print("   ❗ Make sure MongoDB is running: mongod.exe")
    sys.exit(1)

# 2. Check Database
print("\n📌 Step 2: Checking Database 'synora'...")
try:
    db = client["synora"]
    firewall_logs_collection = db["firewall_logs"]
    print("✅ Database 'synora' OK")
except Exception as db_error:
    print(f"❌ Database Error: {str(db_error)}")
    sys.exit(1)

# 3. Check Collection
print("\n📌 Step 3: Checking Collection 'firewall_logs'...")
try:
    collection_list = db.list_collection_names()
    if "firewall_logs" in collection_list:
        print("✅ Collection 'firewall_logs' exists")
    else:
        print("⚠️  Collection 'firewall_logs' not created yet (will be created on first scan)")
except Exception as coll_error:
    print(f"❌ Collection Error: {str(coll_error)}")
    sys.exit(1)

# 4. Count Documents
print("\n📌 Step 4: Counting Firewall Logs...")
try:
    total_docs = firewall_logs_collection.count_documents({})
    if total_docs > 0:
        print(f"✅ Found {total_docs} firewall log entries!")
        
        # Show recent logs
        print("\n📋 Recent Log Entries:")
        recent = list(firewall_logs_collection.find({}).sort("timestamp", -1).limit(3))
        for i, log in enumerate(recent, 1):
            email = log.get("email", "N/A")
            timestamp = log.get("timestamp", "N/A")
            accuracy = log.get("results", {}).get("accuracy", "N/A")
            print(f"   {i}. Email: {email} | Time: {timestamp} | Accuracy: {accuracy:.1f}%")
    else:
        print("⚠️  No logs found in database")
        print("   This is normal if you haven't run any scans yet")
except Exception as count_error:
    print(f"❌ Count Error: {str(count_error)}")

# 5. Test Insert
print("\n📌 Step 5: Testing Data Insert (Test Log)...")
try:
    test_log = {
        "email": "test@example.com",
        "timestamp": datetime.now(),
        "scan_config": {
            "total_packets": 20,
            "total_sequences": 11,
            "injection_rate": "30.0%"
        },
        "results": {
            "accuracy": 85.5,
            "malicious_detected": 6,
            "normal_passed": 14,
            "decision_breakdown": {"ALLOW": 5, "BLOCK": 4, "QUARANTINE": 2}
        },
        "statistics": {
            "total_decisions": 11,
            "decisions_list": ["ALLOW", "BLOCK", "ALLOW", "QUARANTINE"],
            "malicious_distribution": 6
        },
        "session_id": f"test_{datetime.now().timestamp()}"
    }
    
    result = firewall_logs_collection.insert_one(test_log)
    print(f"✅ Test Log Inserted Successfully (ID: {result.inserted_id})")
    
    # Verify inserted
    found = firewall_logs_collection.find_one({"_id": result.inserted_id})
    if found:
        print("✅ Test Log Verified in Database")
    else:
        print("❌ Test Log Not Found After Insert")
        
except Exception as insert_error:
    print(f"❌ Insert Error: {str(insert_error)}")

# 6. Check User Logs
print("\n📌 Step 6: Checking Logs for Your User...")
try:
    # Note: Replace with actual email if needed
    sample_email = "test@example.com"
    user_logs = firewall_logs_collection.find({"email": sample_email})
    user_count = firewall_logs_collection.count_documents({"email": sample_email})
    
    if user_count > 0:
        print(f"✅ Found {user_count} log(s) for {sample_email}")
    else:
        print(f"⚠️  No logs for {sample_email}")
        # Get any email
        any_log = firewall_logs_collection.find_one()
        if any_log:
            print(f"   Sample user in logs: {any_log.get('email')}")
except Exception as user_error:
    print(f"❌ User Logs Error: {str(user_error)}")

# Summary
print("\n" + "=" * 60)
print("✅ MongoDB Status: OK")
print("=" * 60)

print("""
📝 Troubleshooting Tips:
1. If "MongoDB Connection FAILED":
   - Run: mongod.exe (start MongoDB server)
   - Check if MongoDB is installed and running

2. If collection is empty (no logs):
   - Run a scan in the app
   - Check the console output (print statements show errors)
   
3. If you see errors during insert:
   - Data type issue likely (numpy array, etc.)
   - Check console for the exact error message

📊 Next Steps:
- Run the Streamlit app: streamlit run app.py
- Perform a scan with 20+ packets
- Return here to check if logs appear
- Logs should show in MongoDB Compass under:
  synora > firewall_logs
""")

print("\n✨ Close MongoDB Compass and reopen it to see new logs!")
