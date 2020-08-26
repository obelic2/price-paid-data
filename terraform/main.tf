# Terraform to build resources in GCP

terraform {
  required_version = "0.13.0"
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "3.36.0"
    }
  }
}

provider "google" {
  project = var.gcp_project
  region  = var.region
  zone = var.zone
}

# resource "google_compute_instance" "vm_instance" {
#   name         = "beam-runner"
#   machine_type = "f1-micro"
#   zone = var.zone

#   boot_disk {
#     initialize_params {
#       image = "debian-cloud/debian-9"
#     }
#   }

#   network_interface {
#     # A default network is created for all GCP projects
#     network = google_compute_network.vpc_network.self_link
#     access_config {
#     }
#   }
# }

# resource "google_compute_network" "vpc_network" {
#   name                    = "terraform-network"
#   auto_create_subnetworks = "true"
# }

resource "google_storage_bucket" "beam_storage" {
  name = "uk-housing-prices"
  location = var.region
  project = var.gcp_project  
}
