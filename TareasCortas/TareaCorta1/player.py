
from flask import Flask, render_template, request, send_from_directory, jsonify
import json

app = Flask(__name__)

data_file_path = ""

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_data")
def get_data():
    # with open("data.json", "r") as file:
    global data_file_path
    with open(data_file_path, "r") as file:
        data = json.load(file)
    return jsonify(data)


@app.route("/set_file_path", methods=["POST"])
def set_file_path():
    global data_file_path
    data = request.get_json()
    file_path = data.get("filePath")

    if not file_path:
        return jsonify(error="No file path provided"), 400

    # Aquí esta la ruta del archivo
    print(file_path)
    data_file_path = file_path

    return jsonify(message="File path received successfully"), 200


if __name__ == "__main__":
    app.run(debug=True)
