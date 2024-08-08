variable "aws_email_sender" {
  description = "Address of email sender; must be verified on SES"
  type        = string
  nullable    = false
}

variable "aws_email_recipient" {
  description = "Address of email recipient; must be verified on SES if in sandbox"
  type        = string
  nullable    = false
}

variable "aws_email_cron_schedule" {
  description = "Cron schedule of when email should be sent"
  type        = string
  default     = "5 11 ? * 2-7 *"
}

variable "aws_email_cron_schedule_timezone" {
  description = "Time zone associated with cron schedule for when email should be sent"
  type        = string
  default     = "UTC"
}

variable "aws_problem_count" {
  description = "Number of problems to have in email; will be used as lambda environment variable"
  type        = string
  default     = "5"
}

variable "aws_problem_use_add" {
  description = "Include addition problems; will be used as lambda environment variable; 1 = yes, 2 = no"
  type        = string
  default     = "1"
}

variable "aws_problem_use_sub" {
  description = "Include subtraction problems; will be used as lambda environment variable; 1 = yes, 2 = no"
  type        = string
  default     = "1"
}

variable "aws_problem_use_mul" {
  description = "Include multiplication problems; will be used as lambda environment variable; 1 = yes, 2 = no"
  type        = string
  default     = "0"
}

variable "aws_problem_use_div" {
  description = "Include divison problems; will be used as lambda environment variable; 1 = yes, 2 = no"
  type        = string
  default     = "0"
}