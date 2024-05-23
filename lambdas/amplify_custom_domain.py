import boto3
import cfnresponse
import logging
import os
import json

def handler(event, context):

    try:
        amplify_role_arn = os.environ['AMPLIFY_ROLE_ARN']
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.info('Event structure: %s', event)
        client = boto3.client('amplify')
        ssm = boto3.client('ssm')

        if event['RequestType'] == 'Delete':
            try:
                client.delete_domain_association(
                    appId=event['ResourceProperties']['AppId'],
                    domainName=event['ResourceProperties']['DomainName']
                )
            except client.exceptions.NotFoundException:
                logger.info('Domain association not found, skipping deletion.')
        else:
            # Get the certificate ARN from the Parameter Store
            certificate_arn = ssm.get_parameter(
                Name='/config/certificate/FrontendCertificateArn',
                WithDecryption=True
            )['Parameter']['Value']

            client.create_domain_association(
                appId=event['ResourceProperties']['AppId'],
                domainName=event['ResourceProperties']['DomainName'],
                enableAutoSubDomain=True,
                autoSubDomainIAMRole=os.environ['AMPLIFY_ROLE_ARN'],
                subDomainSettings=[{
                    'prefix': 'www',
                    'branchName': os.environ['AMPLIFY_BRANCH_NAME']
                }, {
                    'prefix': '',
                    'branchName': os.environ['AMPLIFY_BRANCH_NAME']
                }],
                autoSubDomainCreationPatterns=['*'],
                certificateSettings={
                    'type': 'CUSTOM',
                    'customCertificateArn': certificate_arn
                }
            )

            lambda_client = boto3.client('lambda')
            lambda_client.invoke(
                FunctionName=os.environ['DNS_UPDATER_FUNCTION_ARN'],
                InvocationType='Event',
                Payload=json.dumps({
                    'ResourceProperties': {
                        'DnsRecords': response['domainAssociation']['dnsRecord']
                    }
                })
            )

        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    except Exception as e:
        logger.error('Error: %s', e)
        cfnresponse.send(event, context, cfnresponse.FAILED, {})