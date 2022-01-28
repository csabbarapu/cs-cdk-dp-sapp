import aws_cdk as cdk
from aws_cdk import (
    aws_codecommit as codecommit,
    pipelines as pipelines,
    Stack,
)
from constructs import Construct
from operations.get_aws_env import get_aws_env
from stages.vpc_serverless_and_container_app import DeployAll


class PipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Defining Environment
        env = get_aws_env

        # We are creating an codecommit repo.
        # todo Uncomment following code block if you are creating a fresh project.
        # self.repository = codecommit.Repository(
        #     self,
        #     "CsAssignmentCreateRepository",
        #     repository_name="cs-assignment",
        #     description="This repo holds source code for cdk python developemet \
        #                 of AWSInfra,Serverless and Container applications with a Pipeline.",
        # )

        # We are importing an existing codecommit repo here.
        # todo Comment following code block if you are creating a fresh project.
        # self.repository = codecommit.Repository.from_repository_name(
        #     self, "ImportRepo", "cdk-cs-assignment"
        # )

        # We are creating a pipeline for deploying to AWS account.
        self.pipeline = pipelines.CodePipeline(
            self,
            "CsPipeline",
            pipeline_name="cs-cdk-cicd-pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.git_hub(
                    "chaitanyasabbarapu/cs-cdk-dp-sapp",
                    branch="main",
                ),
                commands=[
                    "npm install -g aws-cdk",
                    "gem install cfn-nag",
                    "pip install -r requirements.txt",
                    "cdk synth",
                    "mkdir ./cfnnag_output",
                    "for template in $(find ./cdk.out -type f -maxdepth 2  \
                        -name '*.template.json'); do cp $template ./cfnnag_output; done",
                    "cfn_nag_scan --input-path ./cfnnag_output",
                ],
            ),
        )

        # Passing VPC Serverless, and Container stacks in a stage to pipeline
        self.deploy = self.pipeline.add_stage(
            DeployAll(self, "Deploy", env=env),
        )
        # self.destroy = self.pipeline.add_stage(
        #     DeployAll(self, "Destroy", env=env),
        # )
        # self.destroy.add_post(pipelines.ManualApprovalStep("approval"))
