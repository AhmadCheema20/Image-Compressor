from flask import Flask, request, send_file, jsonify, render_template
from PIL import Image
import io
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')  # this will render templates/index.html

@app.route('/compress', methods=['POST'])
def compress_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image part"}), 400

    file = request.files['image']
    quality = int(request.form.get('quality', 60))
    output_format = request.form.get('format', 'jpeg').lower()

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        img = Image.open(file.stream).convert("RGB")
        buffer = io.BytesIO()

        if output_format == 'png':
            img.save(buffer, format='PNG', optimize=True)
        elif output_format == 'webp':
            img.save(buffer, format='WEBP', quality=quality, method=6)
        else:  # default to jpeg
            img.save(buffer, format='JPEG', quality=quality, optimize=True)

        buffer.seek(0)
        return send_file(
            buffer,
            mimetype=f'image/{output_format}',
            as_attachment=True,
            download_name=secure_filename(file.filename.rsplit('.', 1)[0]) + f'_compressed.{output_format}'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
