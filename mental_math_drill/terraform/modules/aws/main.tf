provider "aws" {
  region  = var.region
  profile = var.aws_profile
}

data "aws_caller_identity" "current" {}

locals {
  aws_account_id = data.aws_caller_identity.current.account_id
}

# iam roles
resource "aws_iam_role" "lambda_execution_role" {
  name = "mental-math-drill-lambda-execution-tf"

  assume_role_policy = <<-POLICY
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Effect": "Allow",
                  "Principal": {
                      "Service": "lambda.amazonaws.com"
                  },
                  "Action": "sts:AssumeRole"
              }
          ]
      }
  POLICY

  inline_policy {
    name   = "write-logs"
    policy = <<-POLICY
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "logs:CreateLogGroup",
                    "Resource": "arn:aws:logs:${var.region}:${local.aws_account_id}:*"
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "logs:CreateLogStream",
                        "logs:PutLogEvents"
                    ],
                    "Resource": [
                        "arn:aws:logs:${var.region}:${local.aws_account_id}:log-group:/aws/lambda/${var.lambda_function_name}:*" 
                    ]
                }
            ]
        }
    POLICY
  }

  inline_policy {
    name   = "send-ses-email"
    policy = <<-POLICY
        {
          "Version": "2012-10-17",
              "Statement": [
                  {
                      "Effect": "Allow",
                      "Action": [
                          "ses:SendEmail",
                          "ses:SendRawEmail"
                      ],
                      "Resource": "*"
                  }
              ]        
        }
    POLICY
  }
}

resource "aws_iam_role" "eventbridge_execution_role" {
  name = "mental-math-drill-eventbridge-execution-tf"

  assume_role_policy = <<-POLICY
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Effect": "Allow",
                  "Principal": {
                      "Service": "scheduler.amazonaws.com"
                  },
                  "Action": "sts:AssumeRole",
                  "Condition": {
                      "StringEquals": {
                          "aws:SourceAccount": "${local.aws_account_id}"
                      }
                  }
              }
          ]
      }
  POLICY

  inline_policy {
    name   = "invoke-lambda"
    policy = <<-POLICY
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "lambda:InvokeFunction"
                    ],
                    "Resource": [
                        "arn:aws:lambda:us-east-1:${local.aws_account_id}:function:${var.lambda_function_name}:*",
                        "arn:aws:lambda:us-east-1:${local.aws_account_id}:function:${var.lambda_function_name}"
                    ]
                }
            ]
        }
    POLICY
  }
}

data "archive_file" "lambda_files" {
  type        = "zip"
  source_dir  = "${path.root}/../src/"
  output_path = "${path.root}/lambda_deployment.zip"

  excludes = [".env", "__pycache__"]
}

resource "terraform_data" "archive_lambda_layer" {
  provisioner "local-exec" {
    interpreter = ["/bin/bash", "-c"]
    command     = <<-COMMANDS
        mkdir python
        cp -r ../venv/lib python/
        zip -r -q layer_content.zip python
        rm -r python
        echo "layer_content.zip is ready"
      COMMANDS
  }
}

# lambda artifacts
resource "aws_lambda_function" "lambda_function" {
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda_execution_role.arn
  filename      = data.archive_file.lambda_files.output_path
  handler       = "main.main"
  runtime       = "python3.10"
  layers        = [aws_lambda_layer_version.lambda_layer.arn]

  environment {
    variables = {
      "MMD_SENDER"    = var.email_sender,
      "MMD_RECIPIENT" = var.email_recipient
      "MMD_NUM_PROBS" = var.problem_count
      "MMD_USE_ADD"   = var.problem_use_add
      "MMD_USE_SUB"   = var.problem_use_sub
      "MMD_USE_MUL"   = var.problem_use_mul
      "MMD_USE_DIV"   = var.problem_use_div
    }
  }
}

resource "aws_lambda_layer_version" "lambda_layer" {
  layer_name          = var.lambda_layer_name
  filename            = "${path.root}/layer_content.zip"
  compatible_runtimes = ["python3.10"]

  depends_on = [terraform_data.archive_lambda_layer]
}

# eventbridge artifacts
resource "aws_scheduler_schedule" "eventbridge_scheduler" {
  name                         = "mental-math-drill-tf"
  group_name                   = "default"
  schedule_expression          = "cron(${var.email_cron_schedule})"
  schedule_expression_timezone = var.email_cron_schedule_timezone

  flexible_time_window {
    maximum_window_in_minutes = 5
    mode                      = "FLEXIBLE"
  }
  target {
    arn      = aws_lambda_function.lambda_function.arn
    role_arn = aws_iam_role.eventbridge_execution_role.arn
    retry_policy {
      maximum_event_age_in_seconds = 7200
      maximum_retry_attempts       = 2
    }
  }
}