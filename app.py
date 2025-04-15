import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from nsfw_model.nsfw_detector import predict
import numpy as np

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jiff'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load NSFW model
model = predict.load_model('nsfw_model/nsfw_mobilenet2.224x224.h5')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_nsfw(results):
    nsfw_categories = ['porn', 'hentai', 'sexy']
    nsfw_threshold = 0.5
    for category in nsfw_categories:
        if results.get(category, 0) > nsfw_threshold:
            return True
    return False

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            result = predict.classify(model, filepath)
            os.remove(filepath)

            image_result = list(result.values())[0]
            highest_category = max(image_result, key=image_result.get)
            highest_percentage = f"{image_result[highest_category]*100:.2f}%"
            nsfw_status = "It is a NSFW image" if is_nsfw(image_result) else "It is not a NSFW image"

            return jsonify({
                'highest_category': highest_category,
                'highest_percentage': highest_percentage,
                'nsfw_status': nsfw_status,
                'categories': image_result
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
