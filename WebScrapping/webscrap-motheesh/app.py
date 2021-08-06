# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 15:57:04 2021

@author: motheesh jay
"""
import traceback
from flask import Flask,request, json,jsonify, render_template
from FlipkartWebScrapper import FlipkartWebScrapper
from logger import logger
from visualize import visualize
from ReviewDetails import ReviewDetails

app=Flask(__name__)
app.config.from_pyfile("config.py")
app.debug = app.config['DEBUG']

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    try:
    #if True:
        searchKey=request.args['keyword']
        print(request)
        reviews=FlipkartWebScrapper().get_all_reviews(searchKey)
        if reviews==None:
            logger.log_error(f"not able to scarp review for product {searchKey}","error")
            return render_template("Error.html",ErrorMessage=f"No product available with name '{searchKey}'")
        logger.log_error(f"{request.url}|{request.method}","info")
        return render_template("table.html",reviews=reviews)
    except Exception as e:
        return render_template("Error.html",ErrorMessage=f"ERROR: '{e.__traceback__}'")

@app.route("/getallreviews")
def getallreviews():
    try:
    #if True:
        searchKey=request.args['keyword']
        number=int(request.args['numberofreview'])
        obj=FlipkartWebScrapper()
        #all_product=obj.get_allProducts(searchKey)
        #products,_=obj.get_allProductReviews(number,all_product)
        products=obj.get_reviews_list(searchKey,number)
        if products==None:
            logger.log_error(f"not able to scarp review for product {searchKey}","error")
            return render_template("Error.html",ErrorMessage=f"No product available with name '{searchKey}'")
        if len(products)>0:
            df=products[0].get_DF(products)
            visual=visualize()
            graph=visual.getProductWiseRatingsAndItsPrice(df)
            distribution=visual.RatingDistributionForAllProducts(df)
            reviewDistribution=visual.getReviewLengthDistribution()
            logger.log_error(f"{request.url}|{request.method}","info")
            return render_template("AllReviews.html",plot=graph,reviews=products,distribution=distribution,reviewDistribution=reviewDistribution)
        else:
            logger.log_error(f"not able to scarp review for product {searchKey}","error")
            return render_template("Error.html",ErrorMessage=f" Something went wrong please try again")           
    except Exception as e:
        return render_template("Error.html",ErrorMessage=f"ERROR: '{e}'")

if __name__=="__main__":
    app.run(port=5000) 