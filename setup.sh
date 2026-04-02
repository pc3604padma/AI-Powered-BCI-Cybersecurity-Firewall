#!/bin/bash

# Create .streamlit directory if it doesn't exist
mkdir -p ~/.streamlit/

# Create Streamlit config for Heroku
echo "[server]
headless = true
port = \$PORT
enableCORS = false
enableXsrfProtection = true

[theme]
base = \"dark\"
primaryColor = \"#e94540\"
backgroundColor = \"#0f0f1e\"
secondaryBackgroundColor = \"#1a1a2e\"
textColor = \"#ffffff\"
font = \"sans serif\"

[client]
showErrorDetails = true
" > ~/.streamlit/config.toml

echo "✅ Streamlit configured for Heroku deployment"
