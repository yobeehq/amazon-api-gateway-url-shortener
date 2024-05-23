import boto3
import cfnresponse
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def handler(event, context):
    try:
        client = boto3.client('amplify')
        appId = os.environ['AMPLIFY_APP_ID'].split('/')[-1]
        branchName = os.environ['AMPLIFY_BRANCH_NAME']

        logging.info(f'App ID: {appId}, Branch Name: {branchName}')

        if event['RequestType'] in ['Create', 'Update']:
            try:
                responseData = client.start_job(
                    appId=appId,
                    branchName=branchName,
                    jobType='RELEASE',
                )
                cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData)
                logging.info(f'Successfully started job: {responseData}')
            except Exception as e:
                cfnresponse.send(event, context, cfnresponse.FAILED, {}, str(e))
                logging.error(f'Failed to start job: {str(e)}')
        else:
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
            logging.info('RequestType not Create or Update, no action taken.')
    except Exception as e:
        cfnresponse.send(event, context, cfnresponse.FAILED, {}, str(e))
        logging.error(f'Error in handler: {str(e)}')