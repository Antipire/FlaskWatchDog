import configparser
from flask import Flask, jsonify
import os

app = Flask(__name__)

# Чтение конфигурации
config = configparser.ConfigParser()
config.read('config.ini')
directory_to_watch = config['Directories']['directory_to_watch']

@app.route('/')
def get_directory_contents():
    contents = os.listdir(directory_to_watch)
    return jsonify(contents)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)