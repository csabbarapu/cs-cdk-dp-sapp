#!/usr/bin/env python3
import os
import aws_cdk as cdk
from operations.get_aws_env import get_aws_env
from cdk_pipeline.pipeline_stack import PipelineStack

app = cdk.App()
aws_env = get_aws_env()

# Pipeline for this project
pipeline_stack = PipelineStack(
    app,
    "cs-pipeline-stack",
    env=aws_env,
)

app.synth()
