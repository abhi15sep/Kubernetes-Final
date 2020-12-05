# 13. Networking: Limitations with the Default CNI AWS-VPC-CNI: Pod IP exhaustion based on instance size

Refs:
- [AWS EKS Instance types & Pod IP size spreadsheet](https://docs.google.com/spreadsheets/d/1MCdsmN7fWbebscGizcK6dAaPGS-8T_dYxWp0IdwkMKI/edit#gid=1549051942)
- [List of EC2 instance types and max # of Pod IPs](https://github.com/awslabs/amazon-eks-ami/blob/master/files/eni-max-pods.txt)

Pod IPs will be exhausted and you will see `0/1 nodes are available: 1 Insufficient pods.` error.
```
Events:
  Type     Reason            Age                  From               Message
  ----     ------            ----                 ----               -------
  Warning  FailedScheduling  33s (x4 over 2m22s)  default-scheduler  0/1 nodes are available: 1 Insufficient pods.
```

# Resolution

You would increase EKS Worker nodes instance type or install other CNI such as Calico.