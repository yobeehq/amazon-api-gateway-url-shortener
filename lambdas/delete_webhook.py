import os
import json
import requests
import cfnresponse


def handler(event, context):
    try:
        if event['RequestType'] == 'Delete':
            token = os.environ['GITHUB_TOKEN']
            repo = event['ResourceProperties']['Repository']
            headers = {'Authorization': f'token {token}'}
            response = requests.get(f'https://api.github.com/repos/{repo}/hooks', headers=headers)
            hooks = json.loads(response.text)
            for hook in hooks:
                if 'config' in hook and 'url' in hook['config'] and 'amazonaws.com' in hook['config']['url']:
                    requests.delete(f"https://api.github.com/repos/{repo}/hooks/{hook['id']}", headers=headers)
            cfnresponse.send(event, context, cfnresponse.SUCCESS,
                             {'Status': 'SUCCESS', 'PhysicalResourceId': 'DeleteWebhookResource'})
        else:
            cfnresponse.send(event, context, cfnresponse.SUCCESS,
                             {'Status': 'SUCCESS', 'PhysicalResourceId': 'DeleteWebhookResource'})
    except Exception as e:
        cfnresponse.send(event, context, cfnresponse.FAILED, {'Status': 'FAILED', 'Reason': str(e)})
