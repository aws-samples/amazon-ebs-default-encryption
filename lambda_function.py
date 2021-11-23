import json
import logging
import botocore
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sts= boto3.client('sts')

# Function to switch role on the member account
def switch_role(account_id, iam_role):
    role = sts.assume_role(
        RoleArn=f'arn:aws:iam::{account_id}:role/{iam_role}',
        RoleSessionName='Lambda_default_ebs_encryption_set'
        )
    return role['Credentials']


# Function to fetch all aws regions or only the required one
def set_regions(regions,credentials):
    if regions == 'all':
        ec2 = boto3.client(
        'ec2',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
        )
        regions_list = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    else:
        regions_list = regions.lower().strip().split(',')
    return regions_list


# Enabled default ebs encryption per region on the member account
def apply_default_ebs_encryption(credentials, regions_list):
    enabled_regions = []
    disabled_regions = []
    invalid_regions = []
    for region in regions_list:
        ec2 = boto3.client(
            'ec2',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
            region_name= region
        )
        try:
            response = ec2.enable_ebs_encryption_by_default()
            if response['EbsEncryptionByDefault'] is True:
                enabled_regions.append(region)
            elif response['EbsEncryptionByDefault'] is False:
                disabled_regions.append(region)
        except botocore.exceptions.EndpointConnectionError as error:
            logger.error(error)
            invalid_regions.append(region)

    return {
            'EBS_ENCRYPTION_ENABLED_FOR_REGIONS': enabled_regions,
            'EBS_ENCRYPTION_DISABLED_FOR_REGIONS': disabled_regions,
            'INVALID_REGIONS': invalid_regions
        }

#Main handler
def lambda_handler(event, context):
    account_id = event['accountId']
    regions = event['regions'].lower()
    iam_role = event['iamRole']
    try:
        credentials = switch_role(account_id,iam_role)
    except botocore.exceptions.ClientError as error:
        logger.error(error)
        return {
            'statusCode': 500,
            'body': format(error)
        }
    regions_list = set_regions(regions,credentials)
    default_ebs_encryption = apply_default_ebs_encryption(credentials, regions_list)
    return {
        'statusCode': 200,
        'body': json.dumps(default_ebs_encryption)
    }
