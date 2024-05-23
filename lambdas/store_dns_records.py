# FILE: store_dns_records.py
import os
import boto3
import requests
import logging
import cfnresponse

# Set up logging
logging.basicConfig(level=logging.INFO)

def lambda_handler(event, context):
    try:
        logging.info(f"Received event: {event}")

        # Get the Cloudflare API token and zone ID from environment variables
        cloudflare_api_token = os.getenv('CFLARE_API_TOKEN')
        zone_id = event['ResourceProperties']['ZoneId']

        # Get the certificate ARN from the event
        certificate_arn = event['ResourceProperties']['CertificateArn']

        # Use the AWS SDK to get the certificate details
        client = boto3.client('acm')
        response = client.describe_certificate(CertificateArn=certificate_arn)
        domain_name = response['Certificate']['DomainName']

        # Get the DNS records from the certificate details
        dns_records = response['Certificate']['DomainValidationOptions']

        # Prepare the headers for the Cloudflare API request
        headers = {
            "Authorization": f"Bearer {cloudflare_api_token}",
            "Content-Type": "application/json"
        }

        # Check if the event is a delete event
        if event['RequestType'] == 'Delete':
            # Loop through the DNS records and delete them from Cloudflare
            for record in dns_records:
                # Get the record ID
                record_id = record['ResourceRecord']['RecordId']

                # Log the DNS record data
                logging.info(f"Deleting DNS record: {record_id}")

                # Make the API request to Cloudflare
                response = requests.delete(
                    f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
                    headers=headers
                )

                # Log the response
                logging.info(f"Response: {response.json()}")

        else:
            # Loop through the DNS records and add them to Cloudflare
            for record in dns_records:
                # Prepare the data for the Cloudflare API request
                record_data = {
                    "type": record['ResourceRecord']['Type'],
                    "name": record['ResourceRecord']['Name'],
                    "content": record['ResourceRecord']['Value'],
                    "ttl": 120,
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

                # Log the response
                logging.info(f"Response: {response.json()}")

        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})

    except Exception as e:
        logging.error(f"Exception: {e}")
        cfnresponse.send(event, context, cfnresponse.FAILED, {})