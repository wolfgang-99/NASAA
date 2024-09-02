import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
import logging


# setting up logging
logger = logging.getLogger(__name__)

# load environmental variable
load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")

# Connect to mongodb
client = MongoClient(MONGODB_URL)
db = client['NASSA']
logger.info("connected to mongodb")


def create_art_data(img_cid, art_name, art_info, art_region, stated_amount):
    try:
        collection = db['art_details']

        # Check if the art info already exists in the database
        existing_art = collection.find_one({'cid': img_cid})
        if existing_art:
            logger.info("Art data already exists. Please choose a different art data.")
            return False

        remaining_percentage = 0
        current_amount = 0
        # If the username doesn't exist, insert the new user
        submission = {'cid': img_cid,
                      'name_of_art': art_name,
                      'art_region': art_region,
                      'art_info': art_info,
                      'current_amount': float(current_amount),
                      'stated_amount': float(stated_amount),
                      'remaining_percentage': float(remaining_percentage)
                      }
        collection.insert_one(submission)
        logger.info(f" Art data with cid: {img_cid} has been recorded")
        return True
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


def create_crowdfunding_data(crowdfunding_name, crowdfunding_info, crowdfunding_region, stated_amount):
    try:
        collection = db['crowdfunding_details']

        remaining_percentage = 0
        current_amount = 0

        # If the username doesn't exist, insert the new user
        submission = {
                      'crowdfunding_name': crowdfunding_name,
                      'crowdfunding_region': crowdfunding_region,
                      'crowdfunding_info': crowdfunding_info,
                    'current_amount': float(current_amount),
                    'stated_amount': float(stated_amount),
                    'remaining_percentage': float(remaining_percentage)
                      }
        collection.insert_one(submission)
        logger.info(f"Data has been recorded")
        return True
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


def get_all_art_doc():
    try:
        collection = db['art_details']

        # Fetch all documents in the collection
        documents = list(collection.find({}))  # Convert the cursor to a list

        # Convert ObjectId to string and jsonify documents
        for doc in documents:
            doc['_id'] = str(doc['_id'])

        logger.info(f"all art documents have been reterived")
        return documents

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


def get_all_crowdfunding_doc():
    try:
        collection = db['crowdfunding_details']

        # Fetch all documents in the collection
        documents = list(collection.find({}))  # Convert the cursor to a list

        # Convert ObjectId to string and jsonify documents
        for doc in documents:
            doc['_id'] = str(doc['_id'])

        logger.info(f"all crowdfunding documents have been reterived")
        return documents

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

