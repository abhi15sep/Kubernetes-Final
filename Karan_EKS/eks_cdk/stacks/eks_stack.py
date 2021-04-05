from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_eks as eks,
    core
) 

class EKSStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        k8s_admin = iam.Role(self, "k8sadmin",
            assumed_by=iam.ServicePrincipal(service='ec2.amazonaws.com'),
            role_name='eks-master-role',
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
                    managed_policy_name='AdministratorAccess'
                )
            ]
        
        )

        k8s_instance_profile = iam.CfnInstanceProfile(self, 'instanceprofile',
            roles=[k8s_admin.role_name],
            instance_profile_name='eks-master-role'
        )


        cluster = eks.Cluster(self, 'dev',
            cluster_name='eks-cdk-demo',
            version='1.15',
            vpc=vpc,
            vpc_subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE)],
            default_capacity=0,
            kubectl_enabled=True,
            #security_group=k8s_sg,
            masters_role= k8s_admin

        )
        #cluster.aws_auth.add_user_mapping(adminuser, {groups['system:masters']})
       
        ng = cluster.add_nodegroup('eks-ng',
            nodegroup_name='eks-ng',
            instance_type=ec2.InstanceType('t3.medium'),
            disk_size=5,
            min_size=2,
            max_size=2,
            desired_size=2,
            #node_role=node_role,
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
            remote_access=eks.NodegroupRemoteAccess(ssh_key_name='k8s-nodes')
            
        )

        
        