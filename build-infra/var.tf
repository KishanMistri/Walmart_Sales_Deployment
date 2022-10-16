variable "region" {
  default = "us-west-2"
}
variable "env" {
  default = "dev"
}
variable "cidr_block" {
  default = "190.160.0.0/16"
}
variable "subnet1" {
  default = "190.160.1.0/24"
}
variable "keypair" {
  default = "walmart-project"
}
variable "instance_type" {
  default = "c4.4xlarge"
}
