from flask import request,jsonify
def isValidJsonRequest(func):
    def wrapper(*args,**kwargs):
        if not request.get_json():
            return jsonify({"status":"Invalid request","statusCode":400,"message":"Please provide valid json data"})
        return func(*args,**kwargs)
    wrapper.__name__ = func.__name__
    return wrapper