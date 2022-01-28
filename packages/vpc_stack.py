from aws_cdk import Stack, aws_ec2 as ec2
from constructs import Construct


class VpcStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            "CsCdkVpc",
            vpc_name="cs-cdk-vpc",
            max_azs=3,
            cidr="10.10.0.0/16",
            enable_dns_support=True,
            # configuration will create 2 subnet groups in 3 AZs = 6 subnets.
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Public",
                    cidr_mask=24,
                    map_public_ip_on_launch=True,
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                    name="Private",
                    cidr_mask=24,
                ),
            ],
            nat_gateways=1,
        )
