
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement, BatchStatement
from cassandra.policies import RetryPolicy
from ReviewDetails import ReviewDetails
from flask import current_app as app
from logger import logger
class dboperations:
    def CreateSession(self):
        try:
            cloud_config= {
                'secure_connect_bundle': app.config["BUNDLE_PATH"]
            }
            auth_provider = PlainTextAuthProvider(app.config["CLIENT_ID"], app.config["SECRET_KEY"])
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            session = cluster.connect()
            return session
        except Exception as e:
            logger.log_error(f"error during db connection {e}","error")
            raise Exception(e)

    def executeQuery(self,query,values=[]):
        try:
            session=self.CreateSession()
            if len(values)>0:
                query=self.prepareQuery(session,query,values)
            result=session.execute(query)
            return result
        except Exception as e:
            logger.log_error(f"error during query execution {e}","error")
            raise Exception(e)

    def executeQueryOne(self,query,values=[]):
        try:
            session=self.CreateSession()
            if len(values)>0:
                query=self.prepareQuery(session,query,values)
            result=session.execute(query).one()
            return result
        except Exception as e:
            logger.log_error(f"error during query execution {e}","error")
            raise Exception(e)

    def insertBatchReview(self,batchList):
        try:
        #if True:
            query='insert into scarp.reviewdetails(id,searchkey,productname,price,username,rating,shortcomments) values(now(),%s, %s, %s, %s,%s,%s)'
            session=self.CreateSession()
            batch=BatchStatement()
            for one in batchList:
                #print(one.searchKey, one.ProductName,one.price, one.UserName,one.rating,one.ShortComments)
                batch.add(SimpleStatement(query), (one.searchKey, one.ProductName,one.price, one.UserName,one.rating,one.ShortComments))
            result=session.execute(batch)
            return 1
        except Exception as e:
            logger.log_error(f"error during batch review insertion {e}","error")
            raise Exception(e)

    def prepareQuery(self,session,query,values):
        try:
            stmt=session.prepare(query)
            qry=stmt.bind(values)
            return qry
        except Exception as e:
            logger.log_error(f"error during query preparation {e}","error")
            raise Exception(e)

    def get_reviews(self,limit,search):
        try:
            columns="searchkey,productname ,price,username,rating,shortcomments"
            selectReview=f"select {columns} from scarp.reviewdetails where searchkey='{search}' ALLOW FILTERING;" if limit==-1 else f"select {columns} from scarp.reviewdetails where searchkey='{search}' limit {limit} ALLOW FILTERING;" 
            rows=self.executeQuery(selectReview)
            reviewList=[]
            for row in rows:
                temp=ReviewDetails(row[0],row[1],row[2],row[3],row[4],row[5])
                reviewList.append(temp)
            return reviewList
        except Exception as e:
            logger.log_error(f"error during getting reviews from DB {e}","error")
            raise Exception(e)

    def checkSearchCount(self,searchKey):
        try:
            columns="searchkey,product_count,review_count"
            query=f"select {columns} from scarp.searchdetails where  searchkey=? ALLOW FILTERING;"
            row=self.executeQueryOne(query,[searchKey])
            return row.product_count,row.review_count
        except Exception as e:
            logger.log_error(f"error during checkSearchCount {e}","error")
            raise Exception(e)
    
    def checkProductPresence(self,searchKey):
        columns="searchkey,product_count,review_count"
        query=f"select {columns} from scarp.searchdetails where  searchkey=? ALLOW FILTERING"
        row=self.executeQuery(query,[searchKey])
        if len(list(row))>0:
            return 1
        else:
            return 0
    def updateSearchDetails(self,searchKey,pCount,rCount):
        try:
            query=f"update scarp.searchdetails set product_count=?,review_count=? where searchkey=?;"
            self.executeQuery(query,[pCount,rCount,searchKey])
            return 1
        except Exception as e:
            logger.log_error(f"error during updateSearchDetails {e}","error")
            raise Exception(e)
    def addSearchDetails(self,searchKey,pCount,rCount):
        try:
            query=f"insert into scarp.searchdetails(searchkey,product_count,review_count) values(?,?,?);"
            self.executeQuery(query,[searchKey,pCount,rCount])
            return 1
        except Exception as e:
            logger.log_error(f"error during addSearchDetails {e}","error")
            raise Exception(e)
    