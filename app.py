import os
import shutil
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from lab import collect_data_from_train_model, collect_data_by_train_model

app = Flask(__name__)
UPLOAD_FOLDER = 'img'
RUNS_FOLDER = 'runs/detect/predict'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["RUNS_FOLDER"] = RUNS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size (16MB)

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return filename
    return render_template('index.html')

# Route to serve images
@app.route('/img/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/train/<filename>', methods=["POST"])
def train_data(filename):
    delete_all_in_detect()
    str = collect_data_by_train_model(filename)
    return str

# Get runs image
@app.route('/runs/<filename>')
def get_result_image(filename):
    print('-- get_result_image --')
    if "png" in filename:
        filename = filename.replace("png", "jpg")
        print(filename)
    return send_from_directory(app.config["RUNS_FOLDER"], filename)

@app.route('/')
def hello():
    return render_template('index.html', name=str)

# Common function
def delete_all_in_detect():
    folder_path = 'runs/detect'
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)  # Delete files or symlinks
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Delete folders
        print(f"All contents of '{folder_path}' have been deleted.")
    else:
        print(f"Folder '{folder_path}' does not exist.")

if __name__ == '__main__':
    app.run(debug=True)