from urllib.parse import quote
from flask import Blueprint, jsonify, request, send_file
import os

class FileController:
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

    def __init__(self, app, upload_folder='static/upload'):
        self.app = app 
        self.upload_folder = os.path.join(app.root_path, upload_folder)
        self.blueprint = Blueprint('file', __name__)

        @self.blueprint.route('/upload', methods=['POST'])
        def upload_file():
            if 'file' not in request.files:
                return jsonify({'error': 'No file part'}), 400

            file = request.files['file']

            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400
            
            # Validate file extension
            if not FileController.allowed_file(file.filename):
                return jsonify({'error': 'Invalid file format. Allowed formats: pdf, jpg, jpeg, png'}), 400

            # Ensure the upload folder exists
            os.makedirs(self.upload_folder, exist_ok=True)

            # Modify filename to lowercase and replace spaces with dash
            filename = file.filename.lower().replace(' ', '-')
            
            # Save the file to the specified upload folder
            file_path = os.path.join(self.upload_folder, filename)
            file.save(file_path)

            # Create URL or path for the file
            file_url = self.app.static_url_path + '/upload/' + quote(filename)

            # Provide a preview response with file URL
            preview_data = {
                'filename': filename,
                'filetype': file.content_type,
                'file_url': file_url
            }

            return jsonify(preview_data)

        @self.blueprint.route('/upload/<filename>', methods=['GET'])
        def get_image(filename):
            image_path = os.path.join(self.upload_folder, filename)
            if os.path.exists(image_path):
                return send_file(image_path)
            else:
                return jsonify({'error': 'Image not found'}), 404
            
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in FileController.ALLOWED_EXTENSIONS


