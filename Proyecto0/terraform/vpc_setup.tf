##Main VPC
#resource "aws_vpc" "main_vpc" {
#  cidr_block           = "192.168.0.0/16"
#  enable_dns_hostnames = true
#  enable_dns_support   = true

#  tags = {
#    Name = "Main VPC"
#  }
#}

#Public subnet
#resource "aws_subnet" "public_subnet" {
#  vpc_id                  = aws_vpc.main_vpc.id
#  cidr_block              = "192.168.1.0/24"
#  map_public_ip_on_launch = true
#  availability_zone       = "us-east-1a"

#  tags = {
#    Name = "public-subnet"
#  }
#}

#Private subnet
#resource "aws_subnet" "private_subnet" {
#  vpc_id            = aws_vpc.main_vpc.id
#  cidr_block        = "192.168.0.0/24"
#  availability_zone = "us-east-1b"

#  tags = {
#    Name = "private-subnet"
#  }
#}

##Internet gateway for the public subnet
#resource "aws_internet_gateway" "main_internet_gw" {
#  vpc_id = aws_vpc.main_vpc.id
#}

#resource "aws_route_table" "public_route_table" {
#  vpc_id = aws_vpc.main_vpc.id
#}

#resource "aws_route" "default_route" {
#  route_table_id         = aws_route_table.public_route_table.id
#  destination_cidr_block = "0.0.0.0/0"
#  gateway_id             = aws_internet_gateway.main_internet_gw.id
#}

#resource "aws_route_table_association" "public_subnet_association" {
#  subnet_id      = aws_subnet.public_subnet.id
#  route_table_id = aws_route_table.public_route_table.id
#}

#NAT gateway to the private subnet
#resource "aws_eip" "nat_eip" {
#  domain   = "vpc"
#}
#resource "aws_nat_gateway" "nat" {
#  connectivity_type = "private"
#  subnet_id         = aws_subnet.private_subnet.id
#  allocation_id     = aws_eip.nat_eip.id
#}

##Security group
#resource "aws_security_group" "securty_group" {
#  name        = "main_security_group"
#  description = "main security group"
#  vpc_id      = aws_vpc.main_vpc.id

#  ingress {
#    from_port   = 22
#    to_port     = 22
#    protocol    = "tcp"
#    cidr_blocks = [aws_vpc.main_vpc.cidr_block]
#  }

#  ingress {
#    from_port   = 80
#    to_port     = 80
#    protocol    = "tcp"
#    cidr_blocks = [aws_vpc.main_vpc.cidr_block]
#  }

#  ingress {
#    from_port   = 443
#    to_port     = 443
#    protocol    = "tcp"
#    cidr_blocks = [aws_vpc.main_vpc.cidr_block]
#  }

#  ingress {
#    from_port   = 560
#    to_port     = 560
#    protocol    = "udp"
#    cidr_blocks = [aws_vpc.main_vpc.cidr_block]
#  }

#  ingress {
#    from_port   = 10000
#    to_port     = 20000
#    protocol    = "udp-tcp"
#    cidr_blocks = [aws_vpc.main_vpc.cidr_block]
#  }

#  ingress {
#    from_port   = 4569
#    to_port     = 4569
#    protocol    = "udp"
#    cidr_blocks = [aws_vpc.main_vpc.cidr_block]
#  }

#  egress {
#    from_port   = 0
#    to_port     = 0
#    protocol    = "-1"
#    cidr_blocks = ["0.0.0.0/0"]
#  }
#}

##Create key pair to access via ssh later
#resource "aws_key_pair" "main_auth" {
#  key_name   = "mainkey"
#  public_key = file("~/.ssh/mainkey.pub")
#}
##Create EC2 instances in public subnet
#resource "aws_instance" "public_instance" {
#  instance_type          = "t3.micro"
#  ami                    = data.aws_ami.main_ami.id
#  key_name               = aws_key_pair.main_auth.id
#  vpc_security_group_ids = [aws_security_group.securty_group.id]
#  subnet_id              = aws_subnet.public_subnet.id

