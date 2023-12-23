import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

@dataclass           #used to automatically generate base functionalities to classes
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")



class DataIngestion:
    def __init__(self):
        self.ingestion_config= DataIngestionConfig()     # when this is executed the 3 paths defined above will be saved in DataIngestionConfig() variable

    def initiate_data_ingestion(self):                     #read and write data
        logging.info("Entered the data ingestion method or component")
        
        try:
            
            df= pd.read_csv('Notebook\data\StudentsPerformance.csv')   # read data
            logging.info('Read the dataset as dataframe')

            #creating folders/paths for the test, train, and raw data paths 
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True) #initiating raw data path and exist_ok=True checks weather it is present or not 

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True) #saving data to raw_data_path

            logging.info("Train test split initiated")
            train_set, test_set=train_test_split(df,test_size=0.2,random_state=42) 

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Inmgestion of the data iss completed ")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )


        except Exception as e:
            raise CustomException(e,sys)

if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data = obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    data_transformation.initiate_data_transformation(train_data,test_data)
    