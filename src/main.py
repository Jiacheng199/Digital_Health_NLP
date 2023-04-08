from matching import map_sys
from read_data import read_data
from flask import send_from_directory
from io import StringIO
from flask import Flask, request, render_template, jsonify, send_file
from collections import Counter
from matching import map_sys
from writing import writing
import csv
import os
from flask_cors import CORS
import pandas
app = Flask(__name__)

app.config.from_object(__name__)
app.secret_key = "your_secret_key"
UPLOAD_FOLDER = "uploads_files"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
PROCESS_FOLDER = "process_files"
app.config["PROCESS_FOLDER"] = PROCESS_FOLDER
ALLOWED_EXTENSIONS = {".csv", ".txt", ".json"}
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])
if not os.path.exists(app.config["PROCESS_FOLDER"]):
    os.makedirs(app.config["PROCESS_FOLDER"])
CORS(app,resources={r"/*":{"origins":"*"}})

@app.route("/")
def index():
    return render_template("uploadpage.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400
    
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400
    
    _, file_extension = os.path.splitext(file.filename)
    if file_extension.lower() not in ALLOWED_EXTENSIONS:
        return "Unsupported file type", 400
    
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
    print(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
    return "File uploaded successfully", 200

@app.route("/modify", methods=["POST"])
def modify_file():
    data = request.get_json()
    rawdata = data.get("modifiedData")
    # print(data)
    df = pandas.read_csv('modify.csv')
    processed_filename = data.get("output_filename")
    df_processed_file = pandas.read_csv(os.path.join(app.config["PROCESS_FOLDER"], processed_filename))
    for key, value in rawdata.items():
        matched_rows = df[df['raw'] == key]
        if len(matched_rows) == 0:
            df = df.append({"raw": key, "result": value}, ignore_index=True)
        else:
            df.loc[df['raw'] == key, 'result'] = value
        
        df_processed_file.loc[df_processed_file['raw'] == key, 'result'] = value
    df_processed_file.to_csv(os.path.join(app.config["PROCESS_FOLDER"], processed_filename),index=False)
    df.to_csv('modify.csv', index=False)

    return jsonify({"message": "Successfully updated modify.csv"}), 200

@app.route("/process", methods=["POST"])
def process_file():
    # cmd = 'mpiexec -n 12 python snomed_ct.py'
    # os.system(cmd)
    data = request.get_json()
    filename = data.get("filename")
    if not filename:
        return "No filename provided", 400
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if not os.path.exists(file_path):
        return "File not found", 404
    
    map = map_sys(file_path, 'process_files/example.csv')
    processed_csv = map.mapping()
    # processed_csv = writing(result, 'example.csv')

    response_data = {"processed_csv": processed_csv, "output_filename": "example.csv"}
    return response_data,200

@app.route("/delete", methods=["POST"])
def delete_file():
    filename = request.form.get("filename")
    if not filename:
        return "No filename provided", 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    
    if not os.path.exists(file_path):
        return "File not found", 404

    try:
        os.remove(file_path)
        return "File deleted successfully", 200
    except Exception as e:
        print(f"Error deleting file: {e}")
        return "File deletion failed", 500

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["PROCESS_FOLDER"], filename, as_attachment=True)

# ！！！
@app.route('/visualization/<filename>')
def visualization(filename):
    print(123)
    csv_path = os.path.join(app.config["PROCESS_FOLDER"], filename)
    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile)
        isFirstLine = True
        counts = {
            'Matched': 0,
            'Non-Match': 0,
            'not sure': 0
        }
        for row in reader:
            if isFirstLine:
                isFirstLine = False
            else:
                if row[1] == 'Non-Match':
                    counts['Non-Match'] += 1
                else:
                    counts['Matched'] += 1

        total = counts['Matched'] + counts['Non-Match'] + counts['not sure']
        matched_percentage = round(counts['Matched'] / total * 100, 2)

        chart_data = {
            'labels': ['Matched', 'Non-Match'],
            'datasets': [
                {
                    'label': 'Matched', 
                    'data': [counts['Matched'], counts['Non-Match']],
                    'backgroundColor': ['rgba(75, 192, 192, 0.8)',
      'rgba(54, 162, 235, 0.8)',
      #'rgba(153, 102, 255, 0.8)'
      ]
                }
            ]
        }

    return render_template('visualization.html', matched_percentage = matched_percentage, chart_data = chart_data)

# @app.route('/upload1', methods=['POST'])
# def upload():
#     if "files0" not in request.files:
#         return "No file part", 400
    # file = request.files["files"]
    # if file.filename == "":
    #     return "No selected file", 400
    
    # _, file_extension = os.path.splitext(file.filename)
    # if file_extension.lower() not in ALLOWED_EXTENSIONS:
    #     return "Unsupported file type", 400
    # count = 0
    # while True:
    #     if "files"+str(count) not in request.files:
    #         break
    #     file = request.files["files"+str(count)]
    #     file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
    #     count += 1
    #     print(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
    # return "Uploaded successfully", 200

# @app.route("/dropzone1", methods=["POST"])
# def upload_file():
#     if "file" not in request.files:
#         return "No file part", 400

#     file = request.files["file"]
#     if file.filename == "":
#         return "No selected file", 400
    
#     _, file_extension = os.path.splitext(file.filename)
#     if file_extension.lower() not in ALLOWED_EXTENSIONS:
#         return "Unsupported file type", 400
    
#     file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
#     print(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
#     return "File uploaded successfully", 200



if __name__ == '__main__':
    app.run(debug=True)