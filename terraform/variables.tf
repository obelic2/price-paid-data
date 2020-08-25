# Variables for build GCP

variable "region" {
    type = string
    default = "us-west1"
    description = "Default region for GCP Always Free"
}

variable "zone" {
    type = string
    default = "us-west1-a"
    description = "Default zone for GCP Always Free"
}

variable "gcp_project" {
    type = string
}