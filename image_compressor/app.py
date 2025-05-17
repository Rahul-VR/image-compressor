from flask import Flask, request, jsonify, render_template
from PIL import Image
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route('/')
def form():
    return render_template('upload_form.html')
@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        
        image = Image.open(file)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        filename = file.filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        image.save(save_path, "JPEG", quality=80, optimize=True)

        return jsonify({'message': 'Image uploaded and compressed successfully', 'filename': filename}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
