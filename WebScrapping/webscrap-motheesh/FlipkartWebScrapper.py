from ReviewDetails import ReviewDetails
import requests
from bs4 import BeautifulSoup
from dbOperations import dboperations
from logger import logger
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
    def get_ProductReviewPage(self,url):
        try:
            search_response=requests.get(self.baseURL+url)
            search_Content=self.get_DOM(search_response)
            temp=FlipkartWebScrapper()
            temp.price=search_Content.find('div',class_=self.classNames["price"]).text
            temp.ProductName=search_Content.find('span',class_=self.classNames["Product_name"]).text
            return search_Content,temp
        except:
            return None,None


    def get_allProductReviews(self,number,AllProducts):
            sum_len=0
            all_reviews=[]
            product_count=0
            for i in AllProducts:
                DOM,obj=self.get_ProductReviewPage(i)
                if DOM!=None and obj!=None:
                    product_reviews=obj._get_reviews(self.search,DOM)
                    all_reviews.extend(product_reviews)
                    sum_len+=len(product_reviews)
                    if sum_len>=number:
                        break
                    #print(f"reviews {sum_len}")
                product_count+=1
            return all_reviews,product_count

    def get_allProducts(self,search,page=1):
        self.search=search
        search_list=self.searchProduct(search,page)
        list_div=search_list.find_all("div",class_="_13oc-S")
        list_a=list(map(lambda x:x.find("a")["href"],list_div))
        #first_search_url=list(map(lambda x: x["href"],list_div.find('a')))
        #print(f"url list {len(list_a)}")
        return list_a    

    def get_DOM(self,response):
        return BeautifulSoup(response.content,"lxml")
        
    def searchProduct(self,search,pageNo=1):
        search_query=f"search?q={search}&page={pageNo}"
        url=self.baseURL+"/"+search_query
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
        try:
            if by_type=="class":
                result=DOM.find(tag_name,class_=type_name)
            elif by_type=="id":
                result=DOM.find(tag_name,id_=type_name)
            result=result.text
        except:
            result=""

        
        return result

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

    def get_reviews_list(self,search,limit):
        try:
            obj=dboperations()
            wanted_review=limit
            is_present=obj.checkProductPresence(search)
            pcount=0
            rcount=0
            if is_present:
                print("yes")
                pcount,rcount=obj.checkSearchCount(search)
            else:
                obj.addSearchDetails(search,0,0)
            page_completed=int(rcount/24)
            slice_req=((page_completed*24)-rcount)*(-1)
            wanted_review-=rcount
            Start_page=page_completed+1
            print(f"start page {Start_page}")
            print(f"reviews required {wanted_review}")
            reviews_list=[]
            if wanted_review>0:
                #get_reviews
                r_count=0
                p_count=0
                while wanted_review>0:
                    all_product=self.get_allProducts(search,Start_page)
                    if slice_req>0:
                        all_product=all_product[slice_req:]
                        slice_req=0
                    if len(all_product)==0:
                        return None
                    reviews,product_count=self.get_allProductReviews(wanted_review,all_product)
                    wanted_review-=len(reviews)
                    reviews_list.extend(reviews)
                    r_count+=len(reviews)
                    p_count+=product_count
                    Start_page+=1
                new_pcount=pcount+p_count
                new_rcount=rcount+r_count
                #batch insert
                if len(reviews_list)>0:
                    obj.insertBatchReview(reviews_list)
                    #update count
                    obj.updateSearchDetails(search,new_pcount,new_rcount)
                    #calculate
            review_list=obj.get_reviews(limit,search)
            return review_list
        except Exception as e:
            logger.log_error(f"error in get_reviews_list  {e}","error")
            raise Exception(e)