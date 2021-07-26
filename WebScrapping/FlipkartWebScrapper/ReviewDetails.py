# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 15:58:46 2021

@author: motheesh jay
"""
import FlipkartWebScrapper
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
    
