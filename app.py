import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from nsfw_model.nsfw_detector import predict
import numpy as np

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','jiff'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load NSFW model
model = predict.load_model('nsfw_model/nsfw_mobilenet2.224x224.h5')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_nsfw(results):
    # Define NSFW thresholds 
    nsfw_categories = ['porn', 'hentai', 'sexy']
    nsfw_threshold = 0.5  # 50% confidence

    for category in nsfw_categories:
        if results[category] > nsfw_threshold:
            return True
    return False

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        
        file = request.files['file']
        
        # If no file is selected
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        
        # If file is allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Predict NSFW content
            try:
                result = predict.classify(model, filepath)
                # Remove the file after processing
                os.remove(filepath)
                
                # Extract the first (and only) result
                image_result = list(result.values())[0]
                
                # Find the highest rated category
                highest_category = max(image_result, key=image_result.get)
                highest_percentage = f"{image_result[highest_category]*100:.2f}%"
                
                # Determine if image is NSFW
                nsfw_status = "It is a NSFW image" if is_nsfw(image_result) else "It is not a NSFW image"
                
                return jsonify({
                    'highest_category': highest_category,
                    'highest_percentage': highest_percentage,
                    'nsfw_status': nsfw_status,
                    'categories': image_result
                })
            
            except Exception as e:
                return jsonify({'error': str(e)})
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)