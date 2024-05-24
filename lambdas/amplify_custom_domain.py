import json
import logging
import os
import time
from typing import List

import boto3

import cfnresponse
from models.DNSRecord import DNSRecord

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def split_dns_record(dns_record, baseDomain) -> DNSRecord:
    parts = dns_record.split(' ', 2)
    if len(parts) != 3:
        raise ValueError('Invalid DNS record format')
    return DNSRecord(parts[1], baseDomain if parts[0] == '' else f'{parts[0]}.{baseDomain}', parts[2])


def get_dns_records(app_id, domain_name) -> List[DNSRecord]:
    client = boto3.client('amplify')
    while True:
        response = client.get_domain_association(
            appId=app_id,
            domainName=domain_name
        )
        domain_status = response['domainAssociation']['domainStatus']

        if domain_status == 'FAILED':
            raise Exception('Domain association creation failed')

        sub_domains = response['domainAssociation']['subDomains']
        base_domain = response['domainAssociation']['domainName']
        if all('pending' not in sub_domain['dnsRecord'] for sub_domain in sub_domains):
            dns_records = [split_dns_record(sub_domain['dnsRecord'], base_domain) for sub_domain in sub_domains]
            return dns_records

        logger.info('Domain status: %s', domain_status)
        logger.info('Domain association: %s', response['domainAssociation'])

        time.sleep(2)


def handler(event, context):
    try:
        amplify_role_arn = os.environ['AMPLIFY_ROLE_ARN']

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

            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        else:
            # Get the certificate ARN from the Parameter Store
            certificate_arn = ssm.get_parameter(
                Name='/config/certificate/FrontendCertificateArn',
                WithDecryption=True
            )['Parameter']['Value']

            response = client.create_domain_association(
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

            logging.info('Domain association created: %s', response)
            dns_records = get_dns_records(event['ResourceProperties']['AppId'],
                                          event['ResourceProperties']['DomainName'])

            lambda_client = boto3.client('lambda')
            lambda_client.invoke(
                FunctionName=os.environ['DNS_UPDATER_FUNCTION_ARN'],
                InvocationType='Event',
                Payload=json.dumps({
                    'ResourceProperties': {
                        'DnsRecords': DNSRecord.to_json_list(dns_records)
                    },
                    'ResponseURL': event['ResponseURL'],
                    'StackId': event['StackId'],
                    'RequestId': event['RequestId'],
                    'LogicalResourceId': event['LogicalResourceId'],
                })
            )

            logger.info('Lambda for DNS Update For Cloudflare Triggered with DNS records: %s',
                        DNSRecord.to_json_list(dns_records))

    except Exception as e:
        logger.error('Error: %s', e)
        cfnresponse.send(event, context, cfnresponse.FAILED, {})
