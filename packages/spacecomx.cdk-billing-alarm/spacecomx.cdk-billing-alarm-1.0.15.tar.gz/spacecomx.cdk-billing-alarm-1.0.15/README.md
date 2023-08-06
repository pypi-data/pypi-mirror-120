[![npm version](https://badge.fury.io/js/%40spacecomx%2Fcdk-billing-alarm.svg)](https://badge.fury.io/js/%40spacecomx%2Fcdk-billing-alarm)
[![PyPI version](https://badge.fury.io/py/spacecomx.cdk-billing-alarm.svg)](https://badge.fury.io/py/spacecomx.cdk-billing-alarm)

# @spacecomx/cdk-billing-alarm

CDK construct to monitor estimated billing charges with alerts and notifications. It sets up an estimated monthly billing alarm associated with an email address endpoint. It then subscribes an email endpoint to an SNS Topic or an existing SNS Topic Arn.

The construct can be used to implement multiple customizable billing alarms for master/payer accounts e.g (AWS Organization). For customizable multi-account billing alarm requirements, see [@spacecomx/cdk-organization-billing-alarm](https://github.com/spacecomx/cdk-organization-billing-alarm)

## Features

Some features built-in:

* consolidated charge estimates of all AWS services in your AWS account.
* associate the billing alarm with an existing SNS topic Arn in your AWS account.
* consolidated charges for a specific AWS service used by your AWS account e.g. Amazon DynamoDB.
* consolidated charges for all linked accounts within the master/payer account e.g. AWS Organization.
* consolidated charges for linked account within a master/payer account.
* consolidated charges for linked account and AWS service within the master/payer account.

## Prerequisites

> :warning: Before you can create a billing alarm, you must enable billing alerts in your account, or the master/payer account if you are using consolidated billing. For more information, see [Enabling Billing Alerts](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html#turning_on_billing_metrics).

## Installation

TypeScript/JavaScript:

```bash
npm i @spacecomx/cdk-billing-alarm
```

or:

```bash
yarn add @spacecomx/cdk-billing-alarm
```

Python:

```bash
pip install spacecomx.cdk-billing-alarm
```

## Example: Create a billing alarm in your AWS account

This type of billing alarm configuration will provide estimated charges for every AWS Service that you use, in addition to the estimated overall total of your AWS charges within your AWS account. For more advanced examples and custom implementations, see [**documentation**](https://github.com/spacecomx/cdk-billing-alarm/blob/main/docs/DOCUMENTATION.md).

> :small_orange_diamond: The `emailAddress` is an endpoint that subscribes to a SNS topic. The `thresholdAmount` is the amount in USD, that will trigger the alarm when AWS charges exceed the threshold.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Stack, StackProps
from spacecomx.cdk_billing_alarm import BillingAlarm, BillingAlarmProps

class BillingAlarmStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        options = {
            "topic_configuration": {
                "email_address": ["john@example.org"]
            },
            "alarm_configuration": {
                "alarm_description": "Consolidated Billing Alarm - All AWS Services",
                "threshold_amount": 150
            }
        }

        BillingAlarm(self, "BillingAlarm", options)
```

## Documentation

For more advanced examples and custom implementations, see [documentation](https://github.com/spacecomx/cdk-billing-alarm/blob/main/docs/DOCUMENTATION.md)

## API Documentation

For more detail, see [API documentation](https://github.com/spacecomx/cdk-billing-alarm/blob/main/API.md)

## Contributions

Contributions of all kinds are welcome! Check out our [contributor's guide](https://github.com/spacecomx/cdk-billing-alarm/blob/main/CONTRIBUTING.md) and our [code of conduct](https://github.com/spacecomx/cdk-billing-alarm/blob/main/CODE_OF_CONDUCT.md)

## Credits

* [Wayne Gibson](https://github.com/waynegibson)

## Alternatives

* [@spacecomx/cdk-organization-billing-alarm](https://github.com/spacecomx/cdk-organization-billing-alarm#readme) - used for multi-account AWS Organization billing alarm requirements.
* [aws-cdk-billing-alarm](https://github.com/alvyn279/aws-cdk-billing-alarm)

## License

@spacecomx/cdk-billing-alarm is distributed under the [MIT](https://github.com/spacecomx/cdk-billing-alarm/blob/main/LICENSE) license.
