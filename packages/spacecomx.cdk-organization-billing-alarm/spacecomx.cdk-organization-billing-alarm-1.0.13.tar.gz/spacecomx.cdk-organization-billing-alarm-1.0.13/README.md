[![npm version](https://badge.fury.io/js/%40spacecomx%2Fcdk-organization-billing-alarm.svg)](https://badge.fury.io/js/%40spacecomx%2Fcdk-organization-billing-alarm)
[![PyPI version](https://badge.fury.io/py/spacecomx.cdk-organization-billing-alarm.svg)](https://badge.fury.io/py/spacecomx.cdk-organization-billing-alarm)

# @spacecomx/cdk-organization-billing-alarm

Multi-account CDK construct to monitor estimated billing charges with alerts and notifications for a AWS Organization. It gives you the capability to monitor specific AWS Service charges, by a linked AWS account in a master/payer account. It can create customizable billing alarms for multiple linked AWS accounts within AWS Organization. It can subscribe multiple email address endpoints to an SNS Topic created by the package or it can use an existing SNS Topic Arn within the master/payer account.

For single AWS account billing alarm requirements, see [@spacecomx/cdk-billing-alarm](https://github.com/spacecomx/cdk-billing-alarm#readme)

## Table of Contents

* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)

  * [Example 1: Create billing alarm in a master/payer account](#example_1)
  * [Example 2: Link alarm to an existing SNS Topic Arn](#example_2)
  * [Example 3: Link alarm to specific AWS Account in master/payer account](#example_3)
  * [Example 4: Updating/Removing SNS Topic email address endpoint subscription](#example_4)
* [Post Deployment](#post-deployment)
* [API Documentation](#api-documentation)

## Prerequisites

> :warning: Before you can create a billing alarm, you must enable billing alerts in your master/payer account when using consolidated billing. For more information, see [Enabling Billing Alerts](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html#turning_on_billing_metrics).

## Installation

TypeScript/JavaScript:

```bash
npm i @spacecomx/cdk-organization-billing-alarm
```

or:

```bash
yarn add @spacecomx/cdk-organization-billing-alarm
```

Python:

```bash
pip install spacecomx.cdk-organization-billing-alarm
```

## Usage

<a name="example_1"></a>

### Example 1: Create billing alarm in a master/payer account.

This type of billing alarm configuration will provide estimated charges for every AWS Service that you use, in addition to the estimated overall total of your AWS charges within your AWS master/payer account e.g (AWS Organization).

* It creates a new SNS Topic in your AWS master/payer account.
* It then subscribes the email address endpoint to the topic.
* It then creates the Cloudwach estimate billing alarm.
* It then associates the SNS topic with the newly created billing alarm.

> :small_orange_diamond: The `emailAddress` is an endpoint that subscribes to a SNS topic. The `thresholdAmount` is the amount in USD, that will trigger the alarm when AWS charges exceed the threshold.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Stack, StackProps
from spacecomx.cdk_organization_billing_alarm import MasterAccountAlarm, MasterAccountAlarmProps

class OrganizationBillingAlarmStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        config = {
            "alarm_configuration": {
                "topic_description": "Organization Billing Alarm Topic",
                "email_address": ["billing@example.org", "admin@example.org"],
                "alarm_description": "Consolidated Billing Alarm: All AWS Services",
                "threshold_amount": 140
            }
        }

        MasterAccountAlarm(self, "MasterAccountAlarm", config)
```

<a name="example_2"></a>

### Example 2: Link alarm to an existing SNS Topic Arn.

This type of billing alarm configuration simliar to [example 1](#example_1), with the exception that the billing alarm is now linked to an existing SNS Topic in the master/payer account.

* It uses an existing SNS Topic within the AWS master/payer account.
* It imports a secret by secret name that was created in master/payer account using AWS Secrets Manager e.g (prod/billing/topicArn).
* It then subscribes the email address endpoint to the retrieved SNS Topic's Arn.
* It then creates the Cloudwach estimate billing alarm.
* It then associates the SNS topic with the newly created billing alarm.

> :small_orange_diamond: The `secretName` option is required and used to retrieve the existing SNS Topic's Arn from AWS Secrets Manager. The secret name **must exist** in the same account and region as the master/payer AWS account.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Stack, StackProps
from spacecomx.cdk_organization_billing_alarm import MasterAccountAlarm, MasterAccountAlarmProps

class OrganizationBillingAlarmStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        config = {
            "secret_name": "prod/billing/topicArn", # existing sns topic arn
            "alarm_configuration": {
                "email_address": ["john@example.org"],
                "alarm_description": "Consolidated Billing Alarm: All AWS Services",
                "threshold_amount": 140
            }
        }

        MasterAccountAlarm(self, "MasterAccountAlarm", config)
```

<a name="example_3"></a>

### Example 3: Link alarm to specific AWS Account in master/payer account.

This type of billing alarm configuration provides customizable options for linked AWS accounts within the master/payer account. The packages `accountConfiguration` required option allows for multiple AWS accounts to link to a single SNS Topic using the required `secretName` option.

* It uses an existing SNS Topic's Arn within the AWS master/payer account.
* It imports a secret by secret name that was created in master/payer account using AWS Secrets Manager e.g (prod/billing/topicArn).
* It then creates the Cloudwach estimate billing alarm associated to the linked AWS account.
* It then associates the SNS topic with the newly created billing alarm.

> :small_orange_diamond: The `secretName` option is required and used to retrieve the existing SNS Topic's Arn from AWS Secrets Manager. The secret name **must exist** in the same account and region as the master/payer AWS account.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Stack, StackProps
from spacecomx.cdk_organization_billing_alarm import LinkedAccountAlarm, LinkedAccountAlarmProps

class OrganizationBillingAlarmStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        config = {
            "secret_name": "prod/billing/topicArn",
            "account_configuration": [{
                "account": "444455556666",
                "alarm_name": "Billing Alarm (Acc: 444455556666)", # named by aws-cdk (recommended)
                "alarm_description": "Billing Alarm: All AWS Services (Acc: 444455556666)",
                "threshold_amount": 50
            }
            ]
        }

        LinkedAccountAlarm(self, "LinkedAccountAlarm", config)
```

-OR-

You can manage **multiple linked AWS accounts** each with its own billing alarm configuration, with a single implementation of the `LinkedAccountAlarm` construct. The code example below uses a ***single SNS Topic*** to manage alerts and notifications for all linked accounts within the master/payer account. Each linked account can send alerts and notifications to either a single email address or multiple email addresses, subscribed to the SNS Topic within the master/payer account

> :small_orange_diamond: Should you need more that one SNS topic e.g. you want seperate out linked accounts by department or business unit, each having its own SNS Topic. One option would be to, firstly create an SNS Topic in the master/payer account for each department or business unit. Remember to create a new secret with that SNS Topic's Arn in AWS Secrets Manager. Then simply, new up `LinkedAccountAlarm` constructs that group those linked accounts by department or business unit, each with its own SNS Topic.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
config = {
    "secret_name": "prod/billing/other/topicArn", # single topic used by multiple accounts
    "account_configuration": [{
        "account": "444455556666",
        "alarm_description": "Billing Alarm: All AWS Services (Acc: 444455556666)",
        "threshold_amount": 50
    }, {
        "account": "123456789000",
        "alarm_description": "Billing Alarm: All AWS Services (Acc: 123456789000)",
        "threshold_amount": 120
    }
    ]
}
```

> :small_orange_diamond: You can also link the alarm to a specific AWS Service, per linked AWS account. Use the `awsService` option. See the code example below.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
config = {
    "secret_name": "prod/billing/topicArn",
    "account_configuration": [{
        "account": "444455556666",
        "alarm_description": "Billing Alarm: All AWS Services (Acc: 444455556666)",
        "threshold_amount": 50
    }, {
        "account": "123456789000",
        "alarm_description": "Billing Alarm: Amazon DynamoDB (Acc: 123456789000)",
        "threshold_amount": 120,
        "aws_service": "AmazonDynamoDB"
    }
    ]
}
```

> :small_orange_diamond: Should you need to remove a `awsService` subscribed to a specific linked account, simply remove the `awsService` option.

<a name="example_4"></a>

### Example 4: Updating/Removing SNS Topic email address endpoint subscription.

When would you use this option?

* When an existing SNS topic that already has an email address endpoint subscribed to it,
* or you dont require any additional email address endpoints to be added to the existing topic,
* or you want to add your own email address endpoints manually to the SNS topic (not recommended),
* or you want to remove an email address endpoints from the SNS topic created with the package,
* or you want to add or update email address endpoints for the SNS topic using the package.

> :small_orange_diamond: To manage adding and removing endpoints for the SNS topic, use the packages `emailAddress` option. You can simply set the `emailAddress: ['john@example.org']` option to `emailAddress: []`. Please note that email endpoint subscriptions created manually via AWS SNS Console **will not be removed** by the package.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
config = {
    "alarm_configuration": {
        "email_address": [], ...
    }
}
```

Adding and removing endpoints means ***you will need to again confirm the subscription*** of each email address you specified with `emailAddress` option or those added manually by you e.g AWS SNS console (not recommended). See [post deployment](#post-deployment) for details.

> :warning: Please be **cautious**. Without an endpoint been provided i.e. (email address been subscribed to the SNS topic), the billing alarm will still trigger when exceeding the alarm threshold. However you will **not recieve any email alarm notifications** via email.

## Post Deployment

Once the Billing Alarm Stack resources has been successfully created in your AWS account, you will need to confirm the subscription of each email address you specified with the `emailAddress` configuration option. Clicking on the **"Confirm Subscription"** link for that email, will automatically activate billing alarm notifications for that email address.

If you did not receive the email, you can process a **"Request Confirmation"** for the subscription from the Simple Notification Service (SNS) console within your AWS account.

> :warning: Without confirming the email subscription you will **not recieve any email alarm notifications** via email. The billing alarm will trigger when exceeding the alarm threshold, but **you will not be notified** via email.

## API Documentation

For more detail, see [API documentation](https://github.com/spacecomx/cdk-organization-billing-alarm/blob/main/API.md)

## Contributions

Contributions of all kinds are welcome! Check out our [contributor's guide](https://github.com/spacecomx/cdk-organization-billing-alarm/blob/main/CONTRIBUTING.md) and our [code of conduct](https://github.com/spacecomx/cdk-organization-billing-alarm/blob/main/CODE_OF_CONDUCT.md)

## Credits

* [Wayne Gibson](https://github.com/waynegibson)

## Alternatives

* [@spacecomx/cdk-billing-alarm](https://github.com/spacecomx/cdk-billing-alarm#readme) - used for single account billing alarm requirements and some.

## License

@spacecomx/cdk-organization-billing-alarm is distributed under the [MIT](https://github.com/spacecomx/cdk-organization-billing-alarm/blob/main/LICENSE) license.
