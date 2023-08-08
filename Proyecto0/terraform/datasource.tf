#Data for AMI Ubuntu
#data "aws_ami" "main_ami" {
#  most_recent = true
#  owners      = ["099720109477"]

#  filter {
#    name   = "name"
#    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
#  }

#  filter {
#    name   = "virtualization-type"
#    values = ["hvm"]
#  }
#}

# ALTERNATIVO PARA ORACLE
provider "oci" {
  tenancy_ocid         = "YOUR_TENANCY_OCID"
  user_ocid            = "YOUR_USER_OCID"
  fingerprint         = "YOUR_FINGERPRINT"
  private_key_path    = "YOUR_PRIVATE_KEY_PATH"
  region              = "YOUR_REGION"
}

data "oci_core_images" "ubuntu_images" {
  compartment_id = "YOUR_COMPARTMENT_OCID"

  # Filter for Oracle Linux images
  filter {
    name   = "display_name"
    values = ["Oracle Linux 7.x"]
  }
}

resource "oci_core_instance" "example_instance" {
  availability_domain = "YOUR_AVAILABILITY_DOMAIN"
  compartment_id     = "YOUR_COMPARTMENT_OCID"
  shape              = "YOUR_INSTANCE_SHAPE"
  subnet_id          = "YOUR_SUBNET_OCID"
  display_name       = "MyInstance"

  source_details {
    source_type = "image"
    source_id   = data.oci_core_images.ubuntu_images.images[0].id
  }

  # Add other instance configuration here
}


