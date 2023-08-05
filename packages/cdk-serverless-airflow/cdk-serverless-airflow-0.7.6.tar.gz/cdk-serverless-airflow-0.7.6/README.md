[![Build](https://github.com/readybuilderone/serverless-airflow/actions/workflows/build.yml/badge.svg)](https://github.com/readybuilderone/serverless-airflow/actions/workflows/build.yml)
[![NPM version](https://badge.fury.io/js/cdk-serverless-airflow.svg)](https://badge.fury.io/js/cdk-serverless-airflow)
[![PyPI version](https://badge.fury.io/py/cdk-serverless-airflow.svg)](https://badge.fury.io/py/cdk-serverless-airflow)
[![construct hub](https://img.shields.io/badge/Construct%20Hub-available-blue)](https://constructs.dev/packages/cdk-serverless-airflow)

# `CDK Serverless Airflow`

CDK construct library that allows you to create [Apache Airflow](https://airflow.apache.org/) on AWS in TypeScript or Python

# Architecture

![architecture](./assets/01-serverless-airflow-on-aws-architecture.svg)

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
import cdk_serverless_airflow as airflow

app = cdk.App()
env = {
    "region": process.env.CDK_DEFAULT_REGION,
    "account": process.env.CDK_DEFAULT_ACCOUNT
}
stack = cdk.Stack(app, "airflow-stack",
    env=env
)
airflow.Airflow(stack, "Airflow")
```

# Airflow Dashboard

> Default Credential: user/bitnami

![airflow-dashboard](./assets/04-airflow-dashboard.jpg)

# AWS China Regions

AWS China regions `cn-north-1` and `cn-northwest-1` are supported by this Library.

## License

This project is licensed under the Apache-2.0 License.
