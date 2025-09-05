terraform {
  required_version = ">= 1.4"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.115"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "azurerm" {
  features {}
}

# --- Resource group ---
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

# --- Storage account (name must be globally unique; use a random suffix) ---
resource "random_string" "sa_suffix" {
  length  = 8
  upper   = false
  numeric = true
  special = false
}

resource "azurerm_storage_account" "sa" {
  name                     = "${var.storage_account_prefix}${random_string.sa_suffix.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
  allow_blob_public_access = false
}

# --- Blob container named "atlas" (lowercase required) ---
resource "azurerm_storage_container" "atlas" {
  name                  = "atlas"
  storage_account_name  = azurerm_storage_account.sa.name
  container_access_type = "private"
}

# Handy outputs
output "resource_group_name"   { value = azurerm_resource_group.rg.name }
output "storage_account_name"  { value = azurerm_storage_account.sa.name }
output "container_name"        { value = azurerm_storage_container.atlas.name }
