from flask import Flask, request, render_template, jsonify,send_file
from flask_cors import CORS
from flask_cors import cross_origin
import pymysql
import bcrypt
import jwt
import datetime
import time 
from functools import wraps
import os
import uuid
import csv
import json
from matching import map_sys
from read_data import read_data
# app = Flask(__name__)
app = Flask(__name__, static_folder='static', static_url_path='/static/dist')
app.config.from_object(__name__)
CORS(app,resources={r"/*":{"origins":"*"}})
app.config["SECRET_KEY"] = "thisisasecretkey"
app.secret_key = "hdiu21y3y4yhr3294"
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESS_FOLDER'] = 'process'
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

if not os.path.exists(app.config["PROCESS_FOLDER"]):
    os.makedirs(app.config["PROCESS_FOLDER"])
pymysql.install_as_MySQLdb()
con = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    db='mapping_system',
    # cursorclass=pymysql.cursors.DictCursor
)
cursor=con.cursor()


@app.route("/")
def index():
    return "Hello World!"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    cursor.execute('SELECT password FROM users WHERE username=%s', username)
    result = cursor.fetchone()

    if not result:
        # User not found
        return jsonify({'message': 'User Not Found'}), 403

    # Check password hash with bcrypt
    if bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
        cursor.execute('SELECT id,username,firstname,lastname,email FROM users WHERE username=%s', username)
        result = cursor.fetchone()
        return jsonify({'message': 'Login successful','userinfo':{'userid':result[0], 'username':result[1],'firstname':result[2],'lastname':result[3],'email':result[4]}}), 200
    else:
        # Passwords do not match
        return jsonify({'message': 'Invalid credentials'}), 403

@app.route("/upload",methods=["POST"])
def upload():
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    user_id = request.headers.get('Authorization').split(' ')[1]
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], user_id)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    uuid_str = str(uuid.uuid4())
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], user_id, uuid_str+'.txt'))
    return jsonify({'message': 'File uploaded successfully','file_id':uuid_str}), 200
    # if file:
    #     file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
    #     return jsonify({'message': 'File uploaded successfully'}), 200
    # else:
    #     return jsonify({'message': 'File upload failed'}), 403
# @app.route("/upload/<string:user_id>", methods=["POST"])
# def upload_file(user_id):
#     if "file" not in request.files:
#         return "No file part", 400
    
#     file = request.files["file"]
#     if file.filename == "":
#         return "No selected file", 400
#     save_path = os.path.join(app.config["UPLOAD_FOLDER"], user_id[1:-1])
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)
#     uuid_str = str(uuid.uuid4())
#     file.save(os.path.join(app.config["UPLOAD_FOLDER"], user_id[1:-1], uuid_str+'.txt'))
#     return jsonify({'message': 'File uploaded successfully','file_id':uuid_str}), 200




@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    cursor.execute('SELECT * FROM users WHERE username=%s OR email=%s', (username, email))
    result = cursor.fetchone()
    if result:
        return jsonify({'message': 'User or Email already exists'}), 403
    else:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute('INSERT INTO users(username, password, email,firstname,lastname) VALUES(%s, %s, %s, %s, %s)', (username, hashed, email, '', ''))
        con.commit()
        return jsonify({'message': 'User created successfully'}), 200


@app.route("/getuserinfo",methods=["GET"])
def getuserinfo():
    data = request.headers.get('Authorization').split(' ')[1]
    username = jwt.decode(data, app.config['SECRET_KEY'],algorithms=["HS256"])['username']
    cursor.execute('SELECT * FROM users WHERE username=%s', username)
    result = cursor.fetchone()
    if result:
        return jsonify({'message': 'User found','userid':result[0], 'username':result[1],'firstname':result[2],'lastname':result[3],'email':result[4]}), 200
    else:
        return jsonify({'message': 'User not found'}), 403

@app.route("/process",methods=["POST"])
def process():
    data = request.get_json()
    userid = data.get("userid")['userid']
    username = data.get("userid")['username']
    fileid = data.get("file_id")
    save_path = os.path.join(app.config["PROCESS_FOLDER"], userid)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    # pending_check = False
    for i in fileid:
        map = map_sys('uploads/'+userid+'/'+i+'.txt', 'process/'+userid+'/'+i+'.csv')
        map.mapping()
        cursor.execute('INSERT INTO Mappings(id,user_id,username,Editdate) VALUES(%s, %s,%s, %s)', (i, userid, username, time.strftime('%Y-%m-%d %H:%M:%S')))
        con.commit()
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"], userid, i+'.txt'))
    return jsonify({'message': 'File processed successfully'}), 200

@app.route("/getmaps",methods=["GET"])
def getmap():
    userid = request.headers.get('Getmapping').split(' ')[1]
    cursor.execute("SELECT * FROM Mappings")
    result = cursor.fetchall()
    temp = []
    if result:
        for i in result:
            temp.append({'mapid':i[0],'userid':i[1],'username':i[2],'comment':i[3],'editdate':i[4].strftime('%Y-%m-%d %H:%M:%S')})
        return jsonify({'message': 'Map found','map':temp}), 200
    else:
        return jsonify({'message': 'Map not found'}), 403
    
