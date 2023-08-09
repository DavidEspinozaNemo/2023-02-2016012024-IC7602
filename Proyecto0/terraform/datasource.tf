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
  tenancy_ocid         = "${var.tenancy_ocid}"
  user_ocid            = "${var.user_ocid}"
  fingerprint          = "${var.fingerprint}"
  private_key_path     = "${var.private_key_path}"
  private_key_password = "${var.private_key_password}
  region               = "${var.region}"
}

data "oci_core_images" "ubuntu_images" {
  compartment_id = "${var.compartment_ocid}"

  # Filter for Oracle Linux images
  filter {
    name   = "display_name"
    values = ["Oracle Linux 7.x"]
  }
}

resource "oci_core_instance" "example_instance" {
  availability_domain = "${var.availability_domain}"
  compartment_id      = "${var.compartment_ocid}"
  shape               = "${var.shape}"
  subnet_id           = oci_core_subnet.public_subnet.id
  subnet_id           = oci_core_subnet.private_subnet.id
  display_name        = "MainOCI"

  source_details {
    source_type = "image"
    #"${image_ocid}"
    source_id   = data.oci_core_images.ubuntu_images.images[0].id
  }

  # Add other instance configuration here
}


