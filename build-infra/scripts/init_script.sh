#!/bin/bash

sudo apt update -y
sudo apt upgrade -y
# VM setup steps
# Installs aws cli for app resource download from S3
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
unzip /tmp/awscliv2.zip
./aws/install
echo aws --version

# Pip and python version
sudo apt install python3-pip -y
sudo apt install pip -y
sudo apt-get install python3.7 -y
   
curl "https://bootstrap.pypa.io/get-pip.py" -o "/tmp/get-pip.py"
python3 /tmp/get-pip.py --user
echo "export PATH=/home/ubuntu/.local/bin:$PATH" | cat >> ~/.bash_profile
source ~/.bash_profile

# Cleanup
rm -rf /tmp/get-pip.py
rm -rf /tmp/awscliv2.zip

