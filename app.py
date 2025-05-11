import os
import shutil
import math
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from lab import collect_data_by_train_model, readJsonFile

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
    data = str.split(",")
    result = ""
    for item in data:
        item = item.strip()
        analysis_data = item.split(" ")
        num = analysis_data[0]
        text = readJsonFile(analysis_data[1])
        result += num + " " + text + " <br>"
    return result

@app.route('/analysis/<filename>',  methods=["POST"])
def analy_data(filename):
    saturation_flow = 1.584
    str = collect_data_by_train_model(filename)
    data = str.split(",")
    east = 0
    north = 0
    west = 0
    south = 0
    intersection = 0
    for item in data:
        item = item.strip()
        analysis_data = item.split(" ")
        num = int(analysis_data[0])
        if "intersection" in item : 
            intersection += num
        if "east" in item :
            east += num
        if "north" in item: 
            north += num
        if "west" in item:
            west += num
        if "south" in item:
            south += num
    total_east_west = east + west
    total_south_north = south + north

    # Calculate east west green time
    east_west_green =  math.ceil(total_east_west / saturation_flow) + (intersection * 2) # add 2 more seconds for intersection
    if east_west_green < 10:
        east_west_green = 10
    if east_west_green > 30:
        east_west_green = 30

    # Calculate north south green time
    norht_south_green = math.ceil(total_south_north / saturation_flow) + (intersection * 2) # add 2 more seconds for intersection
    if norht_south_green < 10:
        norht_south_green = 10
    if norht_south_green > 30:
        norht_south_green = 30

    print('------------------')
    print(east_west_green)
    print(norht_south_green)
    return [east_west_green, norht_south_green]

# Get runs image
@app.route('/runs/<filename>')
def get_result_image(filename):
    print('-- get_result_image --')
    if "png" in filename:
        filename = filename.replace("png", "jpg")
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