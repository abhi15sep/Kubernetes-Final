# Limitations with eksctl Manated Nodes

# 1. Can't use Bootstrap Userdata script for EKS worker nodes
Briefly mentioned in chapter 10: IRSA, when blocking access to instance metadata.

Run commands to change iptables:
```bash
yum install -y iptables-services
iptables --insert FORWARD 1 --in-interface eni+ --destination 169.254.169.254/32 --jump DROP
iptables-save | tee /etc/sysconfig/iptables 
systemctl enable --now iptables
```

Ideally, you should add the above script to userdata script in launch configuration so all the worker nodes starting up will execute shell commands.

Also, there are __some downsides__ to managed node groups ([eksctl doc](https://eksctl.io/usage/eks-managed-nodes/#feature-parity-with-unmanaged-nodegroups)):
> Control over the node bootstrapping process and customization of the kubelet are not supported. This includes the following fields: classicLoadBalancerNames, maxPodsPerNode, __taints__, targetGroupARNs, preBootstrapCommands, __overrideBootstrapCommand__, clusterDNS and __kubeletExtraConfig__.


This means if you want to auto-mount EFS to newly spawned EKS worker nodes using bootstrap userdata script like below, you __cant't__.

```bash
sudo mkdir /mnt/efs

sudo mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport fs-xxxxx.efs.us-east-1.amazonaws.com:/ /mnt/efs

echo 'fs-xxxxx.efs.us-east-1.amazonaws.com:/ /mnt/efs nfs defaults,vers=4.1 0 0' >> /etc/fstab
```

This is another reason why in production, you should be using [Terraform and __Unmanaged Node Groups__](https://github.com/terraform-aws-modules/terraform-aws-eks/blob/master/examples/irsa/main.tf#L64)


# 2. Can't Taint EKS Worker nodes from ASG argument like you could in Unmanaged Node Groups

This is quite important because in production, some nodes will be labeled and tained like `env=prod` and `prod-only=true:PreferNoSchedule`, and if new nodes are getting auto-scaled up but not labeled/tainted, pods with __NodeAffinity__ and __Tolerance__ can't be assigned to those new nodes, hence Cluster Autoscaler will spit out error 
```
pod didn't trigger scale-up (it wouldn't fit if a new node is added)
```



# Resolution: Use Unmanaged Node and Deploy EKS with Terraform in Produciton!

This is exactly how I inject a map of unmanaged worker group, with userdata script argument for 1) blocking access to instance metadata, 2) auto-mounting EFS, and 3) adding K8s taints in `terraform.tfvars`:

```sh
# note (only for unmanaged node group)
# gotcha: need to use kubelet_extra_args to propagate taints/labels to K8s node, because ASG tags not being propagated to k8s node objects.
# ref: https://github.com/kubernetes/autoscaler/issues/1793#issuecomment-517417680
# ref: https://github.com/kubernetes/autoscaler/issues/2434#issuecomment-576479025
worker_groups = [
  {
    name          = "worker-group-staging-1"
    instance_type = "m3.xlarge"
    asg_max_size  = 3
    asg_desired_capacity = 1 # this will be ignored if cluster autoscaler is enabled: asg_desired_capacity: https://github.com/terraform-aws-modules/terraform-aws-eks/blob/master/docs/autoscaling.md#notes

    # ref: https://docs.aws.amazon.com/eks/latest/userguide/restrict-ec2-credential-access.html  
    # this userdata will block access to metadata to avoid pods from using node's IAM instance profile, and also create /mnt/efs and auto-mount EFS to it using fstab. Note: userdata script doesn't resolve shell variable defined within
    additional_userdata  = "yum install -y iptables-services; iptables --insert FORWARD 1 --in-interface eni+ --destination 169.254.169.254/32 --jump DROP; iptables-save | tee /etc/sysconfig/iptables; systemctl enable --now iptables; sudo mkdir /mnt/efs; sudo mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport fs-xxxxx.efs.us-east-1.amazonaws.com:/ /mnt/efs; echo 'fs-xxxxx.efs.us-east-1.amazonaws.com:/ /mnt/efs nfs defaults,vers=4.1 0 0' >> /etc/fstab"
    kubelet_extra_args   = "--node-labels=env=staging,unmanaged-node=true --register-with-taints=staging-only=true:PreferNoSchedule" # for unmanaged nodes, taints and labels work only with extra-arg, not ASG tags. Ref: https://aws.amazon.com/blogs/opensource/improvements-eks-worker-node-provisioning/
    tags = [
      {
        "key"                 = "unmanaged-node"
        "propagate_at_launch" = "true"
        "value"               = "true"
      },
      {
        "key"                 = "k8s.io/cluster-autoscaler/enabled" # need this tag so clusterautoscaler auto-discovers node group: https://github.com/terraform-aws-modules/terraform-aws-eks/blob/master/docs/autoscaling.md
        "propagate_at_launch" = "true"
        "value"               = "true"
      },
    ]
  },
}
```