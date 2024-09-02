import requests
import json
import os
from dotenv import load_dotenv
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("metadata.log"), logging.StreamHandler()]
)

# setting up logging
logger = logging.getLogger(__name__)

# load environmental variable
load_dotenv()
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY")


def pin_img_to_pinata(filepath):
    logger.info("starting pining image to pinata ...")
    
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        'pinata_api_key': PINATA_API_KEY,
        'pinata_secret_api_key': PINATA_SECRET_API_KEY,
    }

    # Use 'with' to handle file opening and closing automatically
    with open(filepath, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, files=files, headers=headers)

    # Handle the response
    if response.status_code == 200:
        cid = response.json()['IpfsHash']
        logger.info(f"Pinned to IPFS with CID: {cid}")
        return cid
    else:
        raise Exception(f"Failed to pin file: {response.text}")


def pin_metadata_to_pinata(metadata):
    logger.info("starting pining metadata to pinata ...")
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        'pinata_api_key': PINATA_API_KEY,
        'pinata_secret_api_key': PINATA_SECRET_API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(metadata), headers=headers)
    if response.status_code == 200:
        return response.json()['IpfsHash']  # CID for the metadata
    else:
        raise Exception(f"Failed to pin metadata: {response.text}")

# image_cid
# image_cid = 'QmdzW2v2VgZaNgeAYt9sRJjnfDLb1CPUbvwDYoT3Vt2qzs'
# # Metadata structure following ERC-721 standard
# metadata = {
#     "name": "My NFT",
#     "description": "This is my first NFT minted using IPFS and Pinata!",
#     "image": f"ipfs://{image_cid}",  # Use the CID of the uploaded image
#     "attributes": [
#         {"trait_type": "Background", "value": "Blue"},
#         {"trait_type": "Eyes", "value": "Green"}
#     ]
# }
#
#
# # Pin metadata JSON
# metadata_cid = pin_metadata_to_pinata(metadata)
# logger.info(f"Metadata pinned to IPFS with CID: {metadata_cid}")

# Example usage
# cid = pin_file_to_pinata("GNeWNfoWoAAbdW-.jpg")
# logger.info(f"Pinned to IPFS with CID: {cid}")
