# Enable EBS Default Encryption - Lambda
This lambda function enables the EBS Default Encryption functionality on demand for the specified Regions on the AWS Account. To have an understanding on the
EBS Default Encryption feature, please refer to: 
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html#encryption-by-default
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html#encryption-by-default-api

The lambda function can be easily integrated with CloudWatch Events (EventBridge), Step Functions and API Gateway.


## Event Parameters
- `accountId` : 123456789012 <br />
The AWS Account number on which the feature will be enabled.
- `regions` : eu-central-1,eu-west-1,us-west-2,us-east-1,ap-east-1 or "all" <br />
The list of Regions where the feature will be enabled. By passing the value "all" it will iterate over all existing regions.
- `iamRole` : OrganizationAccountAccessRole <br />
The IAM Role that the Lambda Function will assume on the Target Account.


### Event sample
```json
{
  "accountId": "123456789012",
  "regions": "eu-central-1,eu-west-1,us-west-2,us-east-1,ap-east-1",
  "iamRole": "OrganizationAccountAccessRole"
}
``` 


## Lambda Settings
- `Memory` : 512MB
- `Timeout` : 300 seconds
- `Runtime` : Python3.8


## IAM Permissions
- `Lambda IAM Role Permission`
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        },
        {
            "Sid": "AllowAssumeRole",
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "*"
        }
    ]
}
```
- `Lambda IAM Role Permission for Target Account`
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EnableEncryption",
            "Effect": "Allow",
            "Action": [
                "ec2:GetEbsEncryptionByDefault",
                "ec2:EnableEbsEncryptionByDefault",
                "ec2:GetEbsDefaultKmsKeyId",
                "ec2:ModifyEbsDefaultKmsKeyId",
                "ec2:DescribeRegions"
            ],
            "Resource": "*"
        }
    ]
}
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.