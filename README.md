# Walmart Unit Sales Forecasting for next 28 days
Streamlit deployment of model result dashboarding.

Pre-requisites:

1: You must have AWS account and its secret configured locally. 

2: AWS key-pair should be generate before-hand as it will be used to connect to VM provisioned.

3: Terraform should be installed and setup on your system.


Steps:

1: Download/clone this [project repo](https://github.com/KishanMistri/Walmart_Sales_Deployment).

2: Move to "build-infra" and move paste private key in keys folder.

3: From build-infra folder. 
 
> terraform init

> terraform validate

> terraform plan

> if no errors then proceed

> terraform apply --auto-approve

4: login on your server and validate if service is running or not by 

> ssh -i <key-name>.pem  ubuntu@<private-ip>

> ps -Al | grep streamlit

if not running: 

> streamlit run Walmart_Sales_Deployment/Home.py --server.port <port-number>

5: Go to [https://private-ip:port-number]() in browser. Your app should be running now.

For other common issues visit [forum](https://discuss.streamlit.io/).
