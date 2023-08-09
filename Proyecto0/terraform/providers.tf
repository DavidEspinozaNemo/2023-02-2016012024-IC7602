#terraform {
#  required_providers {
#    aws = {
#      source  = "hashicorp/aws"
#      version = "~> 5.0"
#    }
#  }
#}

## Configure the AWS Provider
#provider "aws" {
#  region = "us-east-1"

#}

terraform {
  required_providers {
    oci = {
      source  = "hashicorp/oci"
      version = "~> 4.0"
    }
  }
}

# Configure the OCI Provider
provider "oci" {
  tenancy_ocid        = "${var.tenancy_ocid}"
  user_ocid           = "${var.user_ocid}"
  fingerprint         = "${var.fingerprint}"
  private_key_path    = "${var.private_key_path}"
  region              = "${var.region}"
}

# Resto de tu configuración

