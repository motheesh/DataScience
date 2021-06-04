from os import write
import mysql.connector  as connection
from logger import logger 
from customErrorHandler import inSufficientDataError
from queryDetails import query_details
from flask import current_app as app
import csv
import os

class dbOperations:
    def __init__(self,data,typeOfOperation):
        self.data=data
        self.typeOfOperation=typeOfOperation
    
    def __str__(c):
        return "<This class handle all DML and DDL Database operations>"

      
    def handleDbOperation(self):
        """
            This function is used to create,delete,update and insert data into the table 
            
            Parameters:
            argument1 (json): required info to perform db operations
            argument2 (str): type of operation whether it is update/delete/create/insert
            
            return bool -> True if success else False
        """

        is_Download=False
        if self.typeOfOperation=="download":
            is_Download=True
            self.typeOfOperation="select"
            
        try:
            query_data=query_details(self.data)
            sql_query=query_data.generate_query(query_data,self.typeOfOperation)
            data=self.get_data(sql_query,self.typeOfOperation)
            if is_Download==True:
                tabledata=data["data"]
                header=data["headers"]
                return self.downloadData(tabledata,header)
            return data
        except (inSufficientDataError,) as e:
            logger.log_error(e.error,"error")
            return {"message":e.error}
        
    def get_MySql_Connection(self):
        try:
            return connection.connect(host=app.config["DB_HOST"] ,user=app.config["DB_USER"],passwd=app.config["DB_PASS"],port=3306,database=app.config["DB_DATABASE"],use_pure=True)
        except:
            return None
    def convertDbResultToJson(self,data):
        arrList=[]
        if data:
            for row in data:
                rowList=[]
                for col in row:
                    rowList.append(col)
                arrList.append(rowList)
            return arrList

    def downloadData(self,data,header):
        try:
            file_path=app.config["DOWNLOAD_FILE_PATH"]+app.config["DOWNLOAD_FILE_NAME"]
            print(file_path)
            with open(file_path,'w',newline="") as file:
                writer=csv.writer(file)
                writer.writerow(header)
                writer.writerows(data)
            return {"status_code":200,"status":"success","message":"download successful","file_name":app.config["DOWNLOAD_FILE_NAME"],"download_path":os.path.abspath(file_path),"relative_path":file_path}
        except:
            return {"status_code":500,"status":"failed","message":"download failed","error":"Internal Server Error"}

    def get_data(self,query,typeOfOperation):
        try:
            mydb=self.get_MySql_Connection()
            if mydb:
                cursor=mydb.cursor()
                if typeOfOperation=="bulk":
                    cursor.executemany(query["query"],query["data"])
                else:
                    cursor.execute(query)
                if typeOfOperation=="select": 
                    data=cursor.fetchall()
                    data_toList=self.convertDbResultToJson(data)
                    field_names = [i[0] for i in cursor.description]
                    return {"headers":field_names,"count":len(data_toList) if data_toList else 0  ,"data":data_toList or [],"status":"success","statusCode":200,"message":f"{typeOfOperation} successful"}
                elif (typeOfOperation=="update" or typeOfOperation=="delete" or typeOfOperation=="bulk" or typeOfOperation=="insert") and cursor.rowcount>0:
                    mydb.commit()
                    type_update="insert" if typeOfOperation=="bulk" else typeOfOperation
                    return {"data":f"{cursor.rowcount} rows {type_update} successful","status":"success","statusCode":200,"message":f"{type_update} successful"}
                elif (typeOfOperation=="create"):
                    return {"data":f"Table created successfully","status":"success","statusCode":201,"message":f"{typeOfOperation} successful"}                       
                elif (typeOfOperation=="update" or typeOfOperation=="delete") and cursor.rowcount==0:
                    return {"data":f"0 rows {typeOfOperation} affected","status":"success","statusCode":200,"message":f"no matching info found to {typeOfOperation} this data "}
                #print(cursor.rowcount)
                cursor.close()
                
            else:
                logger.log_error("DB connection error","error")
                return {"data":[],"status":"DB connection error","statusCode":500,"message":"unable to proccess your request due to internal server error"}
        except connection.Error as err:
            logger.log_error("Something went wrong: {}".format(err),"error")
            return {"status":"Error","statusCode":500,"error_message":f"unable to proccess your request due to {err.msg}"}  
        finally:
            if mydb:
                mydb.close() 
        
    def display_all(self,data):
        if data:
            for row in data:
                for col in row:
                    print(col)
                
                

