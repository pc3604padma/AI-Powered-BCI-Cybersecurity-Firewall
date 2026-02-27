from blockchain_logger import Blockchain
from datetime import datetime

# -----------------------------
# Initialize blockchain
# -----------------------------
blockchain = Blockchain()

# -----------------------------
# Simulate adding blocks
# (Normally added by firewall)
# -----------------------------
blockchain.add_block({
    "timestamp": str(datetime.now()),
    "session_id": "EEG_STREAM_01",
    "packet_id": 2,
    "decision": "BLOCK",
    "reason": "Anomalous EEG pattern detected"
})

blockchain.add_block({
    "timestamp": str(datetime.now()),
    "session_id": "EEG_STREAM_01",
    "packet_id": 4,
    "decision": "QUARANTINE",
    "reason": "Repeated anomalies detected"
})

# -----------------------------
# Display blockchain
# -----------------------------
print("\n----- BLOCKCHAIN LEDGER -----\n")

for block in blockchain.chain:
    print(f"Block Index     : {block.index}")
    print(f"Timestamp       : {block.timestamp}")
    print(f"Data            : {block.data}")
    print(f"Previous Hash   : {block.previous_hash}")
    print(f"Current Hash    : {block.hash}")
    print("-" * 40)

# -----------------------------
# Validate blockchain
# -----------------------------
print("\nBlockchain valid:", blockchain.is_chain_valid())
