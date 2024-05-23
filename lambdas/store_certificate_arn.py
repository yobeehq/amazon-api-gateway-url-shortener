import boto3
import cfnresponse
import os
import logging

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info('Event structure: %s', event)

    ssm = boto3.client('ssm', region_name=os.environ['REGION'])
    try:
        if event['RequestType'] == 'Delete':
            try:
                ssm.delete_parameter(
                    Name='/config/certificate/BackendCertificateArn'
                )
            except ssm.exceptions.ParameterNotFound:
                logger.info('BackendCertificateArn parameter not found, skipping deletion.')
            try:
                ssm.delete_parameter(
                    Name='/config/certificate/FrontendCertificateArn'
                )
            except ssm.exceptions.ParameterNotFound:
                logger.info('FrontendCertificateArn parameter not found, skipping deletion.')
        else:
            ssm.put_parameter(
                Name='/config/certificate/BackendCertificateArn',
                Type='String',
                Value=event['ResourceProperties']['BackendCertificateArn'],
                Overwrite=True
            )
            ssm.put_parameter(
                Name='/config/certificate/FrontendCertificateArn',
                Type='String',
                Value=event['ResourceProperties']['FrontendCertificateArn'],
                Overwrite=True
            )
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    except Exception as e:
        logger.error('Error: %s', e)
        cfnresponse.send(event, context, cfnresponse.FAILED, {})