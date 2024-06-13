import logging
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import Worker_completed as worker  # Import the worker module

# Initialize Flask app and CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.logger.setLevel(logging.DEBUG)  # Set logging to debug level for more detailed output

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define the route for the index page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')  # Render the index.html template

# Define the route for processing messages
@app.route('/process-message', methods=['POST'])
def process_message_route():
    user_message = request.json.get('userMessage', '')  # Extract the user's message from the request
    app.logger.debug(f"user_message: {user_message}")

    if not user_message:
        return jsonify({"botResponse": "Please provide a message to process."}), 400

    try:
        bot_response = worker.process_prompt(user_message)  # Process the user's message using the worker module
        return jsonify({"botResponse": bot_response}), 200
    except Exception as e:
        app.logger.error(f"Error processing message: {e}")
        return jsonify({"botResponse": "There was an error processing your message."}), 500

# Define the route for processing documents
@app.route('/process-document', methods=['POST'])
def process_document_route():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({
            "botResponse": "It seems like the file was not uploaded correctly, can you try again. "
                           "If the problem persists, try using a different file"
        }), 400

    file = request.files['file']  # Extract the uploaded file from the request

    if file.filename == '':
        return jsonify({"botResponse": "No file selected. Please try again."}), 400

    # Define the path where the file will be saved in the uploads directory
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

    try:
        app.logger.debug(f"Saving file to {file_path}")
        file.save(file_path)  # Save the file
        app.logger.debug(f"File saved successfully to {file_path}")

        worker.process_document(file_path)  # Process the document using the worker module

        return jsonify({
            "botResponse": "Thank you for providing your PDF document. I have analyzed it, so now you can ask me any "
                           "questions regarding it!"
        }), 200
    except Exception as e:
        app.logger.error(f"Error saving or processing document: {e}")
        return jsonify({"botResponse": "There was an error processing your document."}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=8000, host='0.0.0.0')
