variable bucket_name {
  type = string
  # Description = "The name of our bucket"
  default = "share-care-bucket"
}

variable bucket_location {
  type = string
  default = "europe-west1"
}

variable storage_class {
  type = string
  default = "STANDARD"
}

resource "google_storage_bucket" "default" {
  name = var.bucket_name
  storage_class = var.storage_class
  location = var.bucket_location
}