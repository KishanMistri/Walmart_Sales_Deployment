# Resource bolcks
resource "aws_vpc" "assignment_vpc" {
  cidr_block = var.cidr_block
  tags = {
    Name = "${var.env}_vpc"
    Env  = var.env
  }
}


resource "aws_subnet" "subnet1" {
  vpc_id                  = aws_vpc.assignment_vpc.id
  cidr_block              = var.subnet1
  availability_zone       = "us-west-2a"
  map_public_ip_on_launch = "true"
  tags = {
    Name = "${var.env}_subnet1"
    Env  = var.env
  }
}

## Security Group##
resource "aws_security_group" "my_custom_sg" {
  description = "Allow limited inbound external traffic"
  vpc_id      = aws_vpc.assignment_vpc.id
  name        = "terraform_ec2_private_sg"
  ingress {
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 22
    to_port     = 22
  }
  ingress {
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 8080
    to_port     = 8080
  }
  ingress {
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 443
    to_port     = 443
  }
  ingress {
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 8501 # Streamlit
    to_port     = 8501
  }
  egress {
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    to_port     = 0
  }
  tags = {
    Name = "${var.env}_SG"
    Env  = var.env
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.assignment_vpc.id
  tags = {
    Name = "${var.env}_gw"
    Env  = var.env
  }
}

resource "aws_default_route_table" "route_table" {
  default_route_table_id = aws_vpc.assignment_vpc.default_route_table_id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
  tags = {
    Name = "default route table"
    env  = var.env
  }
}

# Attaching SG
resource "aws_network_interface_sg_attachment" "sg_attachment" {
  security_group_id    = aws_security_group.my_custom_sg.id
  network_interface_id = aws_instance.walmart_web_app.primary_network_interface_id
}

resource "aws_instance" "walmart_web_app" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  key_name      = var.keypair
  subnet_id     = aws_subnet.subnet1.id
  tags = {
    Name       = "Walmart Project Machine"
    Company    = "AAIC & UoH"
    Additional = "${var.env}_box"
  }
  user_data = "${file("./scripts/init_script.sh")}"
  
  provisioner "local-exec" {
    command = "chmod 600 ${file("./keys/walmart-project.pem")}"
  }
   
  connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = "${file("./keys/walmart-project.pem")}"
      host        = self.public_ip
      timeout     = "15m"
    }
    
  provisioner "remote-exec" {
    inline = [
        "git clone https://github.com/KishanMistri/Walmart_Sales_Deployment.git",
        "pip install -r Walmart_Sales_Deployment/requirements.txt",
        "(crontab -l 2>/dev/null || echo "# run the model notebook with the papermill process at 1 AM every day"; echo "0 1 * * * papermill ~/.Walmart_Sales_Deployment/selected_model.ipynb ~/.Walmart_Sales_Deployment/results.ipynb") | crontab -",
        "streamlit run Walmart_Sales_Deployment/Home.py"
    ]
  }
}
output "walmart_web_app_ip_addr" {
  value = aws_instance.walmart_web_app.public_ip
}

