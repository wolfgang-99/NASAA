from flask import Flask, request, jsonify, session
import os
from pinata import pin_img_to_pinata
from datetime import timedelta
from database import *
from server import *
import logging
from flask_cors import CORS


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("main.log"), logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
app.permanent_session_lifetime = timedelta(hours=3)
app.secret_key = os.getenv("secret_key")

# Ensure the temp directory exists
os.makedirs('temp', exist_ok=True)


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the NASAA API of art"}), 200


@app.route('/api/upload_img', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save file temporarily to check its type
    file_path = f"temp/{file.filename}"
    try:
        # Save the file to disk
        with open(file_path, 'wb') as f:
            f.write(file.read())

        # Validate if the uploaded file is an image
        if not is_image_file(file_path):
            os.remove(file_path)
            return jsonify({'error': 'The uploaded file is not a valid image'}), 400

        # File has been validated; now upload using its path
        try:
            cid = pin_img_to_pinata(file_path)  # Pass the file path

            # Store cid in the session
            session['img_cid'] = cid

        except Exception as e:
            return jsonify({'error': str(e)}), 500

        finally:
            # Ensure the file is removed even if an error occurs
            if os.path.exists(file_path):
                os.remove(file_path)
        return jsonify({'message': 'image uploaded successfully', 'result': cid}), 200

    except Exception as e:
        # Handle any errors, ensuring file cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload_artData', methods=['POST'])
def upload_art_info():
    try:
        art_name = request.form['art_name']
        art_region = request.form['art_region']
        art_info = request.form['art_info']
        stated_amount = request.form['stated_amount']

        if "img_cid" in session:
            # Retrieve 'cid' from the session
            img_cid = session.get('img_cid', None)

            recorded_data = create_art_data(img_cid, art_name, art_info, art_region, stated_amount)

            if recorded_data:
                return jsonify({'message': 'Art data has been recorded to database'}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/upload_crowdfundingData', methods=['POST'])
def upload_crowdfunding_info():
    try:
        crowdfunding_name = request.form['crowdfunding_name']
        crowdfunding_region = request.form['crowdfunding_region']
        crowdfunding_info = request.form['crowdfunding_info']
        stated_amount = request.form['stated_amount']

        recorded_data = create_crowdfunding_data(crowdfunding_name, crowdfunding_info, crowdfunding_region,
                                                 stated_amount)

        if recorded_data:
            return jsonify({'message': 'crowdfunding data has been recorded to database'}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/art_documents', methods=['GET'])
def get_all_art_documents():
    try:
        documents = get_all_art_doc()
        if documents:

            return jsonify(documents), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/crowdfunding_documents', methods=['GET'])
def get_all_crowdfunding_documents():
    try:
        documents = get_all_crowdfunding_doc()
        if documents:

            return jsonify(documents), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/calculate_percentage', methods=['GET'])
def calculate_percentage():

    try:
        # Get input parameters from the query string
        current_amount = request.args.get('current_amount', type=float)
        stated_amount = request.args.get('stated_amount', type=float)

        # Validate inputs
        if current_amount is None or stated_amount is None:
            return jsonify({"error": "Missing required parameters 'current_amount' or 'stated_amount'"}), 400

        # Calculate the percentage
        result = calculate_percentage(current_amount, stated_amount)

        # Return the result as JSON
        return jsonify({"percentage": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
