terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.86"
    }
  }
}

provider "snowflake" {
  profile = var.snowflake_profile
}

# database, schemas, warehouse
resource "snowflake_database" "hogwarts_db" {
  name                        = "HOGWARTS"
  data_retention_time_in_days = 0
}

resource "snowflake_schema" "raw" {
  database            = snowflake_database.hogwarts_db.name
  name                = "RAW"
  data_retention_days = 0
}

resource "snowflake_schema" "staged" {
  database            = snowflake_database.hogwarts_db.name
  name                = "STAGED"
  data_retention_days = 0
}

resource "snowflake_schema" "main" {
  database            = snowflake_database.hogwarts_db.name
  name                = "MAIN"
  data_retention_days = 0
}

resource "snowflake_warehouse" "hogwarts_wh" {
  name           = "HOGWARTS_WH"
  warehouse_type = "STANDARD"
  warehouse_size = "x-small"
  auto_resume    = true
  auto_suspend   = 600
}

# user and role
resource "snowflake_user" "svc_hogwarts" {
  name              = "SVC_HOGWARTS"
  password          = var.service_user_password
  default_warehouse = snowflake_warehouse.hogwarts_wh.name
  default_role      = snowflake_role.svc_hogwarts_role.name
  default_namespace = snowflake_database.hogwarts_db.name
}

resource "snowflake_role" "svc_hogwarts_role" {
  name = "SVC_HOGWARTS_ROLE"
}

resource "snowflake_grant_account_role" "grant_role" {
  role_name = snowflake_role.svc_hogwarts_role.name
  user_name = snowflake_user.svc_hogwarts.name
}

# service role privileges
resource "snowflake_grant_privileges_to_account_role" "db_usage" {
  privileges        = ["USAGE"]
  account_role_name = snowflake_role.svc_hogwarts_role.name
  on_account_object {
    object_type = "DATABASE"
    object_name = snowflake_database.hogwarts_db.name
  }
}

resource "snowflake_grant_privileges_to_account_role" "schema_privileges_raw" {
  privileges        = ["USAGE", "MODIFY", "CREATE TABLE", "CREATE VIEW"]
  account_role_name = snowflake_role.svc_hogwarts_role.name
  on_schema {
    schema_name = "\"${snowflake_database.hogwarts_db.name}\".\"${snowflake_schema.raw.name}\""
  }
}

resource "snowflake_grant_privileges_to_account_role" "schema_privileges_staged" {
  privileges        = ["USAGE", "MODIFY", "CREATE TABLE", "CREATE VIEW"]
  account_role_name = snowflake_role.svc_hogwarts_role.name
  on_schema {
    schema_name = "\"${snowflake_database.hogwarts_db.name}\".\"${snowflake_schema.staged.name}\""
  }
}

resource "snowflake_grant_privileges_to_account_role" "schema_privileges_main" {
  privileges        = ["USAGE", "MODIFY", "CREATE TABLE", "CREATE VIEW"]
  account_role_name = snowflake_role.svc_hogwarts_role.name
  on_schema {
    schema_name = "\"${snowflake_database.hogwarts_db.name}\".\"${snowflake_schema.main.name}\""
  }
}

resource "snowflake_grant_privileges_to_account_role" "table_privileges_raw" {
  privileges        = ["SELECT", "INSERT", "UPDATE", "DELETE"]
  account_role_name = snowflake_role.svc_hogwarts_role.name
  on_schema_object {
    all {
      object_type_plural = "TABLES"
      in_schema          = "\"${snowflake_database.hogwarts_db.name}\".\"${snowflake_schema.raw.name}\""
    }
  }
}

resource "snowflake_grant_privileges_to_account_role" "future_table_privileges_raw" {
  privileges        = ["SELECT", "INSERT", "UPDATE", "DELETE"]
  account_role_name = snowflake_role.svc_hogwarts_role.name
  on_schema_object {
    future {
      object_type_plural = "TABLES"
      in_schema          = "\"${snowflake_database.hogwarts_db.name}\".\"${snowflake_schema.raw.name}\""
    }
  }
}

resource "snowflake_grant_privileges_to_account_role" "table_privileges_staged" {
  privileges        = ["SELECT", "INSERT", "UPDATE", "DELETE"]
  account_role_name = snowflake_role.svc_hogwarts_role.name
  on_schema_object {
    all {
      object_type_plural = "TABLES"
      in_schema          = "\"${snowflake_database.hogwarts_db.name}\".\"${snowflake_schema.staged.name}\""
    }
  }
}

resource "snowflake_grant_privileges_to_account_role" "future_table_privileges_staged" {
  privileges        = ["SELECT", "INSERT", "UPDATE", "DELETE"]
  account_role_name = snowflake_role.svc_hogwarts_role.name
  on_schema_object {
    future {
      object_type_plural = "TABLES"
      in_schema          = "\"${snowflake_database.hogwarts_db.name}\".\"${snowflake_schema.staged.name}\""
    }
  }
}

resource "snowflake_grant_privileges_to_account_role" "table_privileges_main" {
  privileges        = ["SELECT", "INSERT", "UPDATE", "DELETE"]
  account_role_name = snowflake_role.svc_hogwarts_role.name
  on_schema_object {
    all {
      object_type_plural = "TABLES"
      in_schema          = "\"${snowflake_database.hogwarts_db.name}\".\"${snowflake_schema.main.name}\""
    }
  }
}

resource "snowflake_grant_privileges_to_account_role" "future_table_privileges_main" {
  privileges        = ["SELECT", "INSERT", "UPDATE", "DELETE"]
  account_role_name = snowflake_role.svc_hogwarts_role.name
  on_schema_object {
    future {
      object_type_plural = "TABLES"
      in_schema          = "\"${snowflake_database.hogwarts_db.name}\".\"${snowflake_schema.main.name}\""
    }
  }
}

resource "snowflake_grant_privileges_to_account_role" "warehouse_privileges" {
  privileges        = ["USAGE"]
  account_role_name = snowflake_role.svc_hogwarts_role.name
  on_account_object {
    object_type = "WAREHOUSE"
    object_name = snowflake_warehouse.hogwarts_wh.name
  }
}

resource "snowflake_grant_account_role" "svc_to_sysadmin" {
  role_name        = snowflake_role.svc_hogwarts_role.name
  parent_role_name = "SYSADMIN"
}
