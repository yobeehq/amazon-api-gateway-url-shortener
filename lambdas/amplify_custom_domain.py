import boto3
import cfnresponse
import logging
import os

def handler(event, context):

    amplify_role_arn = os.environ['AMPLIFY_ROLE_ARN']
    print('AMPLIFY_ROLE_ARN -', amplify_role_arn)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info('Event structure: %s', event)
    client = boto3.client('amplify')
    try:
        if event['RequestType'] == 'Delete':
            try:
                client.delete_domain_association(
                    appId=event['ResourceProperties']['AppId'],
                    domainName=event['ResourceProperties']['DomainName']
                )
            except client.exceptions.NotFoundException:
                logger.info('Domain association not found, skipping deletion.')
        else:
            client.create_domain_association(
                appId=event['ResourceProperties']['AppId'],
                domainName=event['ResourceProperties']['DomainName'],
                enableAutoSubDomain=True,
                autoSubDomainIAMRole=os.environ['AMPLIFY_ROLE_ARN'],
                subDomainSettings=[{
                    'prefix': 'www',
                    'branchName': 'master'
                }],
                autoSubDomainCreationPatterns=['*'],
            )
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    except Exception as e:
        logger.error('Error: %s', e)
        cfnresponse.send(event, context, cfnresponse.FAILED, {})