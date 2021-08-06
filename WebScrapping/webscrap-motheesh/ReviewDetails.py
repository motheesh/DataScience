# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 15:58:46 2021

@author: motheesh jay
"""
import FlipkartWebScrapper
import pandas as pd
class ReviewDetails(object):
    
    def __init__(self,searchKey,ProductName,price,UserName,rating,ShortComments):
        self.searchKey=searchKey
        self.ProductName=ProductName
        self.price=price
        self.UserName=UserName
        self.rating=rating
        self.ShortComments=ShortComments
        
    def __str__(self):
        return f"{self.searchKey},{self.ProductName},{self.price},{self.UserName},{self.rating},{self.ShortComments}"
    
    def as_dict(self):
        return {'searchKey': self.searchKey, 'ProductName': self.ProductName, 'price': self.price,
                'UserName':self.UserName,'rating':self.rating,'ShortComments':self.ShortComments}
                
    def get_DF(self,reviews_list):
        return pd.DataFrame([x.as_dict()for x in reviews_list])