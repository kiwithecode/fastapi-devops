module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "devops-cluster"
  cluster_version = "1.29"
  subnet_ids      = ["<subnet-ids>"]
  vpc_id          = "<vpc-id>"
  node_groups = {
    devops_nodes = {
      desired_capacity = 2
      max_capacity     = 3
      min_capacity     = 1
      instance_type    = "t3.medium"
    }
  }
} 