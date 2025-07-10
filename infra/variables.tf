variable "vpc_id" {
  description = "VPC ID para el clúster EKS"
  type        = string
}

variable "subnet_ids" {
  description = "Lista de subredes para el clúster EKS"
  type        = list(string)
} 