from pymongo import MongoClient
from datetime import datetime
import json

client = MongoClient("mongodb://localhost:27017/")

db = client["synora"]

users_collection = db["users"]
firewall_logs_collection = db["firewall_logs"]


def log_firewall_scan(email, num_packets, num_sequences, decisions, is_malicious, 
                      accuracy, malicious_count, normal_count, decision_breakdown=None):
    """
    Log firewall scan results to database
    
    Args:
        email: User email
        num_packets: Number of packets scanned
        num_sequences: Number of LSTM sequences
        decisions: List of decisions per sequence
        is_malicious: Boolean array indicating which packets are malicious
        accuracy: Overall accuracy percentage
        malicious_count: Total malicious packets detected
        normal_count: Total normal packets
        decision_breakdown: Dict with ALLOW/BLOCK/QUARANTINE counts
    """
    log_entry = {
        "email": email,
        "timestamp": datetime.now(),
        "scan_config": {
            "total_packets": num_packets,
            "total_sequences": num_sequences,
            "injection_rate": f"{(malicious_count/num_packets)*100:.1f}%"
        },
        "results": {
            "accuracy": accuracy,
            "malicious_detected": malicious_count,
            "normal_passed": normal_count,
            "decision_breakdown": decision_breakdown or {}
        },
        "statistics": {
            "total_decisions": len(decisions),
            "decisions_list": decisions[:50],  # Store first 50 for reference
            "malicious_distribution": sum(is_malicious)
        },
        "session_id": f"{email}_{datetime.now().timestamp()}"
    }
    
    result = firewall_logs_collection.insert_one(log_entry)
    return result.inserted_id


def get_firewall_history(email, limit=20):
    """Get firewall scan history for a user"""
    try:
        logs = list(firewall_logs_collection.find(
            {"email": email}
        ).sort("timestamp", -1).limit(limit))
        
        # Convert ObjectId to string for JSON serialization
        for log in logs:
            log["_id"] = str(log.get("_id", ""))
            if "timestamp" in log and log["timestamp"]:
                log["timestamp"] = log["timestamp"].isoformat()
            else:
                log["timestamp"] = "N/A"
        
        return logs
    except Exception as e:
        return []


def get_firewall_stats(email):
    """Get aggregate firewall statistics for a user"""
    pipeline = [
        {"$match": {"email": email}},
        {"$group": {
            "_id": None,
            "total_scans": {"$sum": 1},
            "avg_accuracy": {"$avg": "$results.accuracy"},
            "total_threats": {"$sum": "$results.malicious_detected"},
            "total_packets_scanned": {"$sum": "$scan_config.total_packets"}
        }}
    ]
    
    try:
        result = list(firewall_logs_collection.aggregate(pipeline))
        if result:
            stats = result[0]
            # Remove MongoDB's _id field
            stats.pop('_id', None)
            return stats
        else:
            return None
    except:
        return None


def clear_user_logs(email):
    """Delete all logs for a user"""
    result = firewall_logs_collection.delete_many({"email": email})
    return result.deleted_count