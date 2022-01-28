from constructs import Construct
from aws_cdk import (
    aws_ecs_patterns as ecs_patterns,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_route53 as route53,
    aws_elasticloadbalancingv2 as elbv2,
    Stack,
)


class ContainerStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, vpc: ec2.IVpc, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Hardcoding the ID for simplicity - normally I'd pass it as a parameter into this

        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self,
            "AssignmentHostedZone",
            hosted_zone_id="Z0328032U3BO7WC50ZWK",
            zone_name="cloudwithcs.com",
        )

        factorial_api = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "FactorialApiService",
            service_name="cs-factorial-api-service",
            vpc=vpc,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset(directory="./container"),
                container_port=5000,
                container_name="factorialApi",
            ),
            domain_name="cloudwithcs.com",
            domain_zone=hosted_zone,
            protocol=elbv2.ApplicationProtocol.HTTPS,
            redirect_http=True,
            desired_count=1,
        )

        factorial_api.target_group.configure_health_check(path="/status", port="5000")
