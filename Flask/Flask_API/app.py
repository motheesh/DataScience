from flask import Flask, json, request, jsonify,send_file,make_response
from flask_restful import Api , Resource
from dbOperations import dbOperations
from decorators import isValidJsonRequest
from flask_cors import CORS, cross_origin
import os

app=Flask(__name__)
CORS(app, support_credentials=True)
app.config.from_pyfile("config.py")
app.debug = app.config['DEBUG']


@app.route('/download_data/<filename>')
def download_file(filename):
    path=os.path.abspath(app.config["DOWNLOAD_FILE_PATH"]+filename)
    print("path is :"+ path)
    return send_file(path, as_attachment=True)

@app.route('/<query>',methods=["POST"])
@cross_origin(supports_credentials=True)
@isValidJsonRequest
def DatabaseOperations(query):
    if query in ["create","insert","delete","update","select","bulk","download"]:
        data=dbOperations(request.get_json(),query).handleDbOperation()
        response=jsonify(data)
        return response
    else:
        Flask.abort(404)



app.run(port=5000)
