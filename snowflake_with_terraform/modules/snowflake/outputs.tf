output "snowflake_warehouse_name" {
  value = snowflake_warehouse.hogwarts_wh.name
}

output "snowflake_service_user_username" {
  value = snowflake_user.svc_hogwarts.name
}