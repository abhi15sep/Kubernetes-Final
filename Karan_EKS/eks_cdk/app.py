#!/usr/bin/env python3

from aws_cdk import core
from stacks.vpc_stack import VPCStack

#To create new VPC
from stacks.eks_stack import EKSStack

#Enable if you have existing VPC
#from stacks.eks_stack_existing_vpc import EKSStack

app = core.App()

vpc_stack = VPCStack(app, 'vpc')
eks_stack = EKSStack(app, 'eks', vpc=vpc_stack.vpc)

#Enable if you have existing VPC
#eks_stack = EKSStack(app, 'eks')

app.synth()