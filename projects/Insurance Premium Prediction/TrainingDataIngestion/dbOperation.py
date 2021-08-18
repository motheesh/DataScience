from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement, BatchStatement
from cassandra.policies import RetryPolicy
import numpy as np
import config
from ApplicationLogger.logger import logger
from TrainingDataValidation.ValidateTrainingData import TrainValidation
import pandas as pd   
    
class dboperations:
    def __init__(self):
        self.TrainingLogPath="./TrainingLog/DataIngestionLog"
        self.TrainDbLogger=logger(self.TrainingLogPath)
        self.session=self.CreateSession()
    def CreateSession(self):
        try:
            self.TrainDbLogger.log("info",f"creating DB connection starts ")
            cloud_config= {
                'secure_connect_bundle': config.BUNDLE_PATH
            }
            auth_provider = PlainTextAuthProvider(config.CLIENT_ID, config.SECRET_KEY)
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider,protocol_version=4)
            self.cluster=cluster
            session = cluster.connect()
            self.TrainDbLogger.log("info",f"created DB connection")
            return session
        except Exception as e:
            self.TrainDbLogger.log("error",f"error during db connection {e}")
            raise Exception(e)
            
    def close(self):
        try:
            self.TrainDbLogger.log("info",f"started close DB connection operation")
            self.cluster.shutdown()
            self.TrainDbLogger.log("info",f"closed DB connection successfully")
        except Exception as e:
            self.TrainDbLogger.log("error",f"error while closing db connection {e}")
            
    def executeQuery(self,query,values=[]):
        try:
            self.TrainDbLogger.log("info",f"executing query starts")
            session=self.session
            if len(values)>0:
                query=self.prepareQuery(session,query,values)
            result=session.execute(query)
            self.TrainDbLogger.log("info",f"Ending query execution")
            return result
        except Exception as e:
            self.TrainDbLogger.log("error",f"error during query execution {e}")
            raise Exception(e)

    def executeQueryOne(self,query,values=[]):
        try:
            self.TrainDbLogger.log("info",f"starting one query execution")
            session=self.session
            if len(values)>0:
                query=self.prepareQuery(session,query,values)
            result=session.execute(query).one()
            self.TrainDbLogger.log("info",f"Ending one query execution")
            return result
        except Exception as e:
            self.TrainDbLogger.log("error",f"error during query execution {e}")
            raise Exception(e)
            
    def truncateTable(self,query):
        try:
            self.TrainDbLogger.log("info",f"starting Truncate table Operation")
            result=self.executeQueryOne(query)
            self.TrainDbLogger.log("info",f"Ending Truncate table Operation")
        except Exception as e:
            self.TrainDbLogger.log("error",f"error during Truncate table {e}")
            raise Exception(e)
    
    def createTable(self,query):
        try:
            self.TrainDbLogger.log("info",f"starting  create table Operation")
            result=self.executeQueryOne(query)
            self.TrainDbLogger.log("info",f"Ending create table Operation")
        except Exception as e:
            self.TrainDbLogger.log("error",f"error during creating table {e}")
            raise Exception(e)
        
    def dropTable(self,query):
        try:
            self.TrainDbLogger.log("info",f"starting drop table Operation")
            result=self.executeQuery(query)
            self.TrainDbLogger.log("info",f"Ending drop table Operation")
        except Exception as e:
            self.TrainDbLogger.log("error",f"error during dropping table {e}")
            raise Exception(e)
    
    def getTrainData(self,query):
        try:
            self.TrainDbLogger.log("info",f"starting get train data Operation")
            result=self.executeQuery(query)
        except Exception as e:
            self.TrainDbLogger.log("error",f"error during getting data from table using select query {e}")
        self.TrainDbLogger.log("info",f"Ending get train data Operation")
        return result
        
    def prepareBatchData(self,query,batchList,columns):
        batch=BatchStatement()
        try:
            self.TrainDbLogger.log("info",f"starting Batch Data query preperation")
            for i in range(0,len(batchList)):
                values=tuple([batchList.loc[i][j] if j=="id" else str(batchList.loc[i][j])  for j in columns])
                #print(values)
                #print(query)
                batch.add(SimpleStatement(query),values )
            self.TrainDbLogger.log("info","Ending Batch Data query preperation")
        except Exception as e:
            self.TrainDbLogger.log("error",f"Error while preparing batch insert query {e}")
            raise Exception(e)
        return batch
        
    def insertBatchData(self,query,batchList,columns):
        try:
            self.TrainDbLogger.log("info",f"starting Batch data insertion")
            session=self.session
            batch=self.prepareBatchData(query,batchList,columns)
            result=session.execute(batch)
            self.TrainDbLogger.log("info",f"Ending Batch data insertion")
            return 1
        except Exception as e:
            self.TrainDbLogger.log("error",f"error during batch data insertion {e}")
            #raise Exception(e)

    def prepareQuery(self,session,query,values):
        try:
            self.TrainDbLogger.log("info",f"starting query preperation for execution")
            stmt=session.prepare(query)
            qry=stmt.bind(values)
            self.TrainDbLogger.log("info",f"Ending query preperation for execution")
            return qry
        except Exception as e:
            self.TrainDbLogger.log("error",f"error during query preparation {e}")
            raise Exception(e)