# AWS Platform and Applications Monorepository

> This projects creates AWS Infra for application deploed as per the requirements.

### Repository Organization

The aws platform monorepository is used to build and deploy aws infra and applications in the cloud based on CDK Python.

    cdk-cs-assignment
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

At this location all stacks will be stored.

## `/stages`: Define Stages here for deploying inside pipeline.

At this location all stages will be stored. A stage can have a stack or group of stacks deployed together.

## `/lambda`: lambda code

We use lambda folder to store all lambda core under it's own handler folder

## `/tests`: Tests

We use thisfor _unit_ tests:

- **unit tests** should test the smallest independent units of your package code, i.e., functions or classes that only accomplish one piece of functionality.
  Each unit test should run very fast and should not connect to external services like AWS.

## `Bootstraping Process`

This project is fully automated using CDK pipelines using Python. If you you like to deploy in a fresh account bootstraping is required and follow AWS Documentation for bootstraping.

Bootstraping AWS: https://github.com/awsdocs/aws-cdk-guide/blob/main/v2/bootstrapping.md

## `Infra used`

In this CDK project we creates a custom VPC for our use case.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project. The initialization process also creates a `virtualenv` within this project, stored under the .env directory. To create the `virtualenv` it assumes that there is a `python3` (or python for Windows) executable in your path with access to the `venv` package. If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv manually.

## `VPC Specs`

`VPC`:

- VPC has been customized to project requirements where we have 2 `subnets` private with public in 3 `AZ's` of Ireland region with a NAT Gatway attached to private subnets.

## `Serverless App`

As per project requirements, everything that i used here are completely serverless.

- 2 Lambda functions with SQS queues, DynamoDB and an S3 bucket has been chosen.
- This will make sure that as per requirement, Lambda functions will take care of processing CSV data. - Triggers has been created to make lambda's are invoked on s3 puts and data to be stored in a DynamoDb table.
- CSV data can be uploaded directly from this project instead of manually uploading to s3 bucket. For this to happen place your data in directory `csv_data`.
- In case if there are any issues processing the messages, dead-letter queue store the messages, while main sqs takes takes care of the reading messages from lambda.

## `Container App`

As per project requirements, I created a container application and exposed it with a friendly Route53 url.

- A factorial of a given number has to be returned back to the user.
- I have decided to keep things simple, and chose to inflate a flask app that accepts user input through an api and returns factorial value.
- For the underlying resources, I have used Fargate cluster with a service running all the time which listens to an application load balancer.
- ALB recieves traffic from route_53 url. Security is an important aspect here so an acm certificate will be created and used with our route53 url.
- Fargate cluster will make use of our VPC created earlier and placed a dependency to make sure VPC is availaable before creation of our container stack.
- A docker image will be created automatically and used in our fargare resources, where the ecr repo holds the image.
- This application can be accessed with a url at `https://yourdomainname//api/v1/factorial?number=some_x_number`

## `Deployment Process`

`Usage`:

- Bootstrap your environment for your aws account and region as aws documentation.
- Clone the repository, make necessary changes for environment, account_id, Route_53 domain name, and reposity name of your choice for further development.
- push your changes to repo and as a final step make sure to `cdk deploy` for once.
- This will make sure to create an automated cicd pipeline pipeline which will deploy your resources defined.
- In case if you would like to develop further make sure to commit your code and on successful merge to master pipeline will get triggered and respective resources, apps will be deployed.
