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
  tenancy_ocid         = "TU_TENANCY_OCID"
  user_ocid            = "TU_USER_OCID"
  fingerprint         = "TU_FINGERPRINT"
  private_key_path    = "RUTA_A_TU_CLAVE_PRIVADA"
  region              = "TU_REGION"
}

# Resto de tu configuración

