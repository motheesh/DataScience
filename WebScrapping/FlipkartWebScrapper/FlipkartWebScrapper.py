from ReviewDetails import ReviewDetails
import requests
from bs4 import BeautifulSoup


class FlipkartWebScrapper:
    def __init__(self):
        self.baseURL="https://www.flipkart.com"
        self.classNames={
        "first_Item":"_1fQZEK",
        "Product_name":"B_NuCI",
        "username":"_2sc7ZR _2V5EHH",
        "rating":"_3LWZlK _1BLPMq",
        "comment":"t-ZTKy",
        "short_comment":"_2-N8zT",
        "review":"col _2wzgFH",
        "price":"_30jeq3 _16Jk6d"
        } 
        

        
    def get_DOM(self,response):
        return BeautifulSoup(response.content,"lxml")
        
    def searchProduct(self,search):
        search_query="search?q="
        url=self.baseURL+"/"+search_query+search
        res=requests.get(url)
        return self.get_DOM(res)
    
    def getFirstProduct(self,DOM):
        try:
            first_search_url=DOM.find('a',class_=self.classNames["first_Item"])["href"]
        except:
            return None

       
        first_search_response=requests.get(self.baseURL+first_search_url)
        first_search_Content=self.get_DOM(first_search_response)
        self.price=first_search_Content.find('div',class_=self.classNames["price"]).text
        self.ProductName=first_search_Content.find('span',class_=self.classNames["Product_name"]).text
        return first_search_Content
    
    def get_all_reviews(self,search):
        search_list=self.searchProduct(search)
        getFirstItem=self.getFirstProduct(search_list)
        if getFirstItem==None:
            return None
        return self._get_reviews(search,getFirstItem)
        
    def get_text(self,DOM,by_type,type_name,tag_name):
        result=""
        if by_type=="class":
            result=DOM.find(tag_name,class_=type_name)
        elif by_type=="id":
            result=DOM.find(tag_name,id_=type_name)
        return result.text

    def _get_reviews(self,search,DOM):
        review_divs=DOM.find_all("div",class_=self.classNames["review"])
        Reviews=[]
        for review in review_divs:
            name=self.get_text(review,"class",self.classNames["username"],"p")
            rating=self.get_text(review,"class",self.classNames["rating"],"div")
            #comment=get_text(review,"class",comment_class_name,"p")
            short_desc_comment=self.get_text(review,"class",self.classNames["short_comment"],"p")
            Reviews.append(ReviewDetails(search,self.ProductName,self.price,name,rating,short_desc_comment))
        return Reviews