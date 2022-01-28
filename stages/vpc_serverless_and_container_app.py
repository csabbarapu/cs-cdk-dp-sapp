import aws_cdk as cdk
from constructs import Construct
from packages.container_stack import ContainerStack
from packages.serverless_stack import ServerlessStack
from packages.vpc_stack import VpcStack


class DeployAll(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC for using in combination with container app
        self.vpc_stack = VpcStack(
            self,
            "cs-vpc-stack",
        )

        # ContainerApp
        self.container_stack = ContainerStack(
            self, "cs-container-stack", vpc=self.vpc_stack.vpc
        )

        # Add dependency on vpc stack
        self.container_stack.add_dependency(self.vpc_stack)

        # ServerlessApp
        self.serverless_stack = ServerlessStack(
            self,
            "cs-serverless-stack",
        )
