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

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Upload traffic image
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

# Show uploaded image
@app.route('/img/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Train model with uploaded image
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

# Analyze traffic data and show in web page
@app.route('/analysis/<filename>',  methods=["POST"])
def analy_data(filename):
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
            print('Intersection : ')
            intersection += calulate_green_time(item, num)
            print('Intersection : ',intersection)
        if "east" in item :
            print('East : ')
            east += calulate_green_time(item, num)
            print('East : ',east)
        if "north" in item: 
            print('North : ')
            north += calulate_green_time(item, num)
            print('North : ',north)
        if "west" in item:
            print('West : ')
            west += calulate_green_time(item, num)
            print('West : ',west)
        if "south" in item:
            print('South : ')
            south += calulate_green_time(item, num)
            print('South : ',south)
        print('------------------')
  

    if east > west:
        total_east_west = east
    else:
        total_east_west = west

    if north > south:
        total_south_north = north
    else:
        total_south_north = south

    # Calculate east west green time
    east_west_green =  total_east_west + intersection
    
    if east_west_green < 10:
        east_west_green = 10
    if east_west_green > 60:
        east_west_green = 60

    # Calculate north south green time
    norht_south_green = total_south_north + intersection
    if norht_south_green < 10:
        norht_south_green = 10
    if norht_south_green > 60:
        norht_south_green = 60

    print(east_west_green)
    print(norht_south_green)
    return [east_west_green, norht_south_green, east, north, west, south]

# Calculate green time base on traffic density
def calulate_green_time(transport, num):
    print('--- Calculate Green Time ---')
    print('Transport : ' + transport)
    print('Num : ' + str(num))

    if 'intersection' in transport:
        return num * 2
    elif 'car' in transport:
        return num * 2
    elif 'bus' in transport:
        return num * 4
    elif 'long-truck' in transport:
        return num * 5
    elif 'pickup-truck' in transport:
        return num * 3
    return 0
    

# Get trained image
@app.route('/runs/<filename>')
def get_result_image(filename):
    print('-- get_result_image --')
    if "png" in filename:
        filename = filename.replace("png", "jpg")
    return send_from_directory(app.config["RUNS_FOLDER"], filename)

# Main page
@app.route('/')
def hello():
    return render_template('index.html', name=str)

# Delete all trained images in training folder
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

    