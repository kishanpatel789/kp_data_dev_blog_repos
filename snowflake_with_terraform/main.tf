terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.86"
    }
  }

  backend "local" {}
}

module "snowflake" {
  source = "./modules/snowflake"

  service_user_password = var.snowflake_service_user_password
}