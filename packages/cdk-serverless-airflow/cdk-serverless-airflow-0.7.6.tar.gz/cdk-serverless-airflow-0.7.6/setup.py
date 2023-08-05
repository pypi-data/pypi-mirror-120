import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-serverless-airflow",
    "version": "0.7.6",
    "description": "cdk-serverless-airflow",
    "license": "Apache-2.0",
    "url": "https://github.com/readybuilderone/serverless-airflow.git",
    "long_description_content_type": "text/markdown",
    "author": "readybuilderone<neohan2016@outlook.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/readybuilderone/serverless-airflow.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_serverless_airflow",
        "cdk_serverless_airflow._jsii"
    ],
    "package_data": {
        "cdk_serverless_airflow._jsii": [
            "cdk-serverless-airflow@0.7.6.jsii.tgz"
        ],
        "cdk_serverless_airflow": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-ec2>=1.95.2, <2.0.0",
        "aws-cdk.aws-ecr-assets>=1.95.2, <2.0.0",
        "aws-cdk.aws-ecr>=1.95.2, <2.0.0",
        "aws-cdk.aws-ecs-patterns>=1.95.2, <2.0.0",
        "aws-cdk.aws-ecs>=1.95.2, <2.0.0",
        "aws-cdk.aws-elasticache>=1.95.2, <2.0.0",
        "aws-cdk.aws-events>=1.95.2, <2.0.0",
        "aws-cdk.aws-iam>=1.95.2, <2.0.0",
        "aws-cdk.aws-logs>=1.95.2, <2.0.0",
        "aws-cdk.aws-rds>=1.95.2, <2.0.0",
        "aws-cdk.aws-s3>=1.95.2, <2.0.0",
        "aws-cdk.aws-secretsmanager>=1.95.2, <2.0.0",
        "aws-cdk.aws-servicediscovery>=1.95.2, <2.0.0",
        "aws-cdk.core>=1.95.2, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.34.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
