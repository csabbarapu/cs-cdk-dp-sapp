# AWS Platform and Applications Monorepository

> This project creates AWS Infra for applications deployed as per the requirements.

### Repository Organization

The AWS platform mono repository is used to build and deploy AWS infra and applications in the cloud based on CDK Python.

    cs-cdk-dp-sapp
    |
    +-- cdk_pipeline
    |   |
    |   +-- pipeline_stack.py
    +-- container
    |   |
    |   +-- Dockerfile
    |   +-- app/
    |   |   |
    |   |   +-- required files
    +-- packages
    |   |
    |   +-- stack_1
    |   |   |
    |   +-- stack_2
    |   |   |   |
    |   +-- stack_N
    +-- csv_data
    +-- lambda
    |   |
    |   +-- lambda_a/
    |   +-- lambda_b/
    +-- stages
    |   |
    |   +-- stage.py
    +-- tests
    |   |
    |   +-- unit_tests
    |   |   |
    |   |   +-- stack_1.py
    |   |   +-- stack_2.py
    +-- .gitignore
    +-- .pre-commit-config.yaml
    +-- .app.py
    +-- cdk.json
    +-- requirements.txt
    +-- README.md

## `/cdk_pipeline`: Pipeline_stack for CICD

At this location cdk pipeline stack will be stored.

## `/packages`: Packages

At this location, all stacks will be stored.

## `/stages`: Define Stages here for deploying inside the pipeline.

At this location, all stages will be stored. A stage can have a stack or group of stacks deployed together.

## `/lambda`: lambda code

We use a lambda folder to store all lambda core under its own handler folder

## `/tests`: Tests

We use thisfor _unit_ tests:

- **Unit tests** should test the smallest independent units of your package code, i.e., functions or classes that only accomplish one piece of functionality.
  Each unit test should run very fast and should not connect to external services like AWS.

## `Bootstrapping Process`

This project is fully automated using CDK pipelines using Python. If you you like to deploy in a fresh account bootstraping is required and follow AWS Documentation for bootstraping.

Bootstrapping AWS: https://github.com/awsdocs/aws-cdk-guide/blob/main/v2/bootstrapping.md

## `Infra used`

In this CDK project, we create a custom VPC for our use case.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project. The initialization process also creates a `virtualenv` within this project, stored under the .env directory. To create the `virtualenv` it assumes that there is a `python3` (or python for Windows) executable in your path with access to the `venv` package. If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv manually.

## `VPC Specs`

`VPC`:

- VPC has been customized to project requirements where we have 2 `subnets` private with the public in 3 `AZ's` of Ireland region with a NAT Gateway attached to private subnets.

## `Serverless App`

As per project requirements, everything that I used here is completely serverless.

- 2 Lambda functions with SQS queues, DynamoDB, and an S3 bucket have been chosen.
- This will make sure that as per requirement, Lambda functions will take care of processing CSV data. - Triggers have been created to make lambda's invoked on s3 puts and data to be stored in a DynamoDb table.
- CSV data can be uploaded directly from this project instead of manually uploading to the s3 bucket. For this to happen place your data in the directory `csv_data`.
- In case there are any issues processing the messages, the dead-letter queue stores the messages, while the main SQS takes care of the reading messages from lambda.

## `Container App`

As per project requirements, I created a container application and exposed it with a friendly Route53 URL.

- A factorial of a given number has to be returned back to the user.
- I have decided to keep things simple and chose to inflate a Flask app that accepts user input through an API and returns the factorial value.
- For the underlying resources, I have used Fargate cluster with a service running all the time that listens to an application load balancer.
- ALB receives traffic from route_53 URL. Security is an important aspect here so an ACM certificate will be created and used with our route53 URL.
- Fargate cluster will make use of our VPC created earlier and place a dependency to make sure VPC is available before the creation of our container stack.
- A docker image will be created automatically and used in our fargate resources, where the ECR repo holds the image.
- This application can be accessed with a URL at `https://yourdomainname//api/v1/factorial?number=some_x_number`

## `Deployment Process`

`Usage`:

- Bootstrap your environment for your AWS account and region as AWS documentation.
- Clone the repository, and make necessary changes for the environment, account_id, Route_53 domain name, and repository name of your choice for further development.
- push your changes to the repo and as a final step make sure to `cdk deploy` for once.
- This will make sure to create an automated CICD pipeline pipeline which will deploy your resources defined.
- In case you would like to develop further make sure to commit your code and on successful merge to the master pipeline will get triggered and respective resources, and apps will be deployed.
