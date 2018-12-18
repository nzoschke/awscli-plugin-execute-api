# awscli-plugin-execute-api

Plugin to configure a single AWS CLI operation to invoke an API Gateway method

## Motivation

For security reasons we'd like to give an IAM user access to a **limited subset** of an AWS API call functionality. For example on the `dynamodb update-table` operation we'd like to allow a user to modify:

* Global indexes

But disallow them to modify:

* Provisioned throughput
* Streams
* Server side encryption

A "serverless" solution includes:

* IAM User
    * Policy that disallows `dynamodb:UpdateTable`
    * Policy that allows `execute-api:Invoke` on an API Gateway resource
    * Access keys

* API Gateway Method
    * URL to POST an `update-table` request
    * AWS_IAM authorization

* Lambda Function
    * Policy that allows `dynamodb:UpdateTable`
    * Code that validates and performs `update-table` request

* AWS CLI
    * Custom endpoint URL for `dynamodb update-table` command
    * Request signature for API Gateway

This plugin registers a URL for a single CLI operation and automatically uses it.

```shell
$ aws configure set dynamodb.update-table https://m303r7o808.execute-api.us-east-1.amazonaws.com/Prod/update-table
$ aws dynamodb update-table --table-name $TABLE_NAME --sse-specification Enabled=false
An error occurred (ValidationException) when calling the UpdateTable operation: Modifying SSESpecification is not allowed
```

## Quick Start

### Install with pip

```shell
$ pip install awscli-plugin-execute-api
```

If you installed `awscli` with Homebrew, use its bundled Python:

```shell
$ /usr/local/opt/awscli/libexec/bin/pip install awscli-plugin-execute-api
```

### Register the plugin

```shell
$ aws configure set plugins.execute-api awscli_plugin_execute_api
```

### Configure an operation endpoint

First configure a profile for the IAM user with `execute-api` policy:

```shell
$ export AWS_PROFILE=myprofile

$ aws configure
AWS Access Key ID [None]: AKIAIE5DIKNGIBVR75BQ
AWS Secret Access Key [None]: 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
Default region name [None]: us-east-1
Default output format [None]: json
```

Next configure the plugin for an operation and its API Gateway invocation URL:

```shell
$ aws configure set dynamodb.update-table https://m303r7o808.execute-api.us-east-1.amazonaws.com/Prod/update-table
```

<details>
<summary>You can review or manually configure `$HOME/.aws/config`...</summary>

```conf
[plugins]
execute-api = awscli_plugin_execute_api

[profile myprofile]
region = us-east-1
output = json
dynamodb =
    update-table = https://m303r7o808.execute-api.us-east-1.amazonaws.com/Prod/update-table
```
</details>

### Run an operation

Now run a command:

```shell
$ aws dynamodb update-table --table-name $TABLE_NAME --sse-specification Enabled=false
An error occurred (ValidationException) when calling the UpdateTable operation: Modifying SSESpecification is not allowed
```

<details>
<summary>You can use the `--debug` flag to verify the endpoint...</summary>

```shell
$ aws dynamodb update-table --debug --table-name $TABLE_NAME
Plugin awscli_plugin_execute_api: Config [myprofile] dynamodb.update-table => URL https://m303r7o808.execute-api.us-east-1.amazonaws.com/Prod/update-table
Plugin awscli_plugin_execute_api: renamed X-Amz-Target DynamoDB_20120810.UpdateTable

$ aws dynamodb describe-table --debug --table-name $TABLE_NAME
Plugin awscli_plugin_execute_api: Config [myprofile] dynamodb.describe-table not found
```
</details>

## Troubleshooting

### IAM

The CLI user needs [API execution permissions](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-iam-policy-examples-for-api-execution.html):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "execute-api:Invoke"
            ],
            "Resource": [
                "arn:aws:execute-api:us-east-1:303718836660:m303r7o808/*/POST/update-table"
            ]
        }
    ]
}
```

### Lambda

The CLI operation is in the `X-Target` header, since `X-Amz-Target` 

## Credits

- https://github.com/wbingli/awscli-plugin-endpoint