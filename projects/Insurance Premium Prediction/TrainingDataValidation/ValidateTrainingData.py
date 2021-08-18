#imports
import numpy as np
import pandas as pd
import json
import os
import re
from ApplicationLogger.logger import logger
class TrainValidation:
    def __init__(self):
        self.TrainingLogPath="./TrainingLog/DataValidationLog"
        self.Trainlogger=logger(self.TrainingLogPath)
        try:
            self.Trainlogger.log("info","starting Initialization of TrainValidation object")
            self.BatchFilePath="./TrainingBatchDataset"
            self.TrainSchemaPath="./DatasetSchema/TrainingDataSchema.json"
            self.GoodDataPath="./TrainingGoodDataset"
            self.BadDataPath="./TrainingBadDataset"
            self.Trainlogger.log("info","Ending Initialization of TrainValidation object")
        except Exception as e:
            self.Trainlogger.log("error","error while Initializing TrainValidation object{e}")
            

        
        
    def getTrainSchema(self):
        self.Trainlogger.log("info","Started reading TrainSchema json")
        try:
            f = open (self.TrainSchemaPath, "r")
            train_schema_json=json.loads(f.read())
            f.close()
        except Exception as e:
            self.Trainlogger.log("error","Error occured while reading training schema")
        self.Trainlogger.log("info","Ended reading TrainSchema json")
        return train_schema_json
    
    def fileNameValidation(self,file,pattern):
        self.Trainlogger.log("info","starting file name validation")
        result=False
        try:
            if re.match(pattern,file):
                result=True
            else:
                self.Trainlogger.log("info","File name is not matched")
                result=False
        except Exception as e:
            self.Trainlogger.log("error",f"Error occured while validating file name {e}")
        self.Trainlogger.log("info","ending file name validation")
        return result
        
    def checkColumnType(self,actualTypes,requiredTypes):
        self.Trainlogger.log("info","starting column Type validation")
        result=False
        try:
            result=sum([i in j for i,j in zip(requiredTypes,actualTypes)])==len(requiredTypes)
            self.Trainlogger.log("info","Ending column Type validation")
        except Exception as e:
            self.Trainlogger.log("error",f"Error occured while validating column Types {e}")
        return result
    
    def checkColumnNames(self,actualColumnName,columnNames):
        self.Trainlogger.log("info","starting column Names validation")
        result=False
        try:
            result=sum(columnNames==actualColumnName)==len(columnNames)
            self.Trainlogger.log("info","Ending column Names validation")
        except Exception as e:
            self.Trainlogger.log("error",f"Error occured while validating column Names {e}")
        return result
    
    def allCol_LessThan95_NA(self,data):
        self.Trainlogger.log("info"," starting >95% Na validation")
        try:
            dd=(data.isna().sum()/len(data))*100
            result=True
            for i in dd.index:
                if dd[i]>95:
                    self.Trainlogger.log("info",f"column {i} have >95% NA so we reject this dataset")
                    result=False
                    break
        except Exception as e:
            self.Trainlogger.log("error",f"Error occured while validating allCol_LessThan95_NA {e}")  
        self.Trainlogger.log("info",f"completing >95% NA validation")
        return result
    
    def isAllcolumnPresent(self,data,columns):
        self.Trainlogger.log("info","Starting column values and data type check")
        columnLength,actualLength=len(columns),len(data.columns)
        actualColumnName,actualColumnType=data.dtypes.index,data.dtypes.values.astype("str")
        columnNames,columnTypes=list(columns.keys()),columns.values()
        try:
            if actualLength==columnLength:
                if self.checkColumnNames(actualColumnName,columnNames):
                    if self.checkColumnType(actualColumnType,columnTypes):
                        if self.allCol_LessThan95_NA(data):
                            self.Trainlogger.log("info","Column validation succesfull")
                            return True
                        else:
                            return False
                else:
                    return False
            else:
                return False
        except Exception as e:
            self.Trainlogger.log("error",f"error occured during column validation {e}")
            return False
            
    
    def replace_NaWithNULL(self,data):
        self.Trainlogger.log("info","Replacing NA values with NULL")
        try:
            data=data.fillna("NULL")
        except Exception as e:
            self.Trainlogger.log("error",f"error while Replacing NA values with NULL {e}")
        return data
    
    def moveGoodData(self,data,filename):
        self.Trainlogger.log("info","started data moving to good data folder")
        try:
            data.to_csv(f"{self.GoodDataPath}/{filename}",header=True,index=None)
            self.Trainlogger.log("info","ending data movement to good data folder")
            return True
        except:
            self.Trainlogger.log("error",f"error occured while moving file to good data folder {e}")
            return False
            
    
    def moveBadData(self,data,filename):
        self.Trainlogger.log("info","started data moving to bad data folder")
        try:
            data.to_csv(f"{self.BadDataPath}/{filename}",header=True,index=None)
            self.Trainlogger.log("info","ending data movement to bad data folder")
            return True
        except Exception as e:
            self.Trainlogger.log("error",f"error occured while moving file to bad data folder {e}")
            return False
    
    def ValidateTrainData(self):
            try:
                #read the train data schema
                self.Trainlogger.log("info","Starting the Train Validation")
                train_schema_json=self.getTrainSchema()
                pattern=train_schema_json["pattern"]
                columns=train_schema_json["columnname"]
                for fileName in os.listdir(self.BatchFilePath):
                    is_valid=self.fileNameValidation(fileName,pattern)
                    if is_valid:
                        data=pd.read_csv(f"{self.BatchFilePath}/{fileName}")
                        if self.isAllcolumnPresent(data,columns):
                            data=self.replace_NaWithNULL(data)
                            self.moveGoodData(data,fileName)
                        else:
                            self.moveBadData(data,fileName)
                self.Trainlogger.log("info","Ending the Train Validation")
            except Exception as e:
                self.Trainlogger.log("error",f"error occured while validating Train Data {e}")
                raise Exception(e)


