import aws_cdk as core
import aws_cdk.assertions as assertions

from packages.vpc_stack import VpcStack
from packages.serverless_stack import ServerlessStack

# from packages.container_stack import ContainerStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_cs_assignment/cdk_cs_assignment_stack.py
def test_vpc_creation():
    app = core.App()
    vpc_stack = VpcStack(app, "test-vpc-creation")
    template = assertions.Template.from_stack(vpc_stack)


def test_serverless_app_creation():
    app = core.App()
    serverless_stack = ServerlessStack(app, "test-serverless-app-creation")
    template = assertions.Template.from_stack(serverless_stack)


# def test_container_app_creation():
#     app = core.App()
#     container_stack = ContainerStack(
#         app, "test-container-app-creation", vpc=test_vpc_creation.vpc_stack.vpc
#     )
#     template = assertions.Template.from_stack(container_stack)
