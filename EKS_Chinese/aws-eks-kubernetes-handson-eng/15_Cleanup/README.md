# Cleanup

Delete EKS Cluster
```bash
eksctl delete cluster --name eks-from-eksctl --region us-west-2

# output
[ℹ]  eksctl version 0.21.0
[ℹ]  using region us-west-2
[ℹ]  deleting EKS cluster "eks-from-eksctl"
[ℹ]  deleted 0 Fargate profile(s)
[✔]  kubeconfig has been updated
[ℹ]  cleaning up LoadBalancer services
[ℹ]  3 sequential tasks: { delete nodegroup "workers", 2 sequential sub-tasks: { 2 parallel sub-tasks: { 2 sequential sub-tasks: { delete IAM role for serviceaccount "kube-system/cluster-autoscaler-aws-cluster-autoscaler", delete serviceaccount "kube-system/cluster-autoscaler-aws-cluster-autoscaler" }, 2 sequential sub-tasks: { delete IAM role for serviceaccount "default/irsa-service-account", delete serviceaccount "default/irsa-service-account" } }, delete IAM OIDC provider }, delete cluster control plane "eks-from-eksctl" [async] }
[ℹ]  will delete stack "eksctl-eks-from-eksctl-nodegroup-workers"
[ℹ]  waiting for stack "eksctl-eks-from-eksctl-nodegroup-workers" to get deleted
[ℹ]  will delete stack "eksctl-eks-from-eksctl-addon-iamserviceaccount-default-irsa-service-account"
[ℹ]  waiting for stack "eksctl-eks-from-eksctl-addon-iamserviceaccount-default-irsa-service-account" to get deleted
[ℹ]  will delete stack "eksctl-eks-from-eksctl-addon-iamserviceaccount-kube-system-cluster-autoscaler-aws-cluster-autoscaler"
[ℹ]  waiting for stack "eksctl-eks-from-eksctl-addon-iamserviceaccount-kube-system-cluster-autoscaler-aws-cluster-autoscaler" to get deleted
[ℹ]  deleted serviceaccount "default/irsa-service-account"
[ℹ]  deleted serviceaccount "kube-system/cluster-autoscaler-aws-cluster-autoscaler"
[ℹ]  will delete stack "eksctl-eks-from-eksctl-cluster"
[✔]  all cluster resources were deleted
```

Delete S3 bucket created for ELB access logs from Console



