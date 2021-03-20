terraform {
  required_version = "~> 0.12.24" # which means ">= 0.12.24" and "< 0.13"
  backend "s3" {}
}
