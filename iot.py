from flask import Flask
from light import setup, turn_east_light, turn_west_light, turn_south_light,turn_north_light

app = Flask(__name__)

@app.route('/light/<direct>/<color>', methods=['POST'])
def change_light(direct, color):
    if direct is 'east' :
        print(direct)
    if direct is 'west' :
        print(direct)
    if direct is 'north' :
        print(direct)
    if direct is 'south' :
        print(direct)
    return None

@app.route('/')
def hello():
    return 'Hello, World!'



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)