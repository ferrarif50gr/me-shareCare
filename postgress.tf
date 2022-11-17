# setup the GCP provider

terraform {
  required_version = ">= 0.12"
}

# provider "google" {
#  project     = "my-gcp-project"
#  credentials = file("kopicloud-tfadmin.json")
#  region      = "europe-west1"
#  zone        = "europe-west1-b"
# }

resource "google_sql_database_instance" "postgresql" {
  name = "${var.app_name}-db1"
  project = "${var.project_id}"
  region = "${var.db_region}"
  database_version = "${var.db_version}"
  
  settings {
    tier = "${var.db_tier}"
    activation_policy = "${var.db_activation_policy}"
    disk_autoresize = "${var.db_disk_autoresize}"
    disk_size = "${var.db_disk_size}"
    disk_type = "${var.db_disk_type}"
    pricing_plan = "${var.db_pricing_plan}"
    
    location_preference {
      zone = "${var.db_zone}"
    }
   
    maintenance_window {
      day  = "7"  # sunday
      hour = "3" # 3am
    }

   
    backup_configuration {
      binary_log_enabled = false
      enabled = true
      start_time = "00:00"
    }
   
    ip_configuration {
      ipv4_enabled = "true"
      authorized_networks {
        value = "${var.db_instance_access_cidr}"
      }
    }
  }
}

# create database
resource "google_sql_database" "postgresql_db" {
  name = "${var.db_name}"
  project = "${var.app_project}"
  instance = "${google_sql_database_instance.postgresql.name}"
  charset = "${var.db_charset}"
  collation = "${var.db_collation}"
}

# create user
resource "random_id" "user_password" {
  byte_length = 8
}
resource "google_sql_user" "postgresql_user" {
  name = "${var.db_user_name}"
  project  = "${var.app_project}"
  instance = "${google_sql_database_instance.postgresql.name}"
  host = "${var.db_user_host}"
  password = "${var.db_user_password == "" ?
    random_id.user_password.hex : var.db_user_password}"
}
