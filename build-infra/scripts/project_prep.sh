#!/bin/bash

# Adding executable rights
chmod +x /tmp/init_script.sh

# Running basic machine dependency and project setup
sh /tmp/init_script.sh

# Copying project repo locally
git clone https://github.com/KishanMistri/Walmart_Sales_Deployment.git

# Project package requirement installation
pip install -r Walmart_Sales_Deployment/requirements.txt

# crontab set
(crontab -l 2>/dev/null || echo "# run the model notebook with the papermill process at 1 AM every day"; echo "0 1 * * * papermill ~/.Walmart_Sales_Deployment/selected_model.ipynb ~/.Walmart_Sales_Deployment/results.ipynb") | crontab -

# Starting web service
nohup streamlit run Walmart_Sales_Deployment/Home.py --server.port 443  </dev/null &>/dev/null &