#}

#Create EC2 instances in private subnet
#resource "aws_instance" "private_instance" {
#  instance_type          = "t3.micro"
#  ami                    = data.aws_ami.main_ami.id
#  key_name               = aws_key_pair.main_auth.id
#  vpc_security_group_ids = [aws_security_group.securty_group.id]
#  subnet_id              = aws_subnet.private_subnet.id

#}

terraform {
  required_providers {
    oci = {
      source  = "hashicorp/oci"
      version = "~> 4.0"
    }
  }
}

provider "oci" {
  tenancy_ocid         = "${var.tenancy_ocid}"
  user_ocid            = "${var.user_ocid}"
  fingerprint          = "${var.fingerprint}"
  private_key_path     = "${var.private_key_path}"
  region               = "${var.region}"
}

# Main VCN
resource "oci_core_virtual_network" "main_vcn" {
  
  compartment_id = "${var.compartment_ocid}"
  cidr_block     = "192.168.0.0/16"
  display_name   = "Main VCN"
}

# Public subnet
resource "oci_core_subnet" "public_subnet" {
  cidr_block      = "192.168.1.0/24"
  compartment_id  = "${var.compartment_ocid}"
  display_name    = "public-subnet"
  vcn_id          = oci_core_virtual_network.main_vcn.id
  availability_domain = "${var.availability_domain}"
}

# Private subnet
resource "oci_core_subnet" "private_subnet" {
  cidr_block     = "192.168.0.0/24"
  compartment_id = "${var.compartment_ocid}"
  display_name  = "private-subnet"
  vcn_id         = oci_core_virtual_network.main_vcn.id
  availability_domain = "${var.availability_domain}"
}

# Security List for Security Group (equivalent to Security Group in AWS)
resource "oci_core_security_list" "security_list" {
  compartment_id = ${image_ocid}
  display_name  = "main_security_group"

  egress_security_rules {
    destination = "0.0.0.0/0"
    protocol    = "-1"
  }

  ingress_security_rules {
    source      = oci_core_virtual_network.main_vcn.cidr_block
    protocol    = "6"
    tcp_options {
      destination_port_range {
        min = 22
        max = 22
      }
    }
  }

  # Add other ingress rules here
}

# Compute instance in Public Subnet
resource "oci_core_instance" "public_instance" {
  availability_domain = "${var.availability_domain}"
  compartment_id     = "${var.user_ocid}"
  shape              = "${var.shape}"
                        #   "VM.Standard.E2.1.Micro"  # Choose an appropriate shape
  display_name       = "PublicInstance"
  image_id           = "ocid1.image.oc1.region.${image_ocid}"
  subnet_id          = oci_core_subnet.public_subnet.id
  source_details {
    source_type = "image"
    source_id   = "ocid1.image.oc1.region.${image_ocid}"
  }
  create_vnic_details {
    subnet_id = oci_core_subnet.public_subnet.id
  }
}

# Compute instance in Private Subnet
resource "oci_core_instance" "private_instance" {
  availability_domain = "${var.availability_domain}"
  compartment_id      = "${var.user_ocid}"
  shape               = "${var.shape}"
                        # "VM.Standard.E2.1.Micro"  # Choose an appropriate shape
  display_name       = "PrivateInstance"
  image_id           = "ocid1.image.oc1.region.${image_ocid}"
  subnet_id          = oci_core_subnet.private_subnet.id
  source_details {
    source_type = "image"
    source_id   = "ocid1.image.oc1.region.${image_ocid}"
  }
  create_vnic_details {
    subnet_id = oci_core_subnet.private_subnet.id
  }
}

# SSH Key for Instances
resource "oci_identity_ssh_key" "main_auth" {
  compartment_id = "${var.user_ocid}"
  key           = file("~/.ssh/mainkey.pub")
  name          = "mainkey"
}


