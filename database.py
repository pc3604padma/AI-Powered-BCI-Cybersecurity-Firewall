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
    try:
        # Ensure all data types are JSON-serializable
        log_entry = {
            "email": str(email),
            "timestamp": datetime.now(),
            "scan_config": {
                "total_packets": int(num_packets),
                "total_sequences": int(num_sequences),
                "injection_rate": f"{(int(malicious_count)/int(num_packets))*100:.1f}%" if int(num_packets) > 0 else "0.0%"
            },
            "results": {
                "accuracy": float(accuracy),
                "malicious_detected": int(malicious_count),
                "normal_passed": int(normal_count),
                "decision_breakdown": {str(k): int(v) for k, v in (decision_breakdown or {}).items()}
            },
            "statistics": {
                "total_decisions": len(decisions),
                "decisions_list": [str(d) for d in decisions[:50]],  # Convert to string for safety
                "malicious_distribution": sum(1 for x in is_malicious if x)  # Count True values
            },
            "session_id": f"{email}_{datetime.now().timestamp()}"
        }
        
        result = firewall_logs_collection.insert_one(log_entry)
        return result.inserted_id
    except Exception as insert_error:
        print(f"❌ Database Insert Error: {str(insert_error)}")
        return None


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
    except Exception as history_error:
        print(f"❌ History Query Error: {str(history_error)}")
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
            "total_packets_scanned": {"$sum": "$scan_config.total_packets"},
            "decision_breakdown": {"$push": "$results.decision_breakdown"}
        }},
        {"$project": {
            "total_scans": 1,
            "avg_accuracy": 1,
            "total_threats": 1,
            "total_packets_scanned": 1,
            "decision_distribution": {
                "ALLOW": {
                    "$sum": [
                        {"$ifNull": [
                            {"$getField": {"field": "ALLOW", "input": {"$arrayElemAt": ["$decision_breakdown", 0]}}},
                            0
                        ]}
                    ]
                },
                "BLOCK": {
                    "$sum": [
                        {"$ifNull": [
                            {"$getField": {"field": "BLOCK", "input": {"$arrayElemAt": ["$decision_breakdown", 0]}}},
                            0
                        ]}
                    ]
                },
                "QUARANTINE": {
                    "$sum": [
                        {"$ifNull": [
                            {"$getField": {"field": "QUARANTINE", "input": {"$arrayElemAt": ["$decision_breakdown", 0]}}},
                            0
                        ]}
                    ]
                }
            }
        }}
    ]
    
    try:
        result = list(firewall_logs_collection.aggregate(pipeline))
        if result:
            stats = result[0]
            # Remove MongoDB's _id field if present
            stats.pop('_id', None)
            
            # Ensure decision_distribution is a dict with counts
            if 'decision_distribution' not in stats or not isinstance(stats['decision_distribution'], dict):
                # Simpler fallback: just use raw counts
                stats['decision_distribution'] = {
                    "ALLOW": 0,
                    "BLOCK": 0,
                    "QUARANTINE": 0
                }
            
            return stats
        else:
            return None
    except Exception as stats_error:
        print(f"❌ Stats Query Error: {str(stats_error)}")
        return None


def clear_user_logs(email):
    """Delete all logs for a user"""
    result = firewall_logs_collection.delete_many({"email": email})
    return result.deleted_count