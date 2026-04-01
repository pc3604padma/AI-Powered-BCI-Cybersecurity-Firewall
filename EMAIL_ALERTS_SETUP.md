# 📧 Email Alerts Setup Guide

## Quick Start (2 minutes)

### Step 1: Get Gmail App Password
1. Go to: **myaccount.google.com**
2. Click **Security** (left sidebar)
3. Look for **App passwords** (need 2FA enabled)
4. Select: Mail → Windows Computer
5. Copy the **16-character password**

### Step 2: Configure email_alerts.py
Edit `email_alerts.py` (in root directory):

```python
SENDER = "your_gmail@gmail.com"          # Your Gmail address
PASSWORD = "xxxx xxxx xxxx xxxx"          # 16-char app password from Step 1
```

### Step 3: Restart Streamlit
```bash
streamlit run app.py
```

---

## How Email Alerts Work

### Trigger
When malicious packets detected during scan:
- Email sent automatically to your email
- Alert includes threat count and timestamp
- One alert per scan session

### Alert Content
```
Subject: 🚨 BCI Firewall Alert - X Threats Detected!

Body includes:
- Number of threats detected
- Total packets scanned
- Logged-in user
- Timestamp
- Link to review in dashboard
```

### Detection Flow
```
Scan packets → Firewall analysis → Threats found?
                                    ↓ YES
                              Send email alert
                              ↓
                         User receives alert
                              ↓
                         Review in dashboard
```

---

## Troubleshooting

### Issue: "Email failed: [SSL: CERTIFICATE_VERIFY_FAILED]"
**Solution:** You're using regular Gmail password instead of App Password
- Use App Password (16 characters with spaces)
- Don't use your regular Gmail password

### Issue: "Connection refused"
**Solution:** Gmail SMTP port issue
- Ensure 2FA is enabled on Gmail
- App passwords only work with 2FA

### Issue: "Email not received"
**Solution:** Check spam folder or check if configured correctly
```python
# Test manually in Python:
import email_alerts
email_alerts.send_email("your_email@gmail.com", "Test Subject", "This is a test email")
```

### Issue: "Authentication failed"
**Solution:** Wrong credentials
- Double-check SENDER email matches app password Gmail account
- Copy app password exactly (including spaces)

---

## Security Notes

⚠️ **IMPORTANT:**
- Never commit `email_alerts.py` with real passwords to GitHub
- Use environment variables in production
- Gmail App Passwords are specific to your Gmail account only

---

## Optional: Environment Variables (Production)

For production deployment, use environment variables:

```python
# email_alerts.py (root)
import os

SENDER = os.getenv("BCI_EMAIL_SENDER")
PASSWORD = os.getenv("BCI_EMAIL_PASSWORD")
```

Then set in your environment:
```bash
export BCI_EMAIL_SENDER="your_email@gmail.com"
export BCI_EMAIL_PASSWORD="xxxx xxxx xxxx xxxx"
```

Note: Receiver email is passed dynamically from the logged-in user's email.

---

## Features Included

✅ Email alerts on threat detection  
✅ User identification (logged-in email shown)  
✅ Timestamp logging  
✅ Threat count reporting  
✅ Error handling  
✅ Dashboard integration  

---

## Next Steps

1. ✅ Set up Gmail App Password
2. ✅ Configure email_alerts.py
3. ✅ Restart app
4. ✅ Run a scan with malicious packets
5. ✅ Check email for alert!

Happy monitoring! 🛡️
