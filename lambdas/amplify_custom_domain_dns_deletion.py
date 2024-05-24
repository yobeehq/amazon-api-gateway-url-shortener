import boto3
import logging
import os
import requests
import cfnresponse

def handler(event, context):
    try:
        if event['RequestType'] == 'Delete':
            logging.info(f"Received delete event: {event}")

            # Get the Cloudflare API token and zone ID from environment variables
            cloudflare_api_token = os.getenv('CFLARE_API_TOKEN')
            zone_id = os.getenv('CFLARE_ZONE_ID')

            # Prepare the headers for the Cloudflare API request
            headers = {
                "Authorization": f"Bearer {cloudflare_api_token}",
                "Content-Type": "application/json"
            }

            # Get the Amplify App ID from the environment variables
            app_id = os.getenv('AMPLIFY_APP_ID')

            # Create a client for the Amplify service
            amplify = boto3.client('amplify')

            # Get all domain associations
            domain_associations = amplify.list_domain_associations(appId=app_id)['domainAssociations']

            for domain_association in domain_associations:
                # Get the DNS records from the domain association
                dns_records = domain_association['dnsRecord']

                for record in dns_records:
                    # Make the API request to Cloudflare
                    response = requests.delete(
                        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record['id']}",
                        headers=headers
                    )

                    response_data = response.json()
                    if not response_data['success']:
                        # If the request was not successful, raise an exception with the error message
                        raise Exception(f"Cloudflare API request failed: {response_data['errors']}")
                    else:
                        logging.info(f"DNS Record Deleted: {response_data}")

        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        cfnresponse.send(event, context, cfnresponse.FAILED, {})