@app.route("/deletemap/<string:mapping_id>/<user_id>",methods=["DELETE"])
def deleteMap(mapping_id,user_id):
    # return jsonify({'message': mapping_id}), 200
    cursor.execute("DELETE FROM Mappings WHERE id = %s", mapping_id)
    con.commit()
    file_path = os.path.join(app.config["PROCESS_FOLDER"], user_id,mapping_id+'.csv')
    os.remove(file_path)
    return jsonify({'message': 'Map deleted successfully'}), 200


@app.route("/getmapresult/<user_id>/<string:mapping_id>",methods=["GET"])
def getmapresult(user_id,mapping_id):
    path = os.path.join(app.config["PROCESS_FOLDER"], user_id, mapping_id+'.csv')
    with open(path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = json.dumps([row for row in csv_reader])
    return data, 200

@app.route("/editmapping",methods=["POST"])
def editmapping():
    data = request.get_json()
    editinfo = data.get("editinfo")
    index = editinfo['index']
    userid = data.get("userid")
    mapid = data.get("mapid")
    path = os.path.join(app.config["PROCESS_FOLDER"], userid, mapid+'.csv')

    # Edit data
    newrow = [editinfo['raw'], editinfo['result'], editinfo['Flag']]
    # Edit the process csv file
    with open(path, mode='r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
        rows[index+1] = newrow
    with open(path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    with open('modify.csv', mode='r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
        found = False
        for row in rows:
            if newrow[0] in row:
                row[1] = newrow[1]
                found = True
                break
        if not found:
            rows.append(newrow[0:2])
    with open('modify.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    return jsonify({'message': 'Map edited successfully'}), 200
@app.route("/deletemapping",methods=["POST"])
def deletemapping():
    data = request.get_json()
    index = data.get("mapinfo")["index"]
    userid = data.get("userid")
    mapid = data.get("mapid")
    path = os.path.join(app.config["PROCESS_FOLDER"], userid, mapid+'.csv')
    with open(path, mode='r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
        del rows[index+1]
    with open(path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    return jsonify({'message': 'Map deleted successfully'}), 200
# @app.route("/getinfo",methods=["ge"])
# def getinfo():
#     data = request.get_json()
#     tkn = data.get("tkn")
#     username = jwt.decode(tkn, app.config['SECRET_KEY'],algorithms=["HS256"])['username']
#     cursor.execute('SELECT * FROM users WHERE username=%s', username)
#     result = cursor.fetchone()
#     if result:
#         return jsonify({'message': 'User found','username':result[1],'firstname':result[2],'lastname':result[3],'email':result[4]}), 200
#     else:
#         return jsonify({'message': 'User not found'}), 403


# @app.route("/checklogin")
# @token_required
# def checklogin():
#     if session.get('username') == request.args.get('token'):
#         return jsonify({'message': 'Login successful'}), 200
#     else:
#         return jsonify({'message': 'Invalid credentials'}), 403
    


# @app.route("/upload", methods=["POST"])
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

# @app.route("/modify", methods=["POST"])
# def modify_file():
#     data = request.get_json()
#     rawdata = data.get("modifiedData")
#     # print(data)
#     df = pandas.read_csv('modify.csv')
#     processed_filename = data.get("output_filename")
#     df_processed_file = pandas.read_csv(os.path.join(app.config["PROCESS_FOLDER"], processed_filename))
#     for key, value in rawdata.items():
#         matched_rows = df[df['raw'] == key]
#         if len(matched_rows) == 0:
#             df = df.append({"raw": key, "result": value}, ignore_index=True)
#         else:
#             df.loc[df['raw'] == key, 'result'] = value
        
#         df_processed_file.loc[df_processed_file['raw'] == key, 'result'] = value
#     df_processed_file.to_csv(os.path.join(app.config["PROCESS_FOLDER"], processed_filename),index=False)
#     df.to_csv('modify.csv', index=False)

#     return jsonify({"message": "Successfully updated modify.csv"}), 200

# @app.route("/process", methods=["POST"])
# def process_file():
#     data = request.get_json()
#     filename = data.get("filename")
#     if not filename:
#         return "No filename provided", 400
#     file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
#     if not os.path.exists(file_path):
#         return "File not found", 404
    
#     map = map_sys(file_path, 'process_files/example.csv')
#     processed_csv = map.mapping()
#     # processed_csv = writing(result, 'example.csv')

#     response_data = {"processed_csv": processed_csv, "output_filename": "example.csv"}
#     return response_data,200

# @app.route("/delete", methods=["POST"])
# def delete_file():
#     filename = request.form.get("filename")
#     if not filename:
#         return "No filename provided", 400

#     file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    
#     if not os.path.exists(file_path):
#         return "File not found", 404

#     try:
#         os.remove(file_path)
#         return "File deleted successfully", 200
#     except Exception as e:
#         print(f"Error deleting file: {e}")
#         return "File deletion failed", 500

# @app.route("/download/<userid>/<file_id>")
# def download_file(userid, file_id):
@app.route("/download", methods=["POST"])
def download_file():
    file_id = request.json['file_id']
    userid = request.json['userid']
    path = os.path.join(app.config["PROCESS_FOLDER"], userid, file_id+'.csv')
    return send_file(path, as_attachment=True)



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