from TrainingDataValidation.ValidateTrainingData import TrainValidation
from TrainingDataIngestion.DataIngestion import DataIngestion
import pandas as pd

class TrainModel:
    def DataValidation(self):
        #initialize object for TrainValidation
        validate=TrainValidation()
        #validating Training data
        validate.ValidateTrainData()
        
    def DataIngestion(self):
        DI=DataIngestion()
        #Upload Data
        DI.UploadDataToDB()
        #Conver data to csv for training
        DI.CreateInput_CSVFromDB()
        
    def PipeLineCreation(self):
        pass
    
    def getBestModel(self):
        pass
        
        
    def train(self):
        self.DataValidation()
        self.DataIngestion()
        

