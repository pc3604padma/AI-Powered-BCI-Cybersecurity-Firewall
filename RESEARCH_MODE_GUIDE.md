# 🔬 Research Mode Testing Guide

## Overview
The enhanced dashboard now supports **two testing modes** for your BCI firewall research:

### 1. **Research Mode** (NEW!)
Perfect for controlled scientific testing where you need exact control over test parameters.

**Features:**
- Specify exact number of packets (e.g., 10)
- Specify exact number of malicious packets (e.g., 3-4)
- Remaining packets are randomly normal
- Malicious packets are randomly distributed throughout the test set

**Example:** 
- Total packets: 10
- Malicious packets: 4
- Result: 6 normal + 4 malicious, randomly mixed

---

### 2. **Realistic Mode** (Original)
For simulating real-world attack scenarios with percentage-based injection.

**Features:**
- Specify injection rate as percentage (e.g., 30%)
- Specify total packets
- System calculates estimated normal/malicious counts

**Example:**
- Total packets: 10
- Injection rate: 40%
- Result: ~6 normal + ~4 malicious

---

## How to Use Research Mode

### Step 1: Access the Dashboard
```bash
streamlit run app.py
```

### Step 2: Login
- Create an account or login with existing credentials

### Step 3: Select Research Mode
- In the **Control Panel** (left sidebar), select **"📊 Research Mode"**

### Step 4: Configure Test Parameters
- **Total packets to test**: Slide to desired count (e.g., 10)
- **Malicious packets to inject**: Slide to desired count (e.g., 3-4)
- Dashboard shows summary of test configuration

### Step 5: Run Test
- Click **"🚀 Start Research Test"** button
- Dashboard generates exactly configured packets
- Firewall scans all packets
- Results displayed in detail

---

## Understanding the Results

### 📊 Top Metrics Row
```
Packets Scanned: 10  |  Threats Detected: 4  |  Detection Accuracy: 100%
```
- **Packets Scanned**: Total packets used
- **Threats Detected**: How many detected as malicious
- **Detection Accuracy**: % of correct decisions

### ✅ ALLOWED vs 🚫 BLOCKED
```
Packets ALLOWED: 6  |  Packets BLOCKED: 4  |  Total Sequences: 0
```
- **ALLOWED**: Packets passed as normal
- **BLOCKED**: Packets detected as threats
- **Total Sequences**: LSTM window count (packet_count - 10)

---

## 📋 Detailed Results Table

Each row shows **one packet** with:

| Column | Meaning |
|--------|---------|
| **Packet #** | Sequential packet ID (1-10) |
| **Actual Label** | What it really is (🟢 NORMAL or 🔴 MALICIOUS) |
| **Firewall Decision** | What firewall decided (✅ ALLOWED or 🚫 BLOCKED) |
| **In Sequences** | Which LSTM windows contain this packet |
| **Correct** | ✅ if decision matches actual, ❌ if wrong |

---

## 📊 Research Summary Statistics

```
Total Correct: 10/10 (100%)  |  Malicious Detected: 4/4  |  Normal Passed: 6/6  |  Test Mode: Research
```

- **Total Correct**: Overall accuracy
- **Malicious Detected**: How many actual malicious packets were caught
- **Normal Passed**: How many normal packets passed safely
- **Test Mode**: Shows which mode was used

---

## Example Test Scenario

### Configuration:
- Total packets: 12
- Malicious packets: 4
- Normal packets: 8

### Expected Results:
- System generates 12 packets (4 malicious, 8 normal, randomly mixed)
- Creates 2 LSTM sequences (12 - 10 = 2)
- Analyzes each sequence
- Shows which packets passed vs blocked
- Displays accuracy metrics

### Output Display:
```
Packets Scanned: 12
Threats Detected: 4
Detection Accuracy: 100%

✅ Packets ALLOWED: 8
🚫 Packets BLOCKED: 4
📊 Total Sequences: 2

[Detailed packet-by-packet table]
[Research summary with exact counts]
```

---

## Why Two Modes?

| Aspect | Research Mode | Realistic Mode |
|--------|---------------|----------------|
| **Use Case** | Controlled experiments | Real-world simulation |
| **Control** | Exact packet counts | Percentage-based |
| **Variability** | Precise, reproducible | Probabilistic |
| **Research Needs** | ✅ Perfect | ⚠️ Approximate |
| **Demo Purposes** | ✅ Perfect | ✅ Good |

---

## Tips for Research

1. **Start Small**: Begin with 10 packets, 3-4 malicious
2. **Incremental Testing**: Gradually increase packet count
3. **Multiple Runs**: Run same configuration multiple times to check consistency
4. **Vary Malicious Count**: Test different injection rates (1, 2, 3, 4, 5 malicious out of 10)
5. **Document Results**: Take screenshots for your research paper

---

## Common Test Scenarios

### Scenario 1: Baseline Normal
- Total: 10, Malicious: 0
- Expected: All packets ALLOWED
- Use: Verify no false positives

### Scenario 2: All Malicious
- Total: 10, Malicious: 10
- Expected: All packets BLOCKED
- Use: Verify detection capability

### Scenario 3: Mixed (30% Attack)
- Total: 10, Malicious: 3
- Expected: 3 BLOCKED, 7 ALLOWED
- Use: Realistic attack scenario

### Scenario 4: Sparse Attack (10%)
- Total: 10, Malicious: 1
- Expected: 1 BLOCKED, 9 ALLOWED
- Use: Detect needle-in-haystack attacks

---

## Troubleshooting

### Issue: Dashboard shows random results each time
**Solution**: Results vary because malicious packets are randomly distributed. Run same test again to see different distribution.

### Issue: Not all malicious packets detected
**Solution**: Check if detection accuracy < 100%. Some malicious packets might be in non-overlapping LSTM windows.

### Issue: Some normal packets blocked
**Solution**: False positive - check the "Correct" column. Firewall threshold might be too sensitive.

---

## Next Steps

1. Run your first Research Mode test with 10 packets, 3 malicious
2. Verify 100% accuracy
3. Increase packet count gradually
4. Document results for your research

Good luck with your BCI cybersecurity research! 🧠🔒
