# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 15:57:04 2021

@author: motheesh jay
"""

from flask import Flask,request, json,jsonify, render_template
from FlipkartWebScrapper import FlipkartWebScrapper
from logger import logger
app=Flask(__name__)
app.config.from_pyfile("config.py")
app.debug = app.config['DEBUG']

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    searchKey=request.args['keyword']
    print(request)
    reviews=FlipkartWebScrapper().get_all_reviews(searchKey)
    if reviews==None:
        logger.log_error(f"not able to scarp review for product {searchKey}","error")
        return render_template("Error.html",ErrorMessage=f"No product available with name '{searchKey}'")
    logger.log_error(f"{request.url}|{request.method}","info")
    return render_template("table.html",reviews=reviews)

if __name__=="__main__":
    app.run(port=5000) 