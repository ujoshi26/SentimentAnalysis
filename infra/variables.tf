variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus"
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
  default     = "rg-atlas-dev"
}

variable "storage_account_prefix" {
  description = "Prefix for storage account (lowercase letters/numbers only)"
  type        = string
  default     = "atlas"
}
