import logging
import os

import requests

import cfnresponse
from models.DNSRecord import DNSRecord


def main(event, context):
    logging.info(f"Received event: {event}")

    # Get the Cloudflare API token and zone ID from environment variables
    cloudflare_api_token = os.getenv('CFLARE_API_TOKEN')
    zone_id = os.getenv('CFLARE_ZONE_ID')

    # Prepare the headers for the Cloudflare API request
    headers = {
        "Authorization": f"Bearer {cloudflare_api_token}",
        "Content-Type": "application/json"
    }

    dns_records = DNSRecord.from_json_list(event['ResourceProperties']['DnsRecords'])

    for record in dns_records:
        # Prepare the data for the Cloudflare API request
        record_data = {
            "type": record.type,
            "name": record.name,
            "content": record.content,
            "ttl": 1,
            "proxied": False
        }

        # Log the DNS record data
        logging.info(f"Adding DNS record: {record_data}")

        # Make the API request to Cloudflare
        response = requests.post(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
            headers=headers,
            json=record_data
        )

        response_data = response.json()
        if not response_data['success']:
            # If the request was not successful, raise an exception with the error message
            raise Exception(f"Cloudflare API request failed: {response_data['errors']}")
        else:
            logging.info(f"DNS Added: {response_data}")


def handler(event, context):
    try:
        main(event, context)
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        cfnresponse.send(event, context, cfnresponse.FAILED, {